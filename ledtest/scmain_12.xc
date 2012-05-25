/************* CORE 13 ***************/
#include <platform.h>
#include "ledtest.h"
#include "chan.h"
#include <stdio.h>

/* __initLinks for core 13*/
void __initLinks()
{
	unsigned myid = 13, jtagid= 12,i;
	unsigned nlinks=5,tv,c;
	timer t;
	unsigned links[5] = {0x87,0x85,0x86,0x84,0x83,};
	/* Set my core ID */
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	resetChans();
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0);
	}
	/* Enable all just internal links for now... */
	for (i = 0; i < 4; i += 1)
	{
		write_sswitch_reg_no_ack(myid,links[i],0x80020040);
	}
	//Route configuration
	write_sswitch_reg_no_ack(myid,0x0c,0x00000010);
	write_sswitch_reg_no_ack(myid,0x0d,0x00000000);
	//Attach links to routes
	write_sswitch_reg_no_ack(myid,0x22,0x00000500);
	write_sswitch_reg_no_ack(myid,0x23,0x00000100);
	write_sswitch_reg_no_ack(myid,0x24,0x00000000);
	write_sswitch_reg_no_ack(myid,0x25,0x00000000);
	write_sswitch_reg_no_ack(myid,0x26,0x00000000);
	write_sswitch_reg_no_ack(myid,0x27,0x00000000);

	/* Issue hello and wait for credit on active links */
	for (i = 0; i < 4; i += 1)
	{
		resetChans();
		//printf("%d[%d]:	Bringing up link 0x%02x\n",myid,jtagid,links[i]);
		write_sswitch_reg_no_ack(myid,links[i],0x81020040);
		tv = 0;
		c = 0;
		while((tv & 0x0e000000) != 0x06000000)
		{
			if (c++ > 200) //wait a while
			{
				//Hmmm, we haven't got full-duplex linkage, let's try again
				//printf("%d[%d]:	Timeout on 0x%02x, retry\n",myid,jtagid,links[i]);
				write_sswitch_reg_no_ack(myid,links[i],0x81020040);
				c = 0;
			}

			read_sswitch_reg(myid,links[i],tv);
		}
		//write_sswitch_reg_no_ack(myid,links[i],0x81020040);
		//printf("%d[%d]:	0x%02x is up!\n",myid,jtagid,links[i]);
	}
	/* Now do external links */
	resetChans();
	for (i = 4; i < nlinks; i += 1)
	{
		write_sswitch_reg_no_ack(myid,links[i],0x80020040);
	}
	return;
	for (i = 4; i < nlinks; i += 1)
	{
		if (links[i] == 0x82) //First thing link A does it HELLO
		{
			write_sswitch_reg_no_ack(myid,links[i],0x81020040);
			//printf("%d[%d]: Link A says hello in the first stage\n",myid,jtagid);
		}
		else if (links[i] == 0x83) //First thing link B is wait on HELLO
		{
			tv = 0;
			c = 0;
			while((tv & 0x0c000000) != 0x04000000)
			{
				if (tv & 0x08000000)
				{
					printf("%d[%d]: FAIL\n",myid,jtagid);
					return;
				}
				read_sswitch_reg(myid,links[i],tv);
				if (c++ > 200000)
				{
					printf("%d[%d]:	Link B gave up in first stage\n",myid,jtagid);
				}
			}
		}
	}
	for (i = 4; i < nlinks; i += 1)
	{
		if (links[i] == 0x83) //Second thing link A does it HELLO
		{
			write_sswitch_reg_no_ack(myid,links[i],0x81020040);
			printf("%d[%d]: Link B says hello in the second stage\n",myid,jtagid);
		}
		else if (links[i] == 0x82) //Second thing link B is wait on HELLO
		{
			tv = 0;
			c = 0;
			while((tv & 0x0c000000) != 0x04000000)
			{
				if (tv & 0x08000000)
				{
					printf("%d[%d]: FAIL IT\n",myid,jtagid);
					return;
				}
				read_sswitch_reg(myid,links[i],tv);
				if (c++ > 200000)
				{
					printf("%d[%d]:	Link A gave up in first stage\n",myid,jtagid);
				}
			}
		}
	}
	//printf("%d[%d]:	DONE!\n",myid,jtagid);

	return;
}

/* Main for core 13*/
int main(void)
{
	__initLinks();
	par
	{
		doled();

	}
	return 0;
}
