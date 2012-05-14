#include <platform.h>

out port ledc0 	 = XS1_PORT_4F;

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


int main()
{
	c0();
	return 0;
}
