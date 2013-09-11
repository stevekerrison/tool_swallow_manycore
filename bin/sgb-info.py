#!/usr/bin/python

# Copyright (c) 2013, Steve Kerrison, All rights reserved
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

header = \
"""sgb-info.py

Dump info on a Swallow Grid Binary (SGB) file

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 11th Sept 2013

Usage:
	sgb-info.py file.sgb
"""

import sys,os,re,struct,binascii

if len(sys.argv) < 1:
	print >> sys.stderr, "ERROR: Usage:",os.path.basename(sys.argv[0]),"file.sgb"
	sys.exit(1)

f = open(sys.argv[-1],"rb")
s = f.read()
f.close()

print """
Header
------"""
hdr = struct.unpack('<B',s[0])[0]
print "Magic number: {:02x}".format(hdr)

if hdr is not 0x5b:
  print >> sys.stderr, "Not an SGB header!"

print "SGB version: {:02x}".format(struct.unpack('<B',s[1])[0])

print """
Config
------"""
resetbit = struct.unpack('<B',s[2])[0]
if resetbit is 0: doreset = "No"
else: doreset = "Yes"
print "Perform grid reset: {}".format(doreset)
print "Number of images: {}".format(struct.unpack('<H',s[3:5])[0])
print "PLL data: {}".format(struct.unpack('<B',s[5])[0])

idx = 6
print """
Images
------"""
offset = struct.unpack('<I',s[idx:idx+4])[0]
while offset is not 0xffffffff and offset < len(s):
  print "Core: {}".format(offset)
  length = struct.unpack('<I',s[idx+4:idx+8])[0] * 4
  print "Length: {}".format(length)
  idx += length+8
  offset = struct.unpack('<I',s[idx:idx+4])[0]
  
if idx > len(s) or offset != 0xffffffff:
  print >> sys.stderr, "Tail not found - image offsets/lengths invalid?"
  sys.exit(1)

