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

void basicTest(chanend c, unsigned id)
{
  unsigned d;
  if (id)
  {
    c <: 0xbabecafe;
  }
  else
  {
    c :> d;
    while (1)
    {
      leds1 <: d;
    }
  }
  
}

void dynamic_linkup(unsigned vid)
{
  unsigned data, cid = swallow_id(vid), tv;
  timer t;
  //xscope_register(0);
  //xscope_config_io(XSCOPE_IO_BASIC);
  printstr("My core VID/RealID is: 0x");
  printhex(vid);
  printstr("/0x");
  printhexln(cid);
  
  read_sswitch_reg(cid,0x6,data);
  printstr("PLL config is: 0x");
  printhexln(data);
  
  read_sswitch_reg(cid,0x7,data);
  printstr("Switch divider is: 0x");
  printhexln(data);
  
  read_sswitch_reg(cid,0x8,data);
  printstr("Ref divider is: 0x");
  printhexln(data);
  
  printstrln("Enabling link hardware...");
  write_sswitch_reg_clean(cid,0x23,0x00000010);
  write_sswitch_reg_clean(cid,0x83,0xc0000800);
  printstrln("Link enabled, attempting to issue credit...");
  write_sswitch_reg_clean(cid,0x83,0xc1000800);
  printstrln("Credit issued, now reading state... FOREVER!");
  t :> tv;
  read_sswitch_reg(cid,0x83,data);
  while((data & 0x0e000000) != 0x06000000)
  {
    if (data & 0x08000000)
    {
      printstrln("Link bad or down, giving up!");
      return;
    }
    write_sswitch_reg_clean(cid,0x83,0xc1000800);
    read_sswitch_reg(cid,0x83,data);
    printstr("The link state is currently: 0x");
    printhexln(data);
    tv += 0x04000000;;
    t when timerafter(tv) :> void;
  }
  printstrln("Link is now up!");
}

void bwah(chanend c, unsigned cid)
{
  if (cid == 0)
  {
    c <: 1;
  }
  else
  {
    //xscope_register(0);
    //xscope_config_io(XSCOPE_IO_BASIC);
    c :> cid;
    printstrln("HI!");
  }
}

void scopetest(unsigned cid)
{
  timer t;
  unsigned tv;
  //xscope_register(0);
  //xscope_config_io(XSCOPE_IO_BASIC);
  t :> tv;
  while(1) 
  {
    printf("Hello from core %u!\n",cid);
    tv += 0x08000000;
    t when timerafter(tv) :> tv;
  }
}

void tokenscope(chanend ci, chanend co, unsigned cid)
{
  unsigned t;
  //xscope_register(0);
  //xscope_config_io(XSCOPE_IO_BASIC);
  if (cid == 0)
  {
    printintln(cid);
    co <: 1;
  }
  while (1)
  {
    ci :> t;
    printintln(cid);
    co <: t;
  }
}

void doled(void)
{
	timer t;
	unsigned tv,pv = 0;
	t :> tv;
	while (1)
	{
		pv = 0xf - pv;
		tv += 25000000;
		t when timerafter(tv) :> void;
		leds1 <: pv;
	}
	return;
}

void switchChat(unsigned width, unsigned ncores, unsigned cid)
{
  unsigned tv;
	int start = (cid - (width/2)) % ncores, max = (cid + (width/2) - 1) % ncores, i;
	while(1)
	{
		for (i = start; i != max; i = (i + 1) % ncores)
		{
			read_sswitch_reg(swallow_id(i),0x5,tv);
	  }
	}
}

void checkLinks()
{
  int i = 0x82;
  unsigned tv, myid = get_local_tile_id();
  while(1)
  {
    read_sswitch_reg(myid,i,tv);
    if (tv & 0x00800000)
    {
      printf("Link error on %d[%x]\n",myid,i);
    }
    i = (i == 0x87) ? i + 1 : 0x82;
  }
}

void latencyTest(unsigned len)
{
	unsigned i, tv1, tv2, tmp, res[64];
	timer t;
	for (i = 0; i < len; i += 2)
	{
		t :> tv1;
		read_sswitch_reg(swallow_id(i),0x5,tmp);
		t :> tv2;
		res[i] = tv2-tv1;
	}
	for (i = 1; i < len; i += 2)
	{
		t :> tv1;
		read_sswitch_reg(swallow_id(i),0x5,tmp);
		t :> tv2;
		res[i] = tv2-tv1;
	}
	for (i = 0; i < len; i += 1)
	{
		printf("0x%03x: %d refticks\n",i,res[i]);
	}
}

void nonsense(unsigned x)
{
	while(1)
	{
		asm("mov r1,r0"::);
	}
}

void mulkernela(void)
{
    register int a,b,c=0x55555555,d=0x55555555,e=0x55555555,f=0x55555555;
    asm("aloop: lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "bu aloop"
    :"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
}

void mulkernelb(void)
{
    register int a,b,c=0xaaaaaaaa,d=0xaaaaaaaa,e=0xaaaaaaaa,f=0xaaaaaaaa;
    asm("bloop: lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "lmul %0,%1,%2,%3,%4,%5\n"
    "bu bloop"
    :"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
}

void racetrack(chanend cin, chanend cout, unsigned cid)
{
	unsigned char b = 1;
	timer t;
	unsigned tv;
	//printf("Chanend cin: %08x <-> %08x\n",getLocalChanendId(cin),getRemoteChanendId(cin));
	//printf("Chanend cout: %08x <-> %08x\n",getLocalChanendId(cout),getRemoteChanendId(cout));
	//return;
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
		//printf("Core %d done!\n",swallow_id(cid));
	}
}

void commSpeed(chanend c, unsigned role)
{
	unsigned tv1, tv2, tt, i = 0, tests=32, val;
	timer t;
	//printf("Chanend c: %08x <-> %08x\n",getLocalChanendId(c),getRemoteChanendId(c));
	//return;
	while(1)
	{
		if (!role)
		{
			t :> tv1;
			c <: 0;
			c :> val;
			t :> tv2;
			//if (i > 0) //Skip the first test to allow logical links to settle
  			tt += tv2-tv1;
			if (++i == tests)
			{
				break;
			}
		}
		else
		{
			c :> val;
			c <: 1;
			if (++i == tests)
			{
				return;
			}
		}
	}
	t :> tv1;
	t when timerafter(tv1 + 0x08000000) :> void;
	printf("0x%08x: Avg trip time: %d refclocks\n",c,tt/tests);
	return;
}

void testComms(chanend c, unsigned role)
{
	unsigned val = 0, tv;
	timer t;
	t :> tv;
	if (role == 0)
	{
		while(1)
		{
			//tv += 100000;
			//t when timerafter(tv) :> void;
			/*closeChanend(c);
			outUint(c,val);
			closeChanend(c);
			val = inUint(c);*/
		}
	}
	else
	{
		while(1)
		{
			//tv += 100000;
			//t when timerafter(tv) :> void;
			/*closeChanend(c);
			val = inUint(c);
			if ((val & 0xfffff) == 0xfffff ) printf("0x%08x\n",val);
			outUint(c,val + 1);
			closeChanend(c);*/
		}
	}
}
