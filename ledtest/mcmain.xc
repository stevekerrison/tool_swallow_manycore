#include <platform.h>
#include "ledtest.h"
#include "chan.h"

int main(void)
{
	par
	{
		on stdcore[1]: doled();
		on stdcore[3]: doled();
		on stdcore[5]: doled();
		on stdcore[7]: doled();
		on stdcore[9]: doled();
		on stdcore[11]: doled();
		on stdcore[13]: doled();
		on stdcore[15]: doled();
	}
	return 0;
}
