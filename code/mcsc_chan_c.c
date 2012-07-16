/*
 * mcsc_chan - Channel tools for XMP16 multicore->single-core compilation
 *
 * Provides a compatibility layer when needed, some stuff for initialisation,
 * and enables hybrid streaming channels that replace the "streaming chanend"
 * concept by allowing regular channels to be temporarily used for streaming.
 * 
 * Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
 *
 * This software is freely distributable under a derivative of the
 * University of Illinois/NCSA Open Source License posted in
 * LICENSE.txt and at <http://github.xcore.com/>
 */

#include <xs1.h>
#include <xccompat.h>
#include "mcsc_chan.h"

unsigned kep;

void installChanException()
{
  __asm__ __volatile__(" get r11,kep\n"
    " mov %0,r11\n"
    " ldap r11, chanException\n"
    " set kep,r11"
      :"=r"(kep)::"r11");
    
  asm(" retsp 0");
  asm(".align 128\n"
    "chanException: kret"::);
}

void uninstallChanException()
{
  __asm__ __volatile__(" mov r11,%0\n"
    "set kep,r11"::"r"(kep):"r11");
}

void cResetChans(unsigned myid)
{
	unsigned i, c;
	//installChanException();
	do
	{
	  c = getLocalAnonChanend();
	} while (c);
	for (i = 0; i < 0x2; i += 1)
	{
		freeChanend((myid << 16) | (i << 8) | 0x2);
	}
	//uninstallChanException();
	return;
}

/* Something weird happens with channel allocation here */
unsigned write_sswitch_reg_no_ack_clean(unsigned node, unsigned reg, unsigned val)
{
	unsigned ret = 0, c = getLocalAnonChanend(), d;
	freeChanend(c);
	ret = write_sswitch_reg_no_ack(node, reg, val);
	d = getLocalAnonChanend();
	if (d != c)
	{
		freeChanend(c);
	}
	freeChanend(d);
	return ret;
}

/* Something weird happens with channel allocation here*/
unsigned write_sswitch_reg_clean(unsigned node, unsigned reg, unsigned val)
{
	unsigned ret = 0, c = getLocalAnonChanend(), d;
	freeChanend(c);
	ret = write_sswitch_reg(node, reg, val);
	d = getLocalAnonChanend();
	if (d != c)
	{
		freeChanend(c);
	}
	freeChanend(d);
	return ret;
}

unsigned read_sswitch_reg_clean(unsigned node, unsigned reg, unsigned *val)
{
  unsigned ret = 0, c = getLocalAnonChanend(), d;
	freeChanend(c);
	ret = read_sswitch_reg(node, reg, val);
	d = getLocalAnonChanend();
	if (d != c)
	{
		freeChanend(c);
	}
	freeChanend(d);
	return ret;
}

void freeChanend(unsigned c)
{
	asm("freer res[%0]"::"r"(c));
}
