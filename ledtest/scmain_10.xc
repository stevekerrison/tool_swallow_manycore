/************* UNUSED CORE 14***************/
#include <platform.h>
#include "ledtest.h"
#include "chan.h"
#include <stdio.h>

/* __initLinks for core 14*/
void __initLinks()
{
	unsigned myid = 14, jtagid= 10,i;
	unsigned nlinks=5,tv,c;
	timer t;
	unsigned links[5] = {0x87,0x85,0x86,0x84,0x82,};
	/* Set my core ID */
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	resetChans();
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0);
	}
	/* Enable all links for now... */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0xc0001002);
	}
	t :> tv;
	t when timerafter(tv + 1600000-(100000*jtagid)) :> void;
	//Route configuration
	write_sswitch_reg_no_ack(myid,0x0c,0x00001101);
	write_sswitch_reg_no_ack(myid,0x0d,0x00000000);
	//Attach links to routes
	write_sswitch_reg_no_ack(myid,0x22,0x00000000);
	write_sswitch_reg_no_ack(myid,0x23,0x00000400);
	write_sswitch_reg_no_ack(myid,0x24,0x00000100);
	write_sswitch_reg_no_ack(myid,0x25,0x00000100);
	write_sswitch_reg_no_ack(myid,0x26,0x00000100);
	write_sswitch_reg_no_ack(myid,0x27,0x00000100);

	/* Issue hello and wait for credit on active links */
	for (i = 0; i < nlinks; i += 1)
	{
		resetChans();
		//printf("%d[%d]:	Bringing up link 0x%02x\n",myid,jtagid,links[i]);
		write_sswitch_reg_no_ack(myid,links[i],0xc1001002);
		tv = 0;
		c = 0;
		while((tv & 0x0c000000) != 0x04000000)
		{
			if (tv & 0x08000000)
			{
				/*write_sswitch_reg_no_ack(myid,links[i],0xc0801002);
				write_sswitch_reg_no_ack(myid,links[i],0xc1001002);*/
				printf("%d[%d]:	Link error on 0x%02x, retry\n",myid,jtagid,links[i]);
				write_sswitch_reg_no_ack(myid,links[i],0xc1801002);
				/*printf("%d[%d]:	Link error on 0x%02x, bailing\n",myid,jtagid,links[i]);
				return; //GTFO*/
			}
			read_sswitch_reg(myid,links[i],tv);
			if (c++ > 200000)
			{
				printf("%d[%d]:	Link error on 0x%02x, fail! (%d/%d) initialised\n",myid,jtagid,links[i],i,nlinks);
				return;
			}
		}
		write_sswitch_reg_no_ack(myid,links[i],0xc1001002);
		//printf("%d[%d]:	0x%02x is up!\n",myid,jtagid,links[i]);
	}
	printf("%d[%d]:	Links initialised!\n",myid,jtagid);

	return;
}

/* Main for core 14*/
int main(void)
{
	__initLinks();
	par
	{
		while(1);//asm("freet"::);

	}
	return 0;
}
