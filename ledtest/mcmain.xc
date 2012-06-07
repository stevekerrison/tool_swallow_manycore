#include <platform.h>
#include "ledtest.h"
#include "chan.h"

#define NCORES 48

int main(void)
{
	chan c[NCORES];
	//chan d[17];
	par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: commSpeed(c[(i+1) >> 1],i & 1);
		on stdcore[(i+16)%NCORES]: commSpeed(c[(i+1) >> 1],(i + 1) & 1);
	}
	/*par (int i = 0; i < 32; i += 1)
	{
		on stdcore[i]: commSpeed(d[(i+1) >> 1],i & 1);
		on stdcore[(i+4)%32]: commSpeed(d[(i+1) >> 1],(i + 1) & 1);
	}*/
	par (int i = 0; i < NCORES; i += 4)
	{
		on stdcore[i]: doled();
		on stdcore[i+3]: doled();
	}
	/*par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: mulkernela();
		on stdcore[i]: mulkernelb();
		on stdcore[i]: mulkernela();
		on stdcore[i]: mulkernelb();
	}*/
	/*par (int i = 0; i < (NCORES>>1); i += 2)
	{
		on stdcore[(i>>1)*4]: racetrack(c[i],c[i+1],(i>>1)*4);
		on stdcore[((i>>1)*4)+3]: racetrack(c[i+1],c[(i+2)%(NCORES>>1)],((i>>1)*4)+3);
	}*/
	/*par (int i = 7; i < NCORES-4; i += 4)
	{
		on stdcore[((i>>2)*4)+3]: racetrack(c[(i>>2)],c[(i>>2)+1],((i>>2)*4)+3);
	}
	par (int i = 5; i < NCORES-4; i += 4)
	{
		on stdcore[((i>>2)*4)]: racetrack(c[(i>>2)+1+(NCORES>>2)],c[(i>>2)+(NCORES>>2)],((i>>2)*4));
	}
	par
	{
		on stdcore[0]: racetrack(c[21],c[20],0);
		on stdcore[3]: racetrack(c[20],c[1],3);
		on stdcore[79]: racetrack(c[19],c[40],79);
		on stdcore[76]: racetrack(c[40],c[39],76);
	}*/
	return 0;
}
