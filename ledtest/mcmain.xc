#include <platform.h>
#include "ledtest.h"
#include "chan.h"

int main(void)
{
	par
	{
		on stdcore[1]: doled();
	}
	return 0;
}
