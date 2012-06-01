#include <platform.h>
#include "ledtest.h"
#include "chan.h"

int main(void)
{
	chan c[17];
	//chan d[17];
	/*par (int i = 0; i < 32; i += 1)
	{
		on stdcore[i]: commSpeed(c[(i+1) >> 1],i & 1);
		on stdcore[(i+16)%32]: commSpeed(c[(i+1) >> 1],(i + 1) & 1);
	}*/
	/*par (int i = 0; i < 32; i += 1)
	{
		on stdcore[i]: commSpeed(d[(i+1) >> 1],i & 1);
		on stdcore[(i+4)%32]: commSpeed(d[(i+1) >> 1],(i + 1) & 1);
	}*/
	par (int i = 0; i < 48; i += 4)
	{
		on stdcore[i]: doled();
		on stdcore[i+3]: doled();
	}
	return 0;
}
