#include <platform.h>
#include "ledtest.h"
#include "chan.h"

#define NCORES 80

int main(void)
{
	chan c[NCORES];
	//chan d[17];
	/*par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: commSpeed(c[(i+1) >> 1],i & 1);
		on stdcore[(i+16)%NCORES]: commSpeed(c[(i+1) >> 1],(i + 1) & 1);
	}*/
	/*par (int i = 0; i < 32; i += 1)
	{
		on stdcore[i]: commSpeed(d[(i+1) >> 1],i & 1);
		on stdcore[(i+4)%32]: commSpeed(d[(i+1) >> 1],(i + 1) & 1);
	}*/
	/*par (int i = 0; i < NCORES; i += 4)
	{
		on stdcore[i]: doled();
		on stdcore[i+3]: doled();
	}*/
	par (int i = 0; i < (NCORES>>2); i += 1)
	{
		on stdcore[i*4]: racetrack(c[i],c[i+1]);
		on stdcore[(i*4)+3]: racetrack(c[i+1],c[(i+2)%(NCORES>>1)]);
	}
	return 0;
}
