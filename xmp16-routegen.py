#!/usr/bin/python

header = \
"""xmp16-routegen.py

A script for generating routing tables, link settings and JTAG mappings for the
XMP16 UoB development board.

Author: Steve Kerrison <steve.kerrison@bristol.ac.uk>
Created: 11th May 2012

Accepts one argument in the form of a matlab-style matrix definition, where a
'1' signifies a board and a '0' does not. From this the network dimensions are
calculated. This is currently a redundant format due to it only supporting
rectangular board arrangements! Maybe in the future it'll be more flexible, but
it's not likely to need it in the mean time.

If "M" is specified as an additional argument, an L1 memory board is added to
the right of the top row of boards.

Example for a 2x2 mesh of boards: ./xmp16-routegen.py "1 1; 1 1"
Example for a 2x3 mesh of boards: ./xmp16-routegen.py "1 1 1;1 1 1" M
"""
import sys,math

if len(sys.argv) != 2 and len(sys.argv) != 3:
	print >> sys.stderr, header
	sys.exit(1)

#Description of a single board's JTAG map
jtagmap = [ 		\
	3, 2, 4, 5, 	\
	1, 0, 6, 7, 	\
	15, 14, 8, 9, 	\
	13, 12, 10, 11	\
]
#How the board's JTAG quadrants are broken down
nodequadrants = [	\
	0, 0, 1, 1,		\
	0, 0, 1, 1,		\
	3, 3, 2, 2,		\
	3, 3, 2, 2
]

dirmap = { 			\
	'left':0,'right':1, 	\
	'up':2,'down':3,	\
	'away':4,'towards':5	\
}

linkmap = [ 						\
	{'a':'up','b':'down','efgh':'right'}, 		\
	{'a':'towards','b':'right','efgh':'left'}, 	\
	{'a':'left','b':'away','efgh':'right'}, 	\
	{'a':'up','b':'down','efgh':'left'}  		\
]

linkregs = { 'a':0x22,'b':0x23,'c':0x20,'d':0x21, \
	'e':0x26,'f':0x27,'g':0x24,'h':0x25 }

nodereg = 0x05
networkpos = 4
networkwidth = 2
dirwidth = 4
dirpos = 8 #In the link control register
dirreg = 0x0c

xmap = [['right','left'],['right','left'],['right','left'],['right','left']]
ymap = [['down','up'],['left','left'],['right','right'],['down','up']]
zmap = [['right','right'],['right','towards'],['away','left'],['left','left']]

rawconfig = sys.argv[1]
M = len(sys.argv) == 3 and sys.argv[2] == "M"

configrows = rawconfig.split(';')
config = []
for x in configrows:
	config.append(map(int,x.strip().split(' ')))

#print config

#Boards are 4x4 nodes
xboardnodes = 4
yboardnodes = 4
boardnodes = xboardnodes * yboardnodes

xmemboard = int(M)

xboards = len(config[0])
yboards = len(config)

xbits = int(math.ceil(math.log(xboardnodes)/math.log(2)))
yboardbits = int(math.ceil(math.log(yboardnodes)/math.log(2)))
ybits = int(math.ceil(math.log(yboards)/math.log(2)))
zbits = int(math.ceil(math.log(xboards+xmemboard)/math.log(2)))
boardbits = xbits + yboardbits
totalbits = boardbits+ybits+zbits

#print xbits,yboardbits
#print ybits,zbits

def calcdirs(lst,data,width,dirs):
	for b in range(width):
		lst.append(dirs[(data >> b) & 1])

def calcjtag(y,z,c):
	n = nodequadrants[c]
	if n == 0:
		if y == 0 and z == 0:
			blocksbefore = 0
		elif z == 0:
			blocksbefore = (2*yboards*(((xboards-1)*2)+1)) + ((yboards-1-y)*2) + 2
		else:
			blocksbefore = (2*y*(((xboards-1)*2)+1))+(z*2)
	elif n == 1:
		blocksbefore = (2*y*(((xboards-1)*2)+1))+(z*2)+1
	elif n == 2:
		blocksbefore = (2*y*(((xboards-1)*2)+1))+((xboards-1)*2)+((xboards-1-z)*2)+2
	else:
		if z == 0:
			blocksbefore = (2*yboards*(((xboards-1)*2)+1)) + ((yboards-1-y)*2) + 1
		else:
			blocksbefore = (2*y*(((xboards-1)*2)+1))+((xboards-1)*2)+((xboards-1-z)*2)+3
	offset = n * 4
	#print "c:",c
	#print "bb:",blocksbefore
	return (blocksbefore * 4) + jtagmap[c] - offset

def memboard(y,z,c):
	global jtagmap
	nodeid = (z+1) << (boardbits + ybits)
	route = []
	jtagmap = [j + 1 for j in jtagmap]
	jtagnode = calcjtag(y,z,c-1)
	print
	print "# MEMORY BOARD START"
	print "JTAG Node =",jtagnode
	print hex(nodereg),"=",hex(nodeid),("\t#0b{0:0%db}" % totalbits).format(nodeid)
	calcdirs(route,nodeid,xbits,xmap[nodeid&((xbits**2)-1)])
	calcdirs(route,nodeid>>xbits,yboardbits,ymap[nodeid&((xbits**2)-1)])
	calcdirs(route,nodeid>>(xbits+yboardbits),ybits,ymap[nodeid&((xbits**2)-1)])
	calcdirs(route,nodeid>>(xbits+yboardbits+ybits),zbits,zmap[nodeid&((xbits**2)-1)])
	directions = map(lambda x: dirmap[x],route)
	linkdir = { 				\
		'a': dirmap['left'],	\
	}
	for links in linkdir:
		for l in links:
			print hex(linkregs[l]),"=",hex(linkdir[links]<<dirpos)
	dirregs = [0,0]
	dirregspos = 0
	for k,d in enumerate(directions):
		dirregs[dirregspos] |= directions[k]<<(k*dirwidth)
		if k == 7:
			dirregspos += 1
	for k,d in enumerate(dirregs):
		print hex(dirreg+k),"=",hex(d)
	print "# MEMORY BOARD END"
	print "# Resuming XMP16 board..."

for y in range(yboards):
	for z in range(xboards):
		if config[y][z] != 1:
			print >> sys.stderr, "ERROR:",sys.argv[0], "does not yet support non-rectangular board arrangements"
			sys.exit(2)
		#print y,z
		print
		print "#new board"
		for c in range(boardnodes):
			nodeid = c | (y << boardbits) | (z << (boardbits + ybits))

			if M and c == 8 and y == 0 and z == xboards - 1:
				print "ADD THE MEMORY BOARD HERE"
				memboard(y,z,c)


			route = []
			jtagnode = calcjtag(y,z,c)
			print
			print "JTAG Node =",jtagnode
			print hex(nodereg),"=",hex(nodeid),("\t#0b{0:0%db}" % totalbits).format(nodeid)
			calcdirs(route,nodeid,xbits,xmap[nodeid&((xbits**2)-1)])
			calcdirs(route,nodeid>>xbits,yboardbits,ymap[nodeid&((xbits**2)-1)])
			calcdirs(route,nodeid>>(xbits+yboardbits),ybits,ymap[nodeid&((xbits**2)-1)])
			calcdirs(route,nodeid>>(xbits+yboardbits+ybits),zbits,zmap[nodeid&((xbits**2)-1)])
			directions = map(lambda x: dirmap[x],route)
			linkdir = { 							\
				'a': dirmap[linkmap[nodeid&((xbits**2)-1)]['a']],	\
				'b': dirmap[linkmap[nodeid&((xbits**2)-1)]['b']],	\
				'efgh': dirmap[linkmap[nodeid&((xbits**2)-1)]['efgh']]	\
			}
			for links in linkdir:
				for l in links:
					print hex(linkregs[l]),"=",hex(linkdir[links]<<dirpos)
			dirregs = [0,0]
			dirregspos = 0
			for k,d in enumerate(directions):
				dirregs[dirregspos] |= directions[k]<<(k*dirwidth)
				if k == 7:
					dirregspos += 1
			for k,d in enumerate(dirregs):
				print hex(dirreg+k),"=",hex(d)

