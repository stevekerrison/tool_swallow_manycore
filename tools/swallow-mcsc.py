#!/usr/bin/python

# Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
#
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>


header = \
"""swallow-mcsc.py

Take a multi-core main input and produces per-core binaries for compilation

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 1st March 2012

Usage:
  swallow-mcsc.py mcmain.xc [extra compiler options & files]

Takes a multi-core main, tries to parse it and produce a set of single-core
binaries that can be assembled into an image for TFTP'ing to the Swallow grid.
Unlike the previous xmp16-mcsc tool, this is designed for ethernet loading
rather than JTAG, so it is much quicker and doesn't need to know anything about
the network at compile time - everything is handled at runtime and the network
is already setup by the TFTP server.

Operates within $PWD
"""

import sys,os,re,subprocess,shlex,multiprocessing,math,copy

if len(sys.argv) < 2:
  print >> sys.stderr, "ERROR: Usage:",os.path.basename(sys.argv[0]),"manycoremainfile.xc [extra compiler options & files]"
  sys.exit(1)

pwd = os.getcwd()

outdir = pwd + "/"

additional_args = sys.argv[2:]

toolsdir = os.path.dirname(sys.argv[0])

includes = re.findall("^(.*#.*)$",open(sys.argv[1],"r").read(),re.M)

# Use XCC's preprocessor to get the code
xc = subprocess.Popen(["xcc", "-E","-I" + toolsdir + "/../code/sc_swallow_communication/module_swallow_comms/src/", sys.argv[1], "manycore.xn"], stdout=subprocess.PIPE).communicate()[0]
xc = re.sub("^#.*\n","",xc,0,re.M)

# Capture the main block
m = re.search("int\s*main\s*\(.*?\)\s*\{.*?return\s+0\s*;.*?}",xc,re.M|re.S)
xc = m.group(0)

#Fudge all channel declarations into arrays
def arrLen(s):
  if s == '':
    return 1;
  return int(s)

def initMain(core):
  return "\n/* Main for core " + str(core) + """*/
int main(void)
{
  unsigned ctrl_data; //Used by AEC code, maybe
  __initLinks();
//Enable dynamic AEC if we want AEC enabled even on cores that are in use
#ifdef AEC_ON_INUSE_CORE
#if AEC_DIVIDER_""" + str(core) + """ > 1
  write_pswitch_reg(swallow_id(""" + str(core) + """),XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER_""" + str(core) + """ - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#elif AEC_DIVIDER > 1
  write_pswitch_reg(swallow_id(""" + str(core) + """),XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#endif
#endif
  par
  {
"""

def endMain(core):
  return """
  }
//Enable dynamic AEC just before we free the final thread, meaning AEC is always active on this unused core
#ifndef AEC_ON_INUSE_CORE
#if AEC_DIVIDER_""" + str(core) + """ > 1
  write_pswitch_reg(swallow_id(""" + str(core) + """),XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER_""" + str(core) + """ - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#elif AEC_DIVIDER > 1
  write_pswitch_reg(swallow_id(""" + str(core) + """),XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#endif
#endif
  asm("freet"::);
  return 0;
}"""

def initInitLinks(core):
  ret = ""
  for i in includes:
    ret += i + "\n"
  ret += """#include <stdio.h>
#include "swallow_comms.h"

/* __initLinks for core """ + str(core) + """*/
void __initLinks()
{
  unsigned c, sync;
  /* Hot-patch the I/O subroutine so that _write is replaced by _write_intercept */
  io_redirect();
  /* Grab the sync chanend first, so it's always CID 0 */
  sync = getChanend((SWXLB_BOOT_ID << 16) | 0xff02);
  /* Get these board dimensions before anything tries to evaluate a real grid ID */
  asm("in %0,res[%1]":"=r"(sw_nrows):"r"(sync));
  asm("in %0,res[%1]":"=r"(sw_ncols):"r"(sync));
  
  /* Now we declare any channels we need */
"""
  return ret

def endInitLinks(core):
  return """
  /* Do sync after all chanends are allocated. */
  asm("chkct res[%0],1"::"r"(sync));
  return;
}"""
  
  

# This function contains all the reasons that I love Python... and unfortunately a for loop with an if in it
def getChans(xc):
  m = re.findall("chan(\s+(\w+)\s*(\[\s*(\d+)\s*\])?)(\s*,?\s*(\w+)\s*(\[\s*(\d+)\s*\])?)*\s*",xc,re.M|re.S)
  cvars = [item for sl in [x[1::4] for x in m] for item in sl]
  clens = map(arrLen,[item for sl in [x[3::4] for x in m] for item in sl])
  for idx,val in enumerate(cvars):
    if val == '':
      del cvars[idx]
      del clens[idx]
  return zip(cvars,clens)
  
chans = getChans(xc)
print "Found %d channels declared" % sum([x[1] for x in chans])

m = re.findall("par(\s+\([^\{]*\))?\s*\{(.*?)\}",xc,re.M|re.S)
allocs = ""

#print len(coreMap),coreMap
#print len(coreToJtag),coreToJtag
#sys.exit(0)

for x in m:
  replicator = x[0]
  allocator = x[1]

  istart = "i = 0"
  itest = "i < 1"
  istep = "i += 1"
  if replicator:
    m = re.search("\s*int\s*(.*?);(.*?);\s*(.*?)\)",replicator,re.M)
    istart,itest,istep = m.groups()

  toEval = re.findall("(\[(.*?i.*?)\])",allocator);


  exec(istart)
  while eval(itest):
    al = allocator
    for x in toEval:
      v = eval(x[1])
      al = al.replace(x[0],"["+str(v)+"]",1)
    allocs += re.sub("(?<!\w)i(?!\w)",str(i),al)
    exec(istep)

coreChanends = []
channelMappings = {}

allocs = [x.strip() for x in re.findall("\s*on\s+.*?;",allocs)]
for a in allocs:
  m = re.search("on stdcore\[(\d+)\]",a);
  core = int(m.group(1))
  for c in chans:
    #Find all instances of this channel as a channend
    m = re.findall("(?<!\w)(%s)(?!\w)(\s*\[(\d+)\])?" % c[0],a)
    #Fudge non-array entities
    for x in m:
      if x[2] == '':
        ref = x[0]+'0'
      else:
        ref = x[0]+x[2]
      #Make sure our channend counter is big enough for this core num
      if len(coreChanends) != core + 1:
        coreChanends.extend([0] * (core+1-len(coreChanends)))
      #Add references to this chanend
      if ref in channelMappings:
        channelMappings[ref]['cores'].append(core)
        channelMappings[ref]['chan'].append(coreChanends[core])
      else:
        channelMappings[ref] = {'cores':[core],'chan':[coreChanends[core]]}
      coreChanends[core] += 1


print "Chanends used per core (1 for sync) :",map(lambda(x): x + (x != 0),coreChanends)
#print "Channel mappings:",channelMappings

mains = {}
inits = {}

channelMappingsCopy = copy.deepcopy(channelMappings)

for a in allocs:
  #Simple search for "on stdcore" - only works with single-lines for now
  m = re.search("on stdcore\[(\d+)\]",a);
  core = int(m.group(1))
  m = re.search(":\s*(\w+)\s*\((.*)\)\s*;",a);
  fn = m.group(1)
  args = [x.strip() for x in m.group(2).split(",")]
  #Setup the channel layer
  if core in mains:
    mains[core] += "    " + fn + "("
  else:
    inits[core] = ""
    mains[core] = "    " + fn + "("
  for arg in args:
    if mains[core][-1] != '(':
        mains[core] += ','
    ref = re.sub("(\D)$","\g<1>0",re.sub("[\[\]]","",arg))
    if ref in channelMappings:
      cidx = channelMappings[ref]['cores'].index(core)
      dst = (channelMappings[ref]['cores'][cidx] << 16)  \
        | ((channelMappings[ref]['chan'][cidx] + 1) << 8) | 2;
      mains[core] += "swallow_cvt_chanend(0x%08x)" % dst
      del channelMappings[ref]['cores'][cidx],channelMappings[ref]['chan'][cidx]
    else:
      mains[core] += arg
  mains[core] += ");\n"
  
channelMappings = channelMappingsCopy

#print allocs
#sys.exit(0)

chans = {}
for x in channelMappings:
  for idx,y in enumerate(channelMappings[x]['cores']):
    if y not in chans:
      chans[y] = {}
    otheridx = 1-idx
    chans[y][channelMappings[x]['chan'][idx]] = (channelMappings[x]['cores'][otheridx] << 16)  \
        | ((channelMappings[x]['chan'][otheridx] + 1) << 8) | 2;

for x in chans:
  for y in sorted(chans[x]):
    inits[x] += """
  c = getChanend(swallow_cvt_chanend(""" + hex(chans[x][y]) + """));
  asm(\"ecallf %0\"::\"r\"(c));"""


for x in mains:
  inits[x] = initInitLinks(x) + inits[x] + endInitLinks(x)
  mains[x] = initMain(x) + mains[x] + endMain(x)

for x in mains:
  f = open(outdir + "scmain_" + str(x) + ".xc","w")
  print >> f,"/************* CORE " + str(x) + " ***************/"
  print >> f,inits[x]
  print >> f,mains[x]
  f.close()

print "Num cores in use:",str(len(mains))

build = ""

print "Now building..."

cmd = shlex.split("scmake-swallow.py " + outdir + " " + str(mains.keys())[1:-1].replace(' ',''));
cmd.extend(additional_args)
res = subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]
#print res

print "Done building!"


