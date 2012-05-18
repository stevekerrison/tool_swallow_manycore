#include <platform.h>
#include <stdio.h>
#include "xmp16.h"
#include "cores.h"


int main(void)
{
	chan c[8];
	par (int i = 0; i < 8; i += 2)
	{
		on stdcore[i] : c0(c[i]);
		on stdcore[i+1] : c1(c[i]);
	}
	return 0;
}
