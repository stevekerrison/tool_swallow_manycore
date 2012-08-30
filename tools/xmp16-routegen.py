#!/usr/bin/python

# Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
#
# This software is freely distributable under a derivative of the
# University of Illinois/NCSA Open Source License posted in
# LICENSE.txt and at <http://github.xcore.com/>

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
Example for a 2x3 mesh of boards with memory: ./xmp16-routegen.py "1 1 1;1 1 1" M
"""
import sys,math

if len(sys.argv) != 2 and len(sys.argv) != 3:
  print >> sys.stderr, header
  sys.exit(1)

#Description of a single board's JTAG map
jtagmap = [       \
  3, 2, 4, 5,     \
  1, 0, 6, 7,     \
  15, 14, 8, 9,   \
  13, 12, 10, 11  \
]
#How the board's JTAG quadrants are broken down
nodequadrants = [ \
  0, 0, 1, 1,     \
  0, 0, 1, 1,     \
  3, 3, 2, 2,     \
  3, 3, 2, 2      \
]

dirmap = {                  \
  'towards':0,'away':1,     \
  'left':2,'right':3,       \
  'up':4,'down':5           \
}

linkmap = [                               \
  {'a':'up','b':'down','efgh':'towards'}, \
  {'a':'left','b':'right','efgh':'away'}, \
  {'a':'up','b':'down','efgh':'towards'}, \
  {'a':'left','b':'right','efgh':'away'}, \
]

linkregs = { 'a':0x22,'b':0x23,'c':0x20,'d':0x21, \
  'e':0x26,'f':0x27,'g':0x24,'h':0x25 }

linkenable = { 'a':0x82,'b':0x83,'c':0x80,'d':0x81,\
  'e':0x86,'f':0x87,'g':0x84,'h':0x85 }

nodereg = 0x05
networkpos = 4
networkwidth = 2
dirwidth = 4
dirpos = 8 #In the link control register
dirreg = 0x0c

lmap = [['towards','away'],['towards','away']]
xmap = [['towards','towards'],['right','left']]
ymap = [['down','up'],['away','away']]

#Xscopemap applied differently to the regular routing maps: row0, row1, row(>1)
scopemap = [\
  ['down','away','away','down'],\
  ['towards','left','left','towards'],\
  ['up','away','away','up']\
]
#Temporary mapping for memory: row0, row(>0)
memmap = [\
  ['towards','left','left','towards'],\
  ['up','away','away','up']\
]
#xmap = [['right','left'],['right','left'],['right','left'],['right','left']]
#ymap = [['down','up'],['left','left'],['right','right'],['down','up']]
#zmap = [['right','right'],['right','towards'],['away','left'],['left','left']]
#Deal with the memory board creating an irregular mesh.
#zmapmend = [['right','right'],['right','towards'],['right','left'],['up','left']]

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
numcores = xboards * yboards * 16

xboardbits = int(math.ceil(math.log(xboardnodes)/math.log(2)))
yboardbits = int(math.ceil(math.log(yboardnodes)/math.log(2)))
xbits = int(math.ceil(math.log(xboards)/math.log(2)))
ybits = int(math.ceil(math.log(yboards)/math.log(2)))
lbits = 1 #This is the layer of the mesh that the core occupies - there are only two layers
boardbits = xboardbits + yboardbits
totalbits = boardbits+xbits+ybits

def calcdirs(lst,data,width,dirs):
  for b in range(width):
    x = ([dirs[0]]*(2**b) + [dirs[1]]*(2**b))*(2**(width-1)/2**b)
    lst.append(x[data & (2**width-1)])

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

#TODO: Fix routing as it's currently going to use nonexistant links to get to the memory board
"""def memboard(y,z,c):
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
  linkdir = {         \
    'a': dirmap['left'],  \
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
  print "# Resuming XMP16 board..."""
  
print "DIM = %d(%d)x%d(%d)" % (yboards,ybits,xboards,xbits)

def parity(x):
  k = 0
  d = x
  while d != 0:
    k = k + 1
    d = d & (d - 1)
  return k % 2


for y in range(yboards):
  for x in range(xboards):
    if config[y][x] != 1:
      print >> sys.stderr, "ERROR:",sys.argv[0], "does not yet support non-rectangular board arrangements"
      sys.exit(2)
    #print y,x
    print
    print "#new board, position",y,x
    for c in range(boardnodes):
      #New node ID strategy is [y..y x..x c]
      #c = 0 for c & 0x3 in 0,3 and c = 1 for c & 0x3 in 1,2
      layer = parity(c&0x3)
      nodeid = layer | (c & 0x2) | (x << xboardbits) | ((c & 0xc) << (xboardbits + xbits - 2)) | (y << (boardbits + xbits))
      if M and c == 8 and y == 0 and x == xboards - 1:
        memboard(y,x,c)

      route = []
      jtagnode = calcjtag(y,x,c)
      print
      print "JTAG Node =",jtagnode
      print hex(nodereg),"=",hex(nodeid),("\t#0b{0:0%db}" % totalbits).format(nodeid)
      calcdirs(route,nodeid,lbits,lmap[layer])
      calcdirs(route,nodeid>>lbits,xbits+xboardbits-lbits,xmap[layer])
      calcdirs(route,nodeid>>(xbits+xboardbits),ybits+yboardbits,ymap[layer])
      # Meddle with the routing table on the end boards if a memory board is present
      """if M and x == xboards - 1 and c not in [2,3]:
        calcdirs(route,nodeid>>(xbits+yboardbits+ybits),zbits,zmapmend[nodeid&((xbits**2)-1)])
      else:
        calcdirs(route,nodeid>>(xbits+yboardbits+ybits),zbits,zmap[nodeid&((xbits**2)-1)])"""
      directions = map(lambda x: dirmap[x],route)
      #print directions
      linkdir = {                         \
        'a': dirmap[linkmap[nodeid&((xboardbits**2)-1)]['a']],    \
        'b': dirmap[linkmap[nodeid&((xboardbits**2)-1)]['b']],    \
        'efgh': dirmap[linkmap[nodeid&((xboardbits**2)-1)]['efgh']]  \
      }
      #route.reverse()
      #print route
      #print linkdir
      for links in linkdir:
        for l in links:
          print hex(linkregs[l]),"=",hex(linkdir[links]<<dirpos)
      dirregs = [0,0]
      dirregspos = 0
      for k,d in enumerate(directions):
        dirregs[dirregspos] |= directions[k]<<(k*dirwidth)
        if k == 7:
          dirregspos += 1
      #Poke in some XSCOPE stuff!!
      row = min(2,c/xboardnodes + yboardnodes*y)
      dirregs[1] |= dirmap[scopemap[row][c & 0x3]] << 28
      row = min(1,c/xboardnodes + yboardnodes*y)
      dirregs[1] |= dirmap[memmap[row][c & 0x3]] << 24
      for k,d in enumerate(dirregs):
        print hex(dirreg+k),"=",hex(d)
      # Now throw away any links that are unconnected
      if (x == 0 and (c % 4) == 1):
        del linkdir['a']
      elif x == xboards - 1 and (c % 4) == 2 and not (M and c == 2 and y == 0 and x == xboards - 1):
        del linkdir['b']
      elif y == 0 and c in [0,3]:
        del linkdir['a']
      elif y == yboards - 1 and c in [12,15]:
        del linkdir['b']
      print "Links:",
      for i in [hex(linkenable[item]) for sublist in list(linkdir) for item in sublist]:
        print str(i),
      print
