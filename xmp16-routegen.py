#!/usr/bin/python

import sys,math



jtagmap = [ 		\
	3, 2, 4, 5, 	\
	1, 0, 6, 7, 	\
	15, 14, 8, 9, 	\
	13, 12, 10, 11	\
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

configrows = rawconfig.split(';')
config = []
for x in configrows:
	config.append(map(int,x.strip().split(' ')))

#print config

#Boards are 4x4 nodes
xboardnodes = 4
yboardnodes = 4
boardnodes = xboardnodes * yboardnodes

xboards = len(config[0])
yboards = len(config)

xbits = int(math.ceil(math.log(xboardnodes)/math.log(2)))
yboardbits = int(math.ceil(math.log(yboardnodes)/math.log(2)))
ybits = int(math.ceil(math.log(yboards)/math.log(2)))
zbits = int(math.ceil(math.log(xboards)/math.log(2)))
boardbits = xbits + yboardbits
totalbits = boardbits+ybits+zbits

#print xbits,yboardbits
#print ybits,zbits

def calcdirs(lst,data,width,dirs):
	for b in range(width):
		lst.append(dirs[(data >> b) & 1])


for y in range(yboards):
	for z in range(xboards):
		print "#new board"
		if config[y][z] != 1:
			print >> sys.stderr, "ERROR:",sys.argv[0], "does not yet support non-rectangular board arrangements"
			sys.exit(2)
		#print y,z
		for c in range(boardnodes):
			nodeid = c | (y << boardbits) | (z << (boardbits + ybits))
			route = []
			jtagnode = "x" #TODO: Sort this shit out
			"""if c < 4:
				jtagnode = jtagmap[c] + (y * 3)
			elif c < 8:
			elif c < 12:
			else:
				
			if c < 8:
				jtagnode = jtagmap[c] + (z * 8) + (y * 16)
			else:
				jtagnode = (jtagmap[c]-8) + ((xboards-1)*8) + ((xboards-z) * 8) + (y * 16)"""
			print
			print "JTAG Node = ",jtagnode
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
					diregspos += 1
			for k,d in enumerate(dirregs):
				print hex(dirreg+k),"=",hex(d)
			"""route.reverse()
			directions.reverse()
			print route
			print directions
			print linkdir"""
			#print jtagmap[c] * y
#print "{0:0%db}" % (xbits+ybits+zbits)

