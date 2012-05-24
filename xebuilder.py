#!/usr/bin/python

# Copyright (c) 2012, Steve Kerrison, All rights reserved
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""xebuilder.py

Build an xe file from a collection of pre-constructed xe+elf sections

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 15th May 2012

Usage:
	xebuilder.py core0sec [coreNsec...] outfile.xe

Takes the section binaries (see https://github.com/stevekerrison/tool_xesection
for extracting ELFs including their XE section headers & checksums) and
builds a valid XE file from them.
"""

import sys

if len(sys.argv) < 3:
	print >> sys.stderr, "ERROR: Usage:",sys.argv[0],"core0sec [coreNsec...] outfile.xe"
	sys.exit(1)

out = open(sys.argv[-1],"wb")

out.write("XMOS\1\0\0\0")


for fn in sys.argv[1:-1]:
	f = open(fn,"rb")
	out.write(f.read())
	f.close()

for fn in sys.argv[1:-1]:
	out.write("\05\0\0\0\x14\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\x62\x10\xdd\x20")

out.write("\x55\x55\0\0\0\0\0\0\0\0\0\0");
