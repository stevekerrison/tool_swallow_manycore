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
    lpos = self.walk_left_path[self.walkstep]
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

  def dirbits(self):
    """Generate the direction bits for the current node position.
    Implementation is similar to swallow_xlinkboot
    
    TODO: XScope directions - old route probably invalid now, hence
    unimplemented"""
    d = ['0'] * 16
    nref = self.node_ref(self.pos)
    layer = (nref >> self.r_lpos) & (2**self.r_lbits - 1)
    rows = self.h * self.cores_h
    cols = self.w * self.cores_w
    # This is a bit Swallow specific and not very programmatic at times
    if layer:
      d[self.r_lpos] = self.directions['d_away']
    else:
      d[self.r_lpos] = self.directions['d_towards']
    if layer:
      if self.pos[1] >> 1 == 0:
        d[0] = self.directions['d_left']
      else:
        d[0] = self.directions['d_right']
      if self.pos[0] == 1:
        d[15] = self.directions['d_left']
      else:
        d[15] = self.directions['d_away']
      for i in xrange(self.r_vbits):
        d[i + self.r_vpos] = self.directions['d_away']
      for i in xrange(self.r_hbits):
        if (self.pos[1] >> (i+1)) & 1:
          d[i + self.r_hpos] = self.directions['d_left']
        else:
          d[i + self.r_hpos] = self.directions['d_right']
    else:
      if self.pos[0] == 0:
        d[0] = self.directions['d_up']
      else:
        d[0] = self.directions['d_down']
      if self.pos[0] == 1:
        d[15] = self.directions['d_towards']
      elif self.pos[0] == 0:
        d[15] = self.directions['d_down']
      else:
        d[15] = self.directions['d_up']
      for i in xrange(self.r_hbits):
        d[i + self.r_hpos] = self.directions['d_towards']
      for i in xrange(self.r_vbits):
        if (self.pos[0] >> i) & 1:
          d[i + self.r_vpos] = self.directions['d_up']
        else:
          d[i + self.r_vpos] = self.directions['d_down']
    return ''.join(map(str,d))

  def walk_jtag(self):
    """Find the next position in the JTAG chain in row/col terms"""
    self.walkmode()

  def physlink(self,l):
    """Declare the physical link properties for this node and link, if
    necessary"""
    nref = self.node_ref(self.pos)
    layer = (nref >> self.r_lpos) & (2**self.r_lbits - 1)
    if l == 2 or (l >= 4 and layer):
      # Skip left/up links, or internal links if we're the second tile
      return
    if l == 3:
      if layer:
        neighbour = (self.pos[0],self.pos[1] + 2)
      else:
        neighbour = (self.pos[0] + 1, self.pos[1])
    else:
      neighbour = (self.pos[0], self.pos[1] + 1)
    lphys = ET.Element('Link')
    lphys.attrib['Encoding'] = '5wire'
    if l >= 4:
      #On-package links
      lphys.attrib['Delays'] = '0,1'
    else:
      lphys.attrib['Delays'] = '2,1'
    myref = self.logical_ref(self.pos)
    neighbourref = self.logical_ref(neighbour)
    lend1 = ET.Element('LinkEndpoint')
    lend2 = ET.Element('LinkEndpoint')
    lphys.append(lend1)
    lend1.attrib['NodeId'] = str(myref)
    lend1.attrib['Link'] = 'XL' + self.linkmap[l].upper()
    lend2.attrib['NodeId'] = str(neighbourref)
    lend2.attrib['Link'] = 'XL' + self.linkmap[self.linkconn[l]].upper()
    lphys.append(lend2)
    self.Links.append(lphys)

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
        nodes = ET.Element('Nodes')
        pkg.append(nodes)
      lref = str(self.logical_ref(self.pos))
      nref = self.node_ref(self.pos)
      layer = (nref >> self.r_lpos) & (2**self.r_lbits - 1)
      node = ET.Element('Node',Oscillator='25MHz',SystemFrequency='500MHz',
        ReferenceFrequency='100MHz')
      node.attrib['Id'] = lref
      node.attrib['InPackageId'] = str(ipid)
      ipid = 1 - ipid
      node.attrib['Type'] = str(self.coretype)
      node.attrib['routingId'] = hex(nref)
      node.append(ET.Element('Tile',Number='0',
        Reference='tile[{}]'.format(lref)))
      rtbl = ET.Element('RoutingTable')
      node.append(rtbl)
      bits = ET.Element('Bits')
      rtbl.append(bits)
      dirbits = self.dirbits()
      for b in xrange(16):
        bits.append(ET.Element('Bit',number=str(b),direction=dirbits[b]))
      links = ET.Element('Links')
      rtbl.append(links)
      rows = self.h * self.cores_h
      cols = self.w * self.cores_w
      for l in xrange(2,8):
        # Conditions in which we do not normally enable links (board edges)...
        if (
          (self.pos[0] == 0 and not layer and l == 2) # A-links along the top
          or (self.pos[0] == rows - 1 and not layer and l == 3) # Bottom B-links
          # Left A-links
          or (self.pos[1] == 1 and layer and l == 2 and self.pos[0] != 1)
          or (self.pos[1] == cols - 1 and layer and l == 3) # Right B-links
          ):
          continue
        link = ET.Element('Link')
        link.attrib['name'] = 'XL' + self.linkmap[l].upper()
        link.attrib['direction'] = str( self.dirmap[layer].get(
          l,self.dirmap[layer][None] ) )
        links.append(link)
        self.physlink(l)
      nodes.append(node)
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
    Decls = ET.Element('Declarations')
    Decl = ET.Element('Declaration')
    Decl.text = "tileref tile[{}]".format(self.total_cores)
    Decls.append(Decl)
    Network.append(Decls)
    self.walkgen()
    xscope = ET.Element('Link',Encoding='2wire',Delays='4,4',Flags='XSCOPE')
    xscope.append(ET.Element('LinkEndpoint',Link='XLA',
      NodeId=str(self.logical_ref((1,1)))))
    xscope.append(ET.Element('LinkEndpoint',RoutingId="0x8000",Chanend="1"))
    self.Links.append(xscope)
    Network.append(self.Packages)
    Network.append(self.Links)
    Network.append(self.JTAG)
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
