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

#include <platform.h>
#include <stdio.h>
#include "swallow_comms.h"
#include <xscope.h>
#include <print.h>

out port leds1 = XS1_PORT_4F;

void racetrack(chanend cin, chanend cout, unsigned cid)
{
	unsigned char b = 1;
	timer t;
	unsigned tv;
	if (cid % 19 == 0)
	{
		cout <: b;
	}
	while(1)
	{
		cin :> b;
		if (cid == 0)
		{
			b = (b+1) & 0xf;
			if (b == 0) b = 1;
		}
		leds1 <: b;
		t :> tv;
		t when timerafter(tv + 0x00600000) :> void;
		cout <: b;
		leds1 <: 0;
	}
}

