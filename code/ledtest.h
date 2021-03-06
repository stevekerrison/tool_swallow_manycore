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

#include "mcsc_chan.h"

void dynamic_linkup(unsigned vid);

void scopetest(unsigned cid);

void tokenscope(chanend ci, chanend co, unsigned cid);

void bwah(chanend c, unsigned cid);

void doled(void);

void switchChat(unsigned width, unsigned ncores);

void checkLinks();

void testComms(chanend c, unsigned role);

void commSpeed(chanend c, unsigned role);

void latencyTest(unsigned len);

void nonsense(unsigned x);

void racetrack(chanend cin, chanend cout, unsigned cid);

void mulkernela(void);
void mulkernelb(void);

void fourByFour(chanend a, chanend b, chanend c, chanend d);

#endif //_LEDTEST_H
