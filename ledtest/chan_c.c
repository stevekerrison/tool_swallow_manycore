#include <xs1.h>
#include <xccompat.h>
#include "chan.h"

void cResetChans(unsigned myid)
{
	unsigned i, c;
	do
	{
		c = getChanend((myid << 16) | 0x2);
	}
	while (c != ((myid << 16) | 0x1f02));
	for (i = 0; i < 0x2; i += 1)
	{
		freeChanend((myid << 16) | (i << 8) | 0x2);
	}
	return;
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
