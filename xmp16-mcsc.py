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
	xmp16-mcsc.py mcmain.xe boardconfig.brd [outputdir]

Takes a multi-core main, tries to parse it and produce a set of single-core
binaries that can be processed using the routing tables provided in boardconfig.
If an outputdir is not specified, $PWD is used.
"""

import sys,os,re,subprocess,shlex

if len(sys.argv) < 3:
	print >> sys.stderr, "ERROR: Usage:",sys.argv[0],"mcmain.xe boardconfig.brd [outputdir]"
	sys.exit(1)

pwd = os.getcwd()

if len(sys.argv) == 4:
	outdir = sys.argv[3] + "/"
else:
	outdir = pwd + "/"

includes = re.findall("^(.*#.*)$",open(sys.argv[1],"r").read(),re.M)

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
					cfg[jtagid][x] = 0xc0000000
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
	ret = ""
	for i in includes:
		ret += i + "\n"
	ret += """#include <stdio.h>

/* __initLinks for core """ + str(core) + """*/
void __initLinks()
{
	unsigned myid = """ + str(core) + """, jtagid= """ + str(coreToJtag[core]) + """,i,tv,c;
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
	j = coreToJtag[core]
	debugstr = """	printf("%%d[%%d]:	%s 0x%%08x %s 0x%%02x\\n",myid,jtagid,%s,%s);\n"""
	wrstr = "	write_sswitch_reg_no_ack(myid,0x%02x,0x%08x);\n"
	stw = [k for k in bc[j] if k in range(0x84,0x88)]
	dn = [k for k in bc[j] if k in range(0x20,0x28)]
	rt = [k for k in bc[j] if k in range(0xc,0xe)]
	#ret += """	printf("Hai I'm core %d\\n",myid);return;\n"""
	debug = True
	ret += "	//Link enabling\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r])
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
	ret += "	//Route configuration\n"
	for r in rt:
		ret += wrstr % (r,bc[j][r])
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
	ret += "	//Attach links to routes\n"
	for r in dn:
		ret += wrstr % (r,bc[j][r])
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
	ret += "	//Issue HELLO on active links\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r] | 0x01000000)
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r] | 0x01000000),hex(r))
	ret += "	//Wait for credit\n"
	chkstr = """	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x%02x,0x%08x);
		}
		read_sswitch_reg(myid,0x%02x,tv);
	}
"""
	for r in stw:
		ret += chkstr % (r,bc[j][r],r)
		if debug:
			ret += debugstr % ("Read","from","tv",hex(r))
			ret += """	printf("%d[%d]:	Got initial credits for %02x after %d attempts\\n",myid,jtagid,""" + hex(r) + """,i);\n"""
	ret += "	//Reissue HELLOs\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r] | 0x01000000)
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r] | 0x01000000),hex(r))
	#Do off-chip links separately for now
	stw = [k for k in bc[j] if k in range(0x82,0x84)]
	ret += "	//Link enabling\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r])
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r]),hex(r))
	ret += "	//Issue HELLO on active links\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r] | 0x01000000)
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r] | 0x01000000),hex(r))
	ret += "	//Wait for credit\n"
	chkstr = """	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x%02x,0x%08x);
		}
		read_sswitch_reg(myid,0x%02x,tv);
	}
"""
	for r in stw:
		ret += chkstr % (r,bc[j][r],r)
		if debug:
			ret += debugstr % ("Read","from","tv",hex(r))
			ret += """	printf("%d[%d]:	Got initial credits for %02x after %d attempts\\n",myid,jtagid,""" + hex(r) + """,i);\n"""
	ret += "	//Reissue HELLOs\n"
	for r in stw:
		ret += wrstr % (r,bc[j][r] | 0x01000000)
		if debug:
			ret += debugstr % ("Written","to",hex(bc[j][r] | 0x01000000),hex(r))
	ret += "	//Hopefully we're done!\n"
	ret += "	cResetChans(myid);\n"
	if debug:
		ret += """	printf("%d[%d]:	Done link initialisation!\\n",myid,jtagid);\n"""
	return ret

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
		mains[core] += "		" + fn + "("
	else:
		inits[core] = ""
		mains[core] = "		" + fn + "("
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
	mains[core] += ");\n"

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
print "Unused cores (Node,JTAG) :",unused
for x in unused:
	f = open(outdir + "scmain_" + str(x[1]) + ".xc","w")
	print >> f,"/************* UNUSED CORE " + str(x[0]) + "***************/"
	print >> f,initInitLinks(x[0]),endInitLinks(x[0])
	print >> f,initMain(x[0]) + "		asm(\"freet\"::);\n" + endMain(x[0])
	f.close()

build = ""

print "Now building..."
i = 1
ilim = len(coreToJtag)
for c in coreToJtag.items():
	cmd = "xcc -o" + outdir + "scmain_" + str(c[1]) + ".xe " + outdir + "scmain_" + str(c[1]) + ".xc ledtest.xc chan.S chan_c.c -target=XK-1"
	print "\r%0.2f%%" % ((float(i)/ilim)*100),
	i += 1
	sys.stdout.flush()
	subprocess.Popen(shlex.split(cmd), stdout=subprocess.PIPE).communicate()
	sec = subprocess.Popen(shlex.split("xesection " + outdir + "scmain_" + str(c[1]) + ".xe 1"), stdout=subprocess.PIPE).communicate()[0]
	f = open(outdir + str(c[1]) + ".sec","w")
	build += " " + outdir + str(c[1]) + ".sec"
	f.write(sec)
	f.close()

print "\nDone building!"

subprocess.Popen(shlex.split("xebuilder.py " + build + " " + outdir + "a.xe"), stdout=subprocess.PIPE).communicate()[0]
