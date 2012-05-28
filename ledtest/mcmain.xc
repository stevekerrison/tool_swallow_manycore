#include <platform.h>
#include "ledtest.h"
#include "chan.h"

int main(void)
{
	par
	{
		on stdcore[0]: doled();
		on stdcore[3]: doled();
		on stdcore[4]: doled();
		on stdcore[7]: doled();
		on stdcore[8]: doled();
		on stdcore[11]: doled();
		on stdcore[12]: doled();
		on stdcore[15]: doled();
		on stdcore[16]: doled();
		on stdcore[19]: doled();
		on stdcore[20]: doled();
		on stdcore[23]: doled();
		on stdcore[24]: doled();
		on stdcore[27]: doled();
		on stdcore[28]: doled();
		on stdcore[31]: doled();
		//on stdcore[2]: switchChat(0,0);
		on stdcore[3]: switchChat(0,32);
		/*on stdcore[24]: switchChat(16,32);*/
	}
	return 0;
}
