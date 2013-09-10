/*
 * ledtest - Some code for flashing LEDs and doing some basic tests
 * 
 * Demonstrates how to use multi-core mains that are compatible with XMP16s
 * 
 * Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
 *
 * This software is freely distributable under a derivative of the
 * University of Illinois/NCSA Open Source License posted in
 * LICENSE.txt and at <http://github.xcore.com/>
 */

#ifndef _LEDTEST_H
#define _LEDTEST_H

#include "swallow_comms.h"

void racetrack(chanend cin, chanend cout, unsigned cid);

#endif //_LEDTEST_H
