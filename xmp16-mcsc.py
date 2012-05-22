#!/usr/bin/python

# Copyright (c) 2012, Steve Kerrison, All rights reserved
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""xmp16-mcsc.py

Take a multi-core main input and produce per-core binaries for compilation

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 18th May 2012

Usage:
	xmp16-mcsc.py mcmain.xe boardconfig.dat [outputdir]

Takes a multi-core main, tries to parse it and produce a set of single-core
binaries that can be processed using the routing tables provided in boardconfig.
If an outputdir is not specified, $PWD is used.
"""

import sys,re,subprocess

if len(sys.argv) < 3:
	print >> sys.stderr, "ERROR: Usage:",sys.argv[0],"mcmain.xe boardconfig.dat [outputdir]"
	sys.exit(1)

# Use XCC's preprocessor to get the code
xc = subprocess.Popen(["xcc", "-E", sys.argv[1], "test.xn"], stdout=subprocess.PIPE).communicate()[0]
xc = re.sub("^#.*\n","",xc,0,re.M)

# Capture the main block
m = re.search("int\s*main\s*\(.*?\)\s*\{.*?return\s+0\s*;.*?}",xc,re.M|re.S)
xc = m.group(0)

coreToJtag = {}

#Fudge all channel declarations into arrays
def arrLen(s):
	if s == '':
		return 1;
	return int(s)

#Returns a board config list, indexed by JTAG ID
def parseBoardConfig(bc):
	cfg = {}
	global coreToJtag
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
				for x in [int(x,16) for x in l.split(" ")[1:]]:
					cfg[jtagid][x] = 0x80001002
		coreToJtag[cfg[jtagid][5]] = jtagid
	return cfg

bc = parseBoardConfig(open(sys.argv[2],"r").read())

def initMain(core):
	return "\n/* Main for core " + str(core) + """*/
int main(void)
{
	__initLinks();
	par
	{
		"""

def endMain(core):
	return """
	}
	return 0;
}"""

def initInitLinks(core):
	return """
#include <platform.h>
#include <xs1.h>
#include "chan.h"

/* __initLinks for core """ + str(core) + """*/
void __initLinks()
{
	unsigned myid = """ + str(core) + """, i,tv,c;
	/* Set my core ID */
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	resetChans();
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0);
	}
	/* Now allocate the channels needed by this core, setup the links and
		routing tables */
	"""
	#TODO: What he said ^^^

def endInitLinks(core):
	return """
	return;
}"""
	
	

# This function contains all the reasons that I love Python
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

m = re.search("par(\s+\(.*\))?\s*\{(.*)\}\s+return",xc,re.M|re.S)
replicator = m.group(1)
allocator = m.group(2)

istart = "i = 0"
itest = "i < 1"
istep = "i += 1"
if replicator:
	m = re.search("\s*int\s*(.*?);(.*?);\s*(.*?)\)",replicator,re.M)
	istart,itest,istep = m.groups()

allocs = ""

exec(istart)
while eval(itest):
	allocs += re.sub("(?<!\w)i(?!\w)",str(i),allocator)
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


print "Chanends used per core:",coreChanends
print "Channel mappings:",channelMappings

mains = {}
inits = {}

for a in allocs:
	#Simple search for "on stdcore" - only works with single-lines for now
	m = re.search("on stdcore\[(\d+)\]",a);
	core = int(m.group(1))
	m = re.search(":\s*(\w+)\s*\((.*)\)\s*;",a);
	fn = m.group(1)
	args = [x.strip() for x in m.group(2).split(",")]
	#Create a new function that passes encoded channel mappings to functions
	#encoded as:
	#0:4 - Local resource ID
	#5:9 - Remote resource ID
	#16:31 - Remote node ID
	#Construct a valid resource identifier and do a SETD
	if core in mains:
		mains[core] += fn + "("
	else:
		inits[core] = ""
		mains[core] = fn + "("
	for arg in args:
		if mains[core][-1] != '(':
				mains[core] += ','
		ref = re.sub("(\D)$","\g<1>0",re.sub("[\[\]]","",arg))
		if ref in channelMappings:
			dst = (channelMappings[ref]['cores'].pop(0) << 16)	\
				| (channelMappings[ref]['chan'].pop(0) << 8) | 2;
			mains[core] += "0x%08x" % dst
		else:
			mains[core] += arg
	mains[core] += ");"

for x in mains:
	inits[x] = initInitLinks(x) + inits[x] + endInitLinks(x)
	mains[x] = initMain(x) + mains[x] + endMain(x)

for x in mains:
	print "/************* CORE " + str(x) + " ***************/"
	print inits[x]
	print mains[x]

print coreToJtag
