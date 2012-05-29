#include <platform.h>
#include "ledtest.h"
#include "chan.h"

int main(void)
{
	chan c[2];
	par
	{
		on stdcore[0]: doled();
		//on stdcore[1]: commSpeed(c[1],0);
		//on stdcore[1]: testComms(c[0],0);
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
		//on stdcore[30]: commSpeed(c[1],1);
		on stdcore[31]: doled();
		//on stdcore[31]: testComms(c[0],1);
		//on stdcore[2]: switchChat(0,0);
		on stdcore[0]: switchChat(0,32);
		on stdcore[1]: switchChat(0,32);
		on stdcore[2]: switchChat(0,32);
		on stdcore[3]: switchChat(0,32);
		on stdcore[4]: switchChat(0,32);
		on stdcore[5]: switchChat(0,32);
		on stdcore[6]: switchChat(0,32);
		on stdcore[7]: switchChat(0,32);
		on stdcore[8]: switchChat(0,32);
		on stdcore[9]: switchChat(0,32);
		on stdcore[10]: switchChat(0,32);
		on stdcore[11]: switchChat(0,32);
		on stdcore[12]: switchChat(0,32);
		on stdcore[13]: switchChat(0,32);
		on stdcore[14]: switchChat(0,32);
		on stdcore[15]: switchChat(0,32);
		on stdcore[16]: switchChat(0,32);
		on stdcore[17]: switchChat(0,32);
		on stdcore[18]: switchChat(0,32);
		on stdcore[19]: switchChat(0,32);
		on stdcore[20]: switchChat(0,32);
		on stdcore[21]: switchChat(0,32);
		on stdcore[22]: switchChat(0,32);
		on stdcore[23]: switchChat(0,32);
		on stdcore[24]: switchChat(0,32);
		on stdcore[25]: switchChat(0,32);
		on stdcore[26]: switchChat(0,32);
		on stdcore[27]: switchChat(0,32);
		on stdcore[28]: switchChat(0,32);
		on stdcore[29]: switchChat(0,32);
		on stdcore[30]: switchChat(0,32);
		on stdcore[31]: switchChat(0,32);
		/*on stdcore[24]: switchChat(16,32);*/
	}
	return 0;
}
