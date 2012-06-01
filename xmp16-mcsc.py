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

import sys,os,re,subprocess,shlex,multiprocessing

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

zeroLeft = [0x87,0x85,0x86,0x84,0x82,0x83]
zeroRight = [0x87,0x85,0x86,0x84,0x82,0x83]
oneEven = [0x84,0x86,0x85,0x87,0x82,0x83]
oneOdd = [0x84,0x86,0x85,0x87,0x82,0x83]
#zeroLeft = [0x86,0x83,0x82]
#zeroRight = [0x86,0x82,0x83]
#oneEven = [0x85,0x83,0x82]
#oneOdd = [0x85,0x82,0x83]

#The order to bring links up in on the board.
linkOrder = [									\
	oneEven,zeroLeft,zeroRight,oneEven,			\
	oneOdd,zeroLeft,zeroRight,oneOdd,			\
	oneEven,zeroLeft,zeroRight,oneEven,			\
	oneOdd,zeroLeft,zeroRight,oneOdd			\
]

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
				if l[0] == '#':
					continue
				for x in [int(x,16) for x in l.split(" ")[1:]]:
					cfg[jtagid][x] = 0x80000000
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
	j = coreToJtag[core]
	debugstr = """	printf("%%d[%%d]:	%s 0x%%08x %s 0x%%02x\\n",myid,jtagid,%s,%s);\n"""
	wrstr = "	write_sswitch_reg_no_ack_clean(myid,0x%02x,0x%08x);\n"
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
	unsigned nlinks=""" + str(len(stw)) + """,tv,c, linksetting = 0xc0000800;
	timer t;
	unsigned links[""" + str(len(stw)) + """] = {"""
	for x in stw:
		ret += hex(x) + ","
	ret += """};
	ledOut(1);
	/* Set my core ID */
	write_sswitch_reg_no_ack_clean(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	cResetChans(myid);
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_clean(myid,i,0);
	}
	/* Enable all links */
	for (i = 0; i < nlinks; i += 1)
	{
		write_sswitch_reg_clean(myid,links[i],linksetting);
	}
	/* Give all other nodes a chance to activate their X-Links before we start
		splatting tokens around */
	t :> tv;
	t when timerafter(tv + 2000000) :> void;
	ledOut(3);
"""
		
	debug = False
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
	
	ret += """
	/* Issue hello and wait for credit on active links */
	for (i = 0; i < nlinks; i += 1)
	{
		if (links[i] & 1)
		{
			write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
			tv = 0;
			while((tv & 0x0e000000) != 0x06000000)
			{
				read_sswitch_reg(myid,links[i],tv);
			}
		}
		else
		{
			tv = 0;
			while((tv & 0x0e000000) != 0x04000000)
			{
				read_sswitch_reg(myid,links[i],tv);
			}
			write_sswitch_reg_clean(myid,links[i],linksetting | 0x01000000);
			tv = 0;
			while((tv & 0x0e000000) != 0x06000000)
			{
				read_sswitch_reg(myid,links[i],tv);
			}
		}
	}
	ledOut(7);
	/* Using the a sswitch register as scratch, pass a token around in a couple of
		directions until we achieve some semblance of syncronisation */
	for (i = 1; i < 3; i += 1)
	{
		if (myid == 0)
			write_sswitch_reg_clean(myid+1,0x3,i);
		tv = 0;
		while (tv != i)
		{
			read_sswitch_reg(myid,0x3,tv);
		}
		write_sswitch_reg_clean((myid+1)%"""+str(len(coreToJtag))+""",0x3,i);
	}
	for (i = 1; i < 3; i += 1)
	{
		if (myid == 0)
			write_sswitch_reg_clean((myid-1)%"""+str(len(coreToJtag))+""",0x3,i);
		tv = 0;
		while (tv != i)
		{
			read_sswitch_reg(myid,0x3,tv);
		}
		write_sswitch_reg_clean((myid-1)%"""+str(len(coreToJtag))+""",0x3,i);
	}
	t :> tv;
	t when timerafter(tv + 200000) :> void;
	/* Now we declare any channels we need */
"""
	return ret

def endInitLinks(core):
	return """
	ledOut(0xf);
	t :> tv;
	t when timerafter(tv + 200000) :> void;
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


print "Chanends used per core:",coreChanends
#print "Channel mappings:",channelMappings

mains = {}
inits = {}

for a in allocs:
	#Simple search for "on stdcore" - only works with single-lines for now
	m = re.search("on stdcore\[(\d+)\]",a);
	core = int(m.group(1))
	m = re.search(":\s*(\w+)\s*\((.*)\)\s*;",a);
	fn = m.group(1)
	args = [x.strip() for x in m.group(2).split(",")]
	#Setup the channel layer
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
			cidx = channelMappings[ref]['cores'].index(core)
			dst = (channelMappings[ref]['cores'][cidx] << 16)	\
				| (channelMappings[ref]['chan'][cidx] << 8) | 2;
			mains[core] += "0x%08x" % dst
		else:
			mains[core] += arg
	mains[core] += ");\n"

chans = {}
for x in channelMappings:
	for idx,y in enumerate(channelMappings[x]['cores']):
		if y not in chans:
			chans[y] = {}
		otheridx = 1-idx
		chans[y][channelMappings[x]['chan'][idx]] = (channelMappings[x]['cores'][otheridx] << 16)	\
				| (channelMappings[x]['chan'][otheridx] << 8) | 2;

for x in chans:
	for y in sorted(chans[x]):
		inits[x] += """
	getChanend(""" + hex(chans[x][y]) + ");"


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
	print >> f,initMain(x[0]) + "		asm(\"freet\"::);\n" + endMain(x[0])
	f.close()

build = ""

print "Now building..."

subprocess.Popen(shlex.split("scmake.py " + outdir + " " + str(len(coreToJtag)) + " -O2 ledtest.xc chan.S chan_c.c"), stdout=subprocess.PIPE).communicate()[0]

print "Done building!"


