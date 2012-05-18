#include <platform.h>
#include <stdio.h>
#include "xmp16.h"
#include "cores.h"

/*
#include blah //comment
*/

int main(void)
{
	/*chan c[8], d[1];
	chan y,z [8];*/
	/* Test loop */
	/*par (int i = 0; i < 8; i += 2)
	{
		on stdcore[i] : c0(c[i]); //Test
		on stdcore[i+1] : c1(c[i]);
	}*/
	/*par {
		on stdcore[0] : c0(y);
		on stdcore[1] : c1(y);
	}*/
	chan c;
	par {
		on stdcore[0] : c0(c[0]);
		on stdcore[1] : c1(c[0]);
	}
	return 0;
}
