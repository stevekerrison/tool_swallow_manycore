#!/usr/bin/python

# Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
#
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""scmake-swallow.py

Parallel single-core builder culminating in a many-core XE - Swallow edition!

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 28th May 2012

Usage:
	scmake-swallow.py workdir coreA,coreB,...,coreXYZ [additional compiler parameters]

Compiles scmain_A.xc ... scmain_XYZ.xc and produces a many-core a.xe

Pass other files in the additional parameters bit
"""

import sys,os,re,subprocess,shlex,multiprocessing

if len(sys.argv) < 4:
	print >> sys.stderr, "ERROR: Usage:",os.path.basename(sys.argv[0]),"workdir commslib coreA,coreB,...,coreXYZ [additional compiler parameters]"
	sys.exit(1)
	
toolsdir = os.path.normpath(os.path.dirname((sys.argv[0])))
incdir = os.path.normpath(toolsdir + '/../include')
if not os.path.isdir(incdir):
  print >> sys.stderr, "ERROR: Incomplete installation - no include directory!"
  sys.exit(2)

scdir = os.path.normpath(sys.argv[2]) + '/'
if not os.path.isdir(scdir):
  print >> sys.stderr, scdir
  print >> sys.stderr, "ERROR: sc_swallow_communication not found!"
  sys.exit(2)

workdir = sys.argv[1]
os.chdir(workdir)


print "Now building..."
build = ""
#print >> sys.stderr, sys.argv
tasks = map(int,sys.argv[3].split(','))
cores = len(tasks)

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

extraargs = sys.argv[4:]

def compileXc(c):
	cmd = "xcc -o scmain_" + str(c) + ".xe scmain_" + str(c) + ".xc " + scdir + "swallow_comms.xc " + scdir + "swallow_comms.S " + scdir + "swallow_comms_c.c " + incdir + "/XMP16-unicore.xn -I" + scdir + " -fxscope -DCORE=" + str(c)
	ex = shlex.split(cmd)
	ex.extend(extraargs)
	print subprocess.Popen(ex, stdout=subprocess.PIPE).communicate()[0]
	

#Parallel build!!!
pool = multiprocessing.Pool(None)
r = pool.map_async(compileXc, tasks)
r.wait() # Wait on the results

files = ' '.join(map(lambda(x): 'scmain_' + str(x) + '.xe',tasks))
#print "sgb-builder.py " + str(cores) + " " + files + " " + outfile
res = subprocess.Popen(shlex.split("sgb-builder.py " + str(cores) + " " + files + " " + outfile), stdout=subprocess.PIPE).communicate()[0]
#print res

def cleanXc(c):
  cmd = "rm scmain_" + str(c) + ".xe scmain_" + str(c) + ".xc"
  ex = shlex.split(cmd)
  subprocess.Popen(ex, stdout=subprocess.PIPE).communicate()

pool = multiprocessing.Pool(None)	
r = pool.map_async(cleanXc, tasks)
r.wait() # Wait on the results

print "Done building!"
