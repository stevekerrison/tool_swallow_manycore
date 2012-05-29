#include <platform.h>
#include "chan.h"
#include <stdio.h>

out port leds1 = XS1_PORT_4F;

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

void switchChat(unsigned i, unsigned max)
{
	unsigned start = i,tv,x,cid = get_core_id();
	while(1)
	{
		for (i = start; i < max; i++)
		{
			read_sswitch_reg(i,0x5,tv);
			x += tv;
			//printf("%d: Switch %d says %d\n",cid,i,tv);
			//printf("HI\n");
		}
		if (x > 0x1f0*20)
		{
			printf("%d:	Had a chat with all %d switches (%x)\n",cid,i,x);
			x = 0;
		}
	}
}

void commSpeed(chanend c, unsigned role)
{
	unsigned tv1, tv2;
	timer t;
	if (role)
	{
		closeChanend(c);
		t :> tv1;
		outUint(c,0);
		closeChanend(c);
		inUint(c);
		t :> tv2;
		printf("Trip time: %d refclocks\n",tv2-tv1);
	}
	else
	{
		closeChanend(c);
		inUint(c);
		closeChanend(c);
		outUint(c,1);
	}
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
			closeChanend(c);
			outUint(c,val);
			closeChanend(c);
			val = inUint(c);
		}
	}
	else
	{
		while(1)
		{
			//tv += 100000;
			//t when timerafter(tv) :> void;
			closeChanend(c);
			val = inUint(c);
			if ((val & 0xfffff) == 0xfffff ) printf("0x%08x\n",val);
			outUint(c,val + 1);
			closeChanend(c);
		}
	}
}
