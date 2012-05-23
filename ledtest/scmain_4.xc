/************* UNUSED CORE 2***************/

#include <platform.h>
#include <xs1.h>
#include "chan.h"

/* __initLinks for core 2*/
void __initLinks()
{
	unsigned myid = 2, i,tv,c;
	/* Set my core ID */
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	/* Make sure all channels unallocated */
	resetChans();
	/* Zero out the link registers */
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0);
	}
	/* Now allocate the channels needed by this core, setup the links and
		routing tables */
	//Link enabling
	write_sswitch_reg_no_ack(myid,0x85,0x80001002);
	write_sswitch_reg_no_ack(myid,0x87,0x80001002);
	write_sswitch_reg_no_ack(myid,0x84,0x80001002);
	write_sswitch_reg_no_ack(myid,0x82,0x80001002);
	write_sswitch_reg_no_ack(myid,0x86,0x80001002);
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
	//Issue HELLO on active links
	write_sswitch_reg_no_ack(myid,0x85,0x81001002);
	write_sswitch_reg_no_ack(myid,0x87,0x81001002);
	write_sswitch_reg_no_ack(myid,0x84,0x81001002);
	write_sswitch_reg_no_ack(myid,0x82,0x81001002);
	write_sswitch_reg_no_ack(myid,0x86,0x81001002);
	//Wait for credit
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x85,tv); }
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x87,tv); }
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x84,tv); }
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x82,tv); }
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x86,tv); }
	//Reissue HELLOs
	write_sswitch_reg_no_ack(myid,0x85,0x81001002);
	write_sswitch_reg_no_ack(myid,0x87,0x81001002);
	write_sswitch_reg_no_ack(myid,0x84,0x81001002);
	write_sswitch_reg_no_ack(myid,0x82,0x81001002);
	write_sswitch_reg_no_ack(myid,0x86,0x81001002);
	//Hopefully we're done!
	cResetChans(myid);

	return;
}

/* Main for core 2*/
int main(void)
{
	__initLinks();
	par
	{
		asm("freet"::);

	}
	return 0;
}
