#!/usr/bin/python

# Copyright (c) 2013, Steve Kerrison, All rights reserved
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""sgb-builder.py

Build an sgb file from a collection of pre-constructed xe+elf sections

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 1st March 2013

Usage:
	sgb-builder.py ncores scmain_A.xe scmain_B.xe ... scmain_XYZ.xe outfile.xe

Requires xobjdump from XDE/xTimeComposer and objcopy from standard GNU binutils
"""

import sys,os,re,tempfile,subprocess,shlex,shutil,struct

if len(sys.argv) < 3:
	print >> sys.stderr, "ERROR: Usage:",os.path.basename(sys.argv[0]),"ncores scmain_A.xe scmain_B.xe ... scmain_XYZ.xe outfile.xe"
	sys.exit(1)

out = open(sys.argv[-1],"wb")
ncores = int(sys.argv[1])

out.write("\x5b\0\1")
out.write(struct.pack('<H',ncores))
out.write("\0")

td = tempfile.mkdtemp('sgb')
for fn in sys.argv[2:-1]:
  shutil.rmtree(td + '/*',True)
  cid = int(re.search(r'_(\d+)\.xe',fn).group(1))
  subprocess.Popen(shlex.split("xobjdump -s --split-dir " + td + " " + fn), stdout=subprocess.PIPE).communicate()[0]
  subprocess.Popen(shlex.split("objcopy -Ielf32-little -Obinary " + td + "/image_n0c0_2.elf " + td + "/image.bin"), stdout=subprocess.PIPE).communicate()[0]
  out.write(struct.pack('<I',cid))
  print os.path.getsize(td + '/image.bin')/4
  out.write(struct.pack('<I',os.path.getsize(td + '/image.bin')/4))
  f = open(td + '/image.bin','rb')
  out.write(f.read())
  f.close()
  
out.wrire(struct.pack('<I',0xffffffff))
out.close()
	
shutil.rmtree(td)
