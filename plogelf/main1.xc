#include <platform.h>

out port ledc1	 = XS1_PORT_4D;

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
	c1();
	return 0;
}
