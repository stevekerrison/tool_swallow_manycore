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
			if (tv != i)
			{
				printf("%d: BAD node ID %x detected at %x\n",cid,tv,i);
			}
			x += tv;
			//printf("%d: Switch %d says %d\n",cid,i,tv);
			//printf("HI\n");
		}
		if (x > 0x1f0*20)
		{
			//printf("%d:	Had a chat with all %d switches (%x)\n",cid,i,x);
			x = 0;
		}
	}
}

void latencyTest(unsigned len)
{
	unsigned i, tv1, tv2, tmp, res[64];
	timer t;
	for (i = 0; i < len; i += 2)
	{
		t :> tv1;
		read_sswitch_reg(i,0x5,tmp);
		t :> tv2;
		res[i] = tv2-tv1;
	}
	for (i = 1; i < len; i += 2)
	{
		t :> tv1;
		read_sswitch_reg(i,0x5,tmp);
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
    register int a,b,c=0x55555555,d=0x5555555,e=0x5555555,f=0x5555555;
    while(1)
    {
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
    }
}

void mulkernelb(void)
{
    register int a,b,c=0xaaaaaaaa,d=0xaaaaaaaa,e=0xaaaaaaaa,f=0xaaaaaaaa;
    while(1)
    {
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
        asm("lmul %0,%1,%2,%3,%4,%5":"=r"(a),"=r"(b):"r"(c),"r"(d),"r"(e),"r"(f));
    }
}

void racetrack(chanend cin, chanend cout, unsigned cid)
{
	unsigned char b = 1;
	timer t;
	unsigned tv;
	if (cid == 0 || cid == 79)
	{
		outByte(cout,b);
	}
	while(1)
	{
		b = inByte(cin);
		if (cid == 0)
		{
			b = (b+1) & 0xf;
			if (b == 0) b = 1;
		}
		leds1 <: b;
		t :> tv;
		t when timerafter(tv + 0x00200000) :> void;
		leds1 <: 0;
		outByte(cout,b);
	}
}

void commSpeed(chanend c, unsigned role)
{
	unsigned tv1, tv2, tt, i = 0, tests=32;
	timer t;
	while(1)
	{
		if (!role)
		{
			//closeChanend(c);
			t :> tv1;
			outUint(c,0);
			//closeChanend(c);
			inUint(c);
			t :> tv2;
			tt += tv2-tv1;
			if (++i == tests)
			{
				break;
			}
		}
		else
		{
			//closeChanend(c);
			inUint(c);
			//closeChanend(c);
			outUint(c,1);
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
