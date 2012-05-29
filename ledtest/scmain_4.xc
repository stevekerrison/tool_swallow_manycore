/************* CORE 2 ***************/
#include <platform.h>
#include "ledtest.h"
#include "chan.h"
#include <stdio.h>

/* __initLinks for core 2*/
void __initLinks()
{
	unsigned myid = 2, jtagid= 4, i;
	unsigned nlinks=5,tv,c,linksetting = 0xc0000800;
	timer t;
	unsigned links[5] = {0x87,0x85,0x86,0x84,0x82,};
	/* Set my core ID */
	write_sswitch_reg_no_ack_clean(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	cResetChans(myid);
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack_clean(myid,i,0);
	}
	/* Enable all links */
	for (i = 0; i < nlinks; i += 1)
	{
		write_sswitch_reg_no_ack_clean(myid,links[i],linksetting);
	}
	//Route configuration
	write_sswitch_reg_no_ack_clean(myid,0x0c,0x00011101);
	write_sswitch_reg_no_ack_clean(myid,0x0d,0x00000000);
	//Attach links to routes
	write_sswitch_reg_no_ack_clean(myid,0x22,0x00000000);
	write_sswitch_reg_no_ack_clean(myid,0x23,0x00000400);
	write_sswitch_reg_no_ack_clean(myid,0x24,0x00000100);
	write_sswitch_reg_no_ack_clean(myid,0x25,0x00000100);
	write_sswitch_reg_no_ack_clean(myid,0x26,0x00000100);
	write_sswitch_reg_no_ack_clean(myid,0x27,0x00000100);

	/* Issue hello and wait for credit on active links */
	for (i = 0; i < nlinks; i += 1)
	{
		write_sswitch_reg_no_ack_clean(myid,links[i],linksetting | 0x01000000);
		tv = 0;
		c = 0;
		while((tv & 0x0e000000) != 0x06000000)
		{
			if (tv & 0x08000000)
			{
				printf ("%d[%d]:	LINK ERROR ON 0x%02x\n",myid,jtagid,links[i]);
				write_sswitch_reg_no_ack_clean(myid,links[i],0x00800000);
				write_sswitch_reg_no_ack_clean(myid,links[i],linksetting);
				write_sswitch_reg_no_ack_clean(myid,links[i],linksetting | 0x01000000);
			}
			else if ((++c % 2000) == 0) //wait a while
			{
				//Hmmm, we haven't got full-duplex linkage, let's try again
				//printf ("%d[%d]:	Link retry 0x%02x\n",myid,jtagid,links[i]);
				if (c > 2000 * 10)
				{
					write_sswitch_reg_no_ack_clean(myid,links[i],0x00800000);
					write_sswitch_reg_no_ack_clean(myid,links[i],linksetting);
				}
				write_sswitch_reg_no_ack_clean(myid,links[i],linksetting | 0x01000000);
			}

			read_sswitch_reg(myid,links[i],tv);
		}
	}
	/* Now we declare any channels we need */

	/* Give the channels long enough to setup */
	t :> tv;
	t when timerafter(tv + 10000000) :> void;
	return;
}

/* Main for core 2*/
int main(void)
{
	__initLinks();
	par
	{
		switchChat(0,32);

	}
	return 0;
}
