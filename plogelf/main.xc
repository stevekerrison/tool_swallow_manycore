#include <platform.h>

on stdcore[1]: out port ledc1	 = XS1_PORT_4D;
on stdcore[0]: out port ledc0 	 = XS1_PORT_4F;

void c0()
{
	unsigned tv, ledv = 0;
	timer t;
	t :> tv;
	while(1) {
		ledv = 1 - ledv;
		tv += 20000000;
		t when timerafter(tv) :> void;
		ledc0 <: ledv;
	}
}

void c1()
{
	unsigned tv, ledv = 0;
	timer t;
	t :> tv;
	while (1)
	{
		tv += 20000000;
		ledv = 1 - ledv;
		t when timerafter(tv) :> void;
		ledc1 <: ledv;
	}
}

int main()
{
	par
	{
		on stdcore[1]: c1();
		on stdcore[0]: c0();
	}
	return 0;
}
