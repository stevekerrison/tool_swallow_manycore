#include <xs1.h>
#include <xccompat.h>
#include "chan.h"

void cResetChans(unsigned myid)
{
	unsigned i, c;
	do
	{
		c = getLocalAnonChanend();
	}
	while (c);
	for (i = 0; i < 0x2; i += 1)
	{
		freeChanend((myid << 16) | (i << 8) | 0x2);
	}
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

void freeChanend(unsigned c)
{
	asm("freer res[%0]"::"r"(c));
}
