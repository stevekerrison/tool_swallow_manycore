#!/usr/bin/python
"""
swallow-gen-xn.py - Build swallow XN files compatible with XMOS tools 13+

Copyright (C) 2014 Steve Kerrison <github@stevekerrison.com>

This software is freely distributable under a derivative of the
University of Illinois/NCSA Open Source License posted in
LICENSE.txt and at <http://github.xcore.com/>

Usage:
  swallow-gen-xn.py <boards_w> <boards_h> [options] [<filename>]
  
Arguments:
  <boards_w>    Number of boards horizontally
  <boards_h>    Number of boards vertically
  <filename>  Output XN file to specified name, stdout if omitted or '-'

Options:
  (None just yet) 
  """



from docopt import docopt
from lxml import etree as ET
import re

class SwallowXNGenerator(object):
  NS        = 'http://www.xmos.com'
  NSS       = '{%s}' % NS
  XSI       = 'http://www.w3.org/2001/XMLSchema-instance'
  XSIS      = '{%s}' % XSI
  NSMAP     = {None: NS, 'xsi': XSI}
  package   = 'XS1-L2A-QF124'
  coretype  = 'XS1-L1A'
  r_pbits   = 1
  r_ppos    = 0
  r_lbits   = 1
  r_lpos    = r_pbits + r_ppos
  r_hbits   = 6
  r_hpos    = r_lbits + r_lpos
  r_vbits   = 7
  r_vpos    = r_hbits + r_hpos
  r_xbits   = 1
  r_xpos    = r_vbits + r_vpos
  chips_w   = 2
  chips_h   = 4
  directions       = {'d_towards': 0, 'd_away': 1, 'd_left': 2, 'd_right': 3,
    'd_up': 4, 'd_down': 5}
  # Dealing with the numerical vs named Xlink maps
  linkmap          = {0: 'c', 1: 'd', 2: 'a', 3: 'b', 4: 'g', 5: 'h', 6: 'e',
    7: 'f'}
  dirmap           = {0: { 2: directions['d_up'],
                           3: directions['d_down'],
                        None: directions['d_towards'] },
                      1: { 2: directions['d_left'],
                           3: directions['d_right'],
                        None: directions['d_away'] } }
  linkconn         = { 0: 1, 1: 0, 2: 3, 3: 2, 4: 7, 5: 6, 6: 5, 7: 4 }
  cores_per_chip   = 2
  cores_w          = chips_w * cores_per_chip
  cores_h          = chips_h
  cores_per_board  = chips_w * chips_h * cores_per_chip
  walk_top_path    = [(1,1),(1,0),(0,1),(0,0),(0,3),(0,2),(1,3),(1,2)]
  walk_bottom_path = [(2,3),(2,2),(3,3),(3,2),(3,1),(3,0),(2,1),(2,0)]
  walk_left_path   = [(3,1),(3,0),(2,1),(2,0),(1,1),(1,0),(0,1),(0,0)]

  def node_ref(self,pos):
    return (pos[0] << self.r_vpos) | (pos[1] << self.r_lpos)

  def logical_ref(self,pos):
    return pos[0] * self.chips_w * self.cores_per_chip * self.w + pos[1]

  def walk_left(self):
    """Walk along the left of the boards, back to the JTAG adapter"""
    lpos = self.walk_bottom_path[self.walkstep]
    self.pos = ( lpos[0] + (self.board[0] * self.cores_w),
      lpos[1] + (self.board[1] * self.cores_h) )
    self.walkstep += 1
    if self.walkstep == 8:
      self.walkstep = 0
      self.board = (self.board[0] - 1, self.board[1])

  def walk_bottom(self):
    """Walking along the bottom of a row of boards"""
    lpos = self.walk_bottom_path[self.walkstep]
    self.pos = ( lpos[0] + (self.board[0] * self.cores_w),
      lpos[1] + (self.board[1] * self.cores_h) )
    self.walkstep += 1
    # Go down if we're on the left board a little early
    if ( self.walkstep == 4 and self.h > 1 and self.board[0] + 1 != self.h
        and self.board[1] == 0 ):
      self.walkstep = 4
      self.walkmode = self.walk_top
      self.board = (self.board[0] + 1, self.board[1])
    # Otherwise move left when it's time to do so
    elif self.walkstep == 8:
      if self.board[1] == 0:
        self.walkstep = 4
        self.walkmode = self.walk_left
      else:
        self.walkstep = 0
        self.board = (self.board[0],self.board[1] - 1)

  def walk_top(self):
    """Walking along the top of a row of boards"""
    lpos = self.walk_top_path[self.walkstep]
    self.pos = ( lpos[0] + (self.board[0] * self.cores_w),
      lpos[1] + (self.board[1] * self.cores_h) )
    self.walkstep += 1
    if self.walkstep == 8:
      self.walkstep = 0
      if self.board[1] + 1 == self.w:
        self.walkmode = self.walk_bottom
      else:
        self.board = (self.board[0],self.board[1] + 1)

  def dirbit(self,b):
    d = None
    if b == 0:
      if self.pos[0] == 0:
        d = 'd_up'
      else:
        d = 'd_down'
    else:
      d = 'd_left'

    return self.directions[d]

  def walk_jtag(self):
    """Find the next position in the JTAG chain in row/col terms"""
    self.walkmode()

  def walkgen(self):
    """Walk the grid's JTAG chain and work out all the links, routes and IDs"""
    self.JTAG = ET.Element('JTAGChain')
    self.Links = ET.Element('Links')
    self.Packages = ET.Element('Packages')
    self.pos = (1,1)
    self.board = (0,0)
    self.walkmode = self.walk_top
    self.walkstep = 0
    pid = 0
    ipid = 0
    for jtagid in xrange(self.total_cores):
      self.walk_jtag()
      # Build the JTAG Device list in the right order, with correct IDs
      jt = ET.Element('JTAGDevice')
      jt.attrib['NodeId'] = str(self.logical_ref(self.pos))
      self.JTAG.append(jt)
      # Add the package
      if ipid == 0:
        pkg = ET.Element('Package')
        pkg.attrib['ID'] = str(pid)
        pid += 1
        pkg.attrib['Type'] = self.package
      lref = str(self.logical_ref(self.pos))
      nref = str(self.node_ref(self.pos))
      layer = (int(nref) >> self.r_lpos) & (2**self.r_lbits - 1)
      node = ET.Element('Node')
      node.attrib['Id'] = lref
      node.attrib['InPackageId'] = str(ipid)
      ipid = 1 - ipid
      node.attrib['Type'] = str(self.coretype)
      node.attrib['routingId'] = nref
      tile = ET.Element('Tile')
      tile.attrib['Number'] = '0'
      tile.attrib['Reference'] = 'tile[{}]'.format(lref)
      tile.text = ''
      node.append(tile)
      rtbl = ET.Element('RoutingTable')
      node.append(rtbl)
      bits = ET.Element('Bits')
      rtbl.append(bits)
      for b in xrange(16):
        bit = ET.Element('Bit')
        bit.attrib['number'] = str(b)
        bit.attrib['direction'] = str(self.dirbit(b))
        bits.append(bit)
      links = ET.Element('Links')
      node.append(links)
      for l in xrange(2,8):
        link = ET.Element('Link')
        link.attrib['name'] = 'XL' + self.linkmap[l].upper()
        link.attrib['direction'] = str( self.dirmap[layer].get(
          l,self.dirmap[layer][None] ) )
        links.append(link)
      pkg.append(node)
      if ipid == 0:
        self.Packages.append(pkg)
      """print "JTAG = {:03}, logical = {:03}, node = 0x{:04x}".format(
        jtagid,self.logical_ref(self.pos),self.node_ref(self.pos) )"""

  def generate(self):
    self.total_cores = self.w * self.h * self.cores_per_board
    Network = ET.Element(self.NSS + 'Network', nsmap=self.NSMAP)
    Network.attrib[self.XSIS + 'schemaLocation'] = '{0} {0}'.format(self.NS)
    Type = ET.Element('Type')
    Type.text = 'Device'
    Network.append(Type)
    Name = ET.Element('Name')
    if self.name.find('{}') != -1:
      Name.text = self.name.format(self.total_cores) 
    else:
      Name.text = self.name
    Name.text += " ({}w * {}h)".format(self.w,self.h)
    Network.append(Name)
    Decls = ET.Element('Delcarations')
    Decl = ET.Element('Declaration')
    Decl.text = "tileref tile[{}]".format(self.total_cores)
    Decls.append(Decl)
    Network.append(Decls)
    self.walkgen()
    Network.append(self.JTAG)
    Network.append(self.Links)
    Network.append(self.Packages)
    return Network

  def __init__(self,boards_w=1,boards_h=1,name='Swallow {} tile system'):
    self.w = int(boards_w)
    self.h = int(boards_h)
    self.name = name
     

if __name__ == '__main__':
  args = docopt(__doc__)
  xn = SwallowXNGenerator(args['<boards_w>'],args['<boards_h>'])
  print ET.tostring(xn.generate(), xml_declaration=True, encoding='utf-8',
    pretty_print=True)
