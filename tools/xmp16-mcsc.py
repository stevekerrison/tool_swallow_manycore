#!/usr/bin/python

# Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
#
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>


header = \
"""xmp16-mcsc.py

Take a multi-core main input and produce per-core binaries for compilation

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 18th May 2012

Usage:
  xmp16-mcsc.py mcmain.xc boardconfig.brd [extra options]

Takes a multi-core main, tries to parse it and produce a set of single-core
binaries that can be processed using the routing tables provided in boardconfig.
Operates within $PWD
"""

import sys,os,re,subprocess,shlex,multiprocessing,math

if len(sys.argv) < 3:
  print >> sys.stderr, "ERROR: Usage:",sys.argv[0],"mcmain.xe boardconfig.brd [outputdir]"
  sys.exit(1)

pwd = os.getcwd()

outdir = pwd + "/"

additional_args = sys.argv[3:]

includes = re.findall("^(.*#.*)$",open(sys.argv[1],"r").read(),re.M)

# Use XCC's preprocessor to get the code
xc = subprocess.Popen(["xcc", "-E", sys.argv[1], "manycore.xn"], stdout=subprocess.PIPE).communicate()[0]
xc = re.sub("^#.*\n","",xc,0,re.M)

# Capture the main block
m = re.search("int\s*main\s*\(.*?\)\s*\{.*?return\s+0\s*;.*?}",xc,re.M|re.S)
xc = m.group(0)

coreToJtag = {}

zeroLeft = [0x87,0x85,0x86,0x84,0x83,0x82]
zeroRight = [0x87,0x85,0x86,0x84,0x82,0x83]
oneEven = [0x84,0x86,0x85,0x87,0x82,0x83]
oneOdd = [0x84,0x86,0x85,0x87,0x82,0x83]

#The order to bring links up in on the board.
linkOrder = [                  \
  oneEven,zeroLeft,zeroRight,oneEven,      \
  oneOdd,zeroLeft,zeroRight,oneOdd,      \
  oneEven,zeroLeft,zeroRight,oneEven,      \
  oneOdd,zeroLeft,zeroRight,oneOdd      \
]

#Locical cores to actual node IDs
coreMap = []

#Fudge all channel declarations into arrays
def arrLen(s):
  if s == '':
    return 1;
  return int(s)

#Returns a board config list, indexed by JTAG ID
def parseBoardConfig(bc):
  cfg = {}
  global coreToJtag
  global coreMap
  dims = bc.splitlines()[0]
  m = re.match("^DIM\s*=\s*([0-9]+)\(([0-9]+)\)x([0-9]+)\(([0-9]+)\)",dims)
  if not m:
    print >> sys.stderr, "WARNING: Dimension data not found. Config compatibility degraded"
    dims = None
  else:
    dims = [(int(m.group(1)),int(m.group(2))),(int(m.group(3)),int(m.group(4)))]
  percore = [filter(None,x.splitlines()) for x in bc.split("JTAG Node")]
  pattern = "^(0x[0-9a-f]+)\s*=\s*(0x[0-9a-f]+)"
  for c in percore[1:]:
    jtagid = int(re.search("^ = (\d+)$",c[0]).group(1))
    cfg[jtagid] = {}
    for l in c[1:]:
      m = re.match(pattern,l)
      if m:
        cfg[jtagid][int(m.group(1),16)] = int(m.group(2),16)
      else:
        if l[0] == '#':
          continue
        for x in [int(x,16) for x in l.split(" ")[1:]]:
          cfg[jtagid][x] = 0x80000000
    coreToJtag[cfg[jtagid][5]] = jtagid
    #print "adding JTAG ID",jtagid,"to",cfg[jtagid][5]
  #Default is direct mapping, for dimensions that fit perfectly the number of address bits, or are simple 2D
  coreMap = range(len(coreToJtag))
  #If we have a 3D system and will generate Node ID holes vertically, we need to do more work on the map!
  if dims and dims[1][0] > 1 and math.log(dims[1][0])/math.log(2.0) != float(dims[1][1]):
    modpoint = 4 * dims[1][0]
    offset = 0
    stepover = ((2**dims[1][1])-(dims[1][0])) * 4
    for i in range(len(coreToJtag)):
      coreMap[i] = offset
      if i > 0 and (i+1) % modpoint == 0:
        offset += stepover+1
      else:
        offset += 1
  coreMap = [c for d in [b[0:2]+[b[3]]+[b[2]] for b in [list(a) for a in zip(*[iter(coreMap)]*4)]] for c in d]
  return cfg

bc = parseBoardConfig(open(sys.argv[2],"r").read())

def initMain(core):
  return "\n/* Main for core " + str(core) + """*/
int main(void)
{
  unsigned ctrl_data; //Used by AEC code, maybe
  __initLinks();
//Enable dynamic AEC if we want AEC enabled even on cores that are in use
#ifdef AEC_ON_INUSE_CORE
#if AEC_DIVIDER_""" + str(core) + """ > 1
  write_pswitch_reg(""" + str(core) + """,XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER_""" + str(core) + """ - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#elif AEC_DIVIDER > 1
  write_pswitch_reg(""" + str(core) + """,XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER - 1);
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
  write_pswitch_reg(""" + str(core) + """,XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER_""" + str(core) + """ - 1);
  ctrl_data = getps(XS1_PS_XCORE_CTRL0);
  ctrl_data |= 0x30;
  setps(XS1_PS_XCORE_CTRL0, ctrl_data);
#elif AEC_DIVIDER > 1
  write_pswitch_reg(""" + str(core) + """,XS1_PSWITCH_PLL_CLK_DIVIDER_NUM,AEC_DIVIDER - 1);
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
  j = coreToJtag[core]
  debugstr = """  printf("%%d[%%d]:  %s 0x%%08x %s 0x%%02x\\n",myid,jtagid,%s,%s);\n"""
  wrstr = "  write_sswitch_reg_no_ack_clean(myid,0x%02x,0x%08x);\n"
  dn = [k for k in bc[j] if k in range(0x20,0x28)]
  rt = [k for k in bc[j] if k in range(0x8,0xe)]
  #stw = [k for k in bc[j] if k in range(0x82,0x88)]
  stw = [l for l in linkOrder[core%16] if l in [k for k in bc[j] if k in range(0x82,0x88)]]
  
  for i in includes:
    ret += i + "\n"
  ret += """#include <stdio.h>

/* __initLinks for core """ + str(core) + """*/
void __initLinks()
{
  unsigned myid = """ + str(core) + """, jtagid= """ + str(coreToJtag[core]) + """, i;
  unsigned nlinks=""" + str(len(stw)) + """,tv,c,d, linksetting = 0xc0001002;
  unsigned waittime = 20000000;
  timer t;
  unsigned links[""" + str(len(stw)) + """] = {"""
  for x in stw:
    ret += hex(x) + ","
  ret += """};
  /* Make sure scratch register is clear */
  write_sswitch_reg_no_ack_clean(0,0x3,0);
  /* Set my core ID */
  write_sswitch_reg_no_ack_clean(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
  /* Zero out the link registers */
  for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
  {
    write_sswitch_reg_clean(myid,i,0);
  }
  /* Enable local links on the chip, between cores */
  for (i = 0x84; i < 0x88; i += 1)
  {
    write_sswitch_reg_clean(myid,i,linksetting);
  }
"""
    
  debug = False
  ret += "  //Route configuration\n"
  for r in rt:
    ret += wrstr % (r,bc[j][r])
    if debug:
      ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
  ret += "  //Attach links to routes\n"
  for r in dn:
    ret += wrstr % (r,bc[j][r])
    if debug:
      ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
  if j == 0:
    ret += """
  /* XSCOPE */
  read_sswitch_reg(myid,0xd,tv);
  write_sswitch_reg_no_ack_clean(myid,0x0d,tv | 0xf0000000);
  write_sswitch_reg_clean(myid,0x22,0xf00);
  write_sswitch_reg_clean(myid,0x82,0x81000800);"""
  
  ret += """
  /* Give neighbouring core a chance to wake up */
  t :> tv;
  t when timerafter(tv + waittime) :> void;
  for (i = 0; i < 4; i += 1)
  {
    if (links[i] & 1)
    {
      write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
      tv = 0;
      c = 0;
      while((tv & 0x0e000000) != 0x06000000)
      {
        read_sswitch_reg(myid,links[i],tv);
        if (tv & 0x08000000)
        {
          asm("ecallt %0"::"r"(tv));
        }
      }
    }
    else
    {
      tv = 0;
      c = 0;
      while((tv & 0x0e000000) != 0x04000000)
      {
        read_sswitch_reg(myid,links[i],tv);
        if (tv & 0x08000000)
        {
          asm("ecallt %0"::"r"(tv));
        }
      }
      write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
      tv = 0;
      while((tv & 0x0e000000) != 0x06000000)
      {
        read_sswitch_reg(myid,links[i],tv);
      }
    }
  }
  ledOut(1);
  if (myid & 1)
  {
    read_sswitch_reg(myid-1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
    if (tv != myid-1)
    {
      //Uh-oh!
      asm("ecallt %0"::"r"(1));
    }
  }
  else
  {
    read_sswitch_reg(myid+1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
    if (tv != myid+1)
    {
      //Uh-oh!
      asm("ecallt %0"::"r"(1));
    }
  }
  ledOut(3);
  /* Enable all other links */
  for (i = 4; i < nlinks; i += 1)
  {
    write_sswitch_reg_clean(myid,links[i],linksetting);
  }
  /* Give all other nodes a chance to activate their X-Links before we start
    splatting tokens around */
  t :> tv;
  t when timerafter(tv + waittime) :> void;
  ledOut(7);
  /* Issue hello and wait for credit on active links */
  for (i = 4; i < nlinks; i += 1)
  {
    if (links[i] & 1)
    {
      write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
      tv = 0;
      c = 0;
      while((tv & 0x0e000000) != 0x06000000)
      {
        read_sswitch_reg(myid,links[i],tv);
        if (tv & 0x08000000)
        {
          asm("ecallt %0"::"r"(tv));
        }
      }
    }
    else
    {
      tv = 0;
      c = 0;
      while((tv & 0x0e000000) != 0x04000000)
      {
        read_sswitch_reg(myid,links[i],tv);
        if (tv & 0x08000000)
        {
          asm("ecallt %0"::"r"(tv));
        }
        /*if (tv & 0x08000000)
        {
          printf("Link error on %d[%x]\\n",myid,links[i]);
          write_sswitch_reg_clean(myid,links[i],linksetting | 0x00800000);
        }*/
      }
      write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
      tv = 0;
      while((tv & 0x0e000000) != 0x06000000)
      {
        read_sswitch_reg(myid,links[i],tv);
      }
    }
  }
  ledOut(0xf);"""
  if (core == 0):
    ret += """
  for (i = 1; i < """ + str(len(coreToJtag)) + """; i += 1)
  {
    write_sswitch_reg_clean(coreMap[i],0x3,1);
    tv = 0;
    while (tv != coreMap[i])
    {
      read_sswitch_reg(0,0x3,tv);
    }
  }
  ledOut(0xe);
  write_sswitch_reg_clean(0,0x3,""" + str(max(coreMap)) + """);
    """
  else:
    ret += """
  tv = 0;
  while(tv != 1)
  {
    read_sswitch_reg(myid,0x3,tv);
  }
  write_sswitch_reg_clean(0,0x3,myid);
  ledOut(0xe);
  while(tv != """ + str(max(coreMap)) + """)
  {
    read_sswitch_reg(0,0x3,tv);
  }
    """
  ret += """
  ledOut(0xc);
  t :> tv;
  t when timerafter(tv + waittime) :> void;
"""
  ret += """  
  /* Now we declare any channels we need */
"""
  return ret

def endInitLinks(core):
  return """
  ledOut(0x8);
  t :> tv;
  t when timerafter(tv + waittime) :> void;
  ledOut(0x0);
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
  core = coreMap[int(m.group(1))]
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


print "Chanends used per core:",coreChanends
#print "Channel mappings:",channelMappings

mains = {}
inits = {}

for a in allocs:
  #Simple search for "on stdcore" - only works with single-lines for now
  m = re.search("on stdcore\[(\d+)\]",a);
  core = coreMap[int(m.group(1))]
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
        | (channelMappings[ref]['chan'][cidx] << 8) | 2;
      mains[core] += "0x%08x" % dst
    else:
      mains[core] += arg
  mains[core] += ");\n"

#print allocs
#sys.exit(0)

chans = {}
for x in channelMappings:
  for idx,y in enumerate(channelMappings[x]['cores']):
    if y not in chans:
      chans[y] = {}
    otheridx = 1-idx
    chans[y][channelMappings[x]['chan'][idx]] = (channelMappings[x]['cores'][otheridx] << 16)  \
        | (channelMappings[x]['chan'][otheridx] << 8) | 2;

for x in chans:
  for y in sorted(chans[x]):
    inits[x] += """
  c = getChanend(""" + hex(chans[x][y]) + """);
  asm(\"ecallf %0\"::\"r\"(c));
  //t :> tv;
  //t when timerafter(tv + waittime) :> void;
  //printf("%02x: %08x\\n",myid,getRemoteChanendId(c));
  //asm("outct res[%0],2"::"r"(c));"""


for x in mains:
  inits[x] = initInitLinks(x) + inits[x] + endInitLinks(x)
  mains[x] = initMain(x) + mains[x] + endMain(x)

for x in mains:
  f = open(outdir + "scmain_" + str(coreToJtag[x]) + ".xc","w")
  print >> f,"/************* CORE " + str(x) + " ***************/"
  print >> f,inits[x]
  print >> f,mains[x]
  f.close()

print "Total available cores:",str(len(coreToJtag))
print "Num cores in use:",str(len(mains))

unused = [(x,coreToJtag[x]) for x in coreToJtag if x not in mains]
#print "Unused cores (Node,JTAG) :",unused
for x in unused:
  f = open(outdir + "scmain_" + str(x[1]) + ".xc","w")
  print >> f,"/************* UNUSED CORE " + str(x[0]) + "***************/"
  print >> f,initInitLinks(x[0]),endInitLinks(x[0])
  print >> f,initMain(x[0]) + "    asm(\"freet\"::);\n" + endMain(x[0])
  f.close()

build = ""

print "Now building..."

cmd = shlex.split("scmake.py " + outdir + " " + str(len(coreToJtag)));
cmd.extend(additional_args)
cmd.extend(["-DCOREMAP=" + ','.join(map(str,coreMap)) + "," + str(len(coreToJtag))])
subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0]

print "Done building!"


