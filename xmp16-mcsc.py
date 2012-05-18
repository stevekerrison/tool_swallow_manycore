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

# Use XCC's preprocessor
xc = subprocess.Popen(["xcc", "-E", sys.argv[1], "test.xn"], stdout=subprocess.PIPE).communicate()[0]
xc = re.sub("^#.*\n","",xc,0,re.M)

# Capture the main block
m = re.search("int\s*main\s*\(.*?\)\s*\{.*?return\s+0\s*;.*?}",xc,re.M|re.S)
xc = m.group(0)

def arrLen(s):
	if s == '':
		return 1;
	return int(s)

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
		#print a,c
		m = re.findall("(?<!\w)(%s)(?!\w)(\s*\[(\d+)\])?" % c[0],a)
		for x in m:
			if x[2] == '':
				ref = x[0]+'0'
			else:
				ref = x[0]+x[2]
			if len(coreChanends) != core + 1:
				coreChanends.extend([0] * (core+1-len(coreChanends)))
			if ref in channelMappings:
				channelMappings[ref]['cores'].append(core)
				channelMappings[ref]['chan'].append(coreChanends[core])
			else:
				channelMappings[ref] = {'cores':[core],'chan':[coreChanends[core]]}
			coreChanends[core] += 1


print "Chanends used per core:",coreChanends
print "Channel mappings:",channelMappings

mains = {}

for a in allocs:
	m = re.search("on stdcore\[(\d+)\]",a);
	core = int(m.group(1))
	m = re.search(":\s*(\w+)\s*\((.*)\)\s*;",a);
	fn = m.group(1)
	args = [x.strip() for x in m.group(2).split(",")]
	#
	if core in mains:
		mains[core] += fn + "("
	else:
		mains[core] = "/* Main for core " + str(core) + """*/
int main(void)
{
	par
	{
		""" + fn + "("
	for arg in args:
		if mains[core][-1] != '(':
				mains[core] += ','
		if re.sub("(\D)$","\g<1>0",re.sub("[\[\]]","",arg)) in channelMappings:
			dst = (channelMappings[ref]['cores'].pop() << 16)	\
				| (channelMappings[ref]['chan'].pop() << 8)	| 2;
			mains[core] += "0x%08x" % dst
		else:
			mains[core] += arg
	mains[core] += ");"

for x in mains:
	print mains[x] + "\n\t}\n\treturn 0;\n}"
