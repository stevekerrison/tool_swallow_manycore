#!/usr/bin/python

import binascii, sys

if len(sys.argv) != 2:
	sys.exit

f = open(sys.argv[1],'rb')

data = f.read();

data = "\5\0\0\0\x14\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"
crc = 0x6210DD20

print hex(binascii.crc32(data,0xffffffff) & 0xffffffff)
print hex(~(binascii.crc32(data,0xffffffff)) & 0xffffffff)
print hex((binascii.crc32(data,0xffffffff) ^ 0xffffffff) & 0xffffffff)
print hex(binascii.crc32(data) & 0xffffffff)
print hex(~(binascii.crc32(data)) & 0xffffffff)
