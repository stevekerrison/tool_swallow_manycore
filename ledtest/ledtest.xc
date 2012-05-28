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
	unsigned tv;
	for (; i < max; i++)
	{
		read_sswitch_reg(i,0x5,tv);
		printf("Switch %d says %d\n",i,tv);
		//printf("HI\n");
	}
}
