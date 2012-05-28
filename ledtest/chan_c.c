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

/* Something weird happens with */
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

void txCloseChan(unsigned c)
{
	unsigned t = XS1_CT_END;
	asm("outct res[%0],%1"::"r"(c),"r"(t));
	asm("inct %0,res[%1]":"=r"(t):"r"(c));
}

void rxCloseChan(unsigned c)
{
	unsigned t;
	asm("inct %0,res[%1]":"=r"(t):"r"(c));
	t = XS1_CT_END;
	asm("outct res[%0],%1"::"r"(c),"r"(t));
}

void freeChanend(unsigned c)
{
	asm("freer res[%0]"::"r"(c));
}
