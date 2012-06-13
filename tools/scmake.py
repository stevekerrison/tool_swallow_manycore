#!/usr/bin/python

# Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
#
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""scmake.py

Parallel single-core builder culminating in a many-core XE

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 28th May 2012

Usage:
	scmake.py workdir numcores [additional compiler parameters]

Compiles scmain_0.xc ... scmain_N.xc and produces a many-core a.xe

Pass other files in the additional parameters bit
"""

import sys,os,re,subprocess,shlex,multiprocessing

if len(sys.argv) < 3:
	print >> sys.stderr, "ERROR: Usage:",sys.argv[0],"workdir numcores [additional compiler parameters]"
	sys.exit(1)

workdir = sys.argv[1]
os.chdir(workdir)

print "Now building..."
build = ""
ilim = int(sys.argv[2])


o = filter(lambda(x): re.match("-o",x),sys.argv)[:1]
if len(o) > 0:
	if o[0] == "-o":
		idx = sys.argv.index("-o")+1
		outfile = sys.argv[idx]
		del sys.argv[idx-1:idx+1]
	else:
		outfile = o[0][2:]
		sys.argv.delete("-o")
else:
	outfile = "a.xe"

extraargs = sys.argv[3:]

def compileXc(c):
	cmd = "xcc -o scmain_" + str(c) + ".xe scmain_" + str(c) + ".xc XMP16-unicore.xn"
	ex = shlex.split(cmd)
	ex.extend(extraargs)
	subprocess.Popen(ex, stdout=subprocess.PIPE).communicate()
	

#Parallel build!!!
pool = multiprocessing.Pool(None)
tasks = range(ilim)
r = pool.map_async(compileXc, tasks)
r.wait() # Wait on the results

for c in range(ilim):
	sec = subprocess.Popen(shlex.split("xesection scmain_" + str(c) + ".xe 1"), stdout=subprocess.PIPE).communicate()[0]
	f = open(str(c) + ".sec","w")
	build += " " + str(c) + ".sec"
	f.write(sec)
	f.close()


print "Done building!"

subprocess.Popen(shlex.split("xebuilder.py " + build + " " + outfile), stdout=subprocess.PIPE).communicate()[0]
