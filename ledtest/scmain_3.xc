/************* UNUSED CORE 0***************/
#include <platform.h>
#include "ledtest.h"
#include "chan.h"
#include <stdio.h>

/* __initLinks for core 0*/
void __initLinks()
{
	unsigned myid = 0, jtagid= 3,i,tv,c;
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
	write_sswitch_reg_no_ack(myid,0x85,0xc0004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0004008,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc0004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0004008,0x87);
	write_sswitch_reg_no_ack(myid,0x83,0xc0004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0004008,0x83);
	write_sswitch_reg_no_ack(myid,0x84,0xc0004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0004008,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc0004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0004008,0x86);
	//Route configuration
	write_sswitch_reg_no_ack(myid,0x0c,0x00003311);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x3311,0xc);
	write_sswitch_reg_no_ack(myid,0x0d,0x00000000);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0xd);
	//Attach links to routes
	write_sswitch_reg_no_ack(myid,0x22,0x00000200);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x200,0x22);
	write_sswitch_reg_no_ack(myid,0x23,0x00000300);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x300,0x23);
	write_sswitch_reg_no_ack(myid,0x24,0x00000100);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x100,0x24);
	write_sswitch_reg_no_ack(myid,0x25,0x00000100);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x100,0x25);
	write_sswitch_reg_no_ack(myid,0x26,0x00000100);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x100,0x26);
	write_sswitch_reg_no_ack(myid,0x27,0x00000100);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0x100,0x27);
	//Issue HELLO on active links
	write_sswitch_reg_no_ack(myid,0x85,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x87);
	write_sswitch_reg_no_ack(myid,0x83,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x83);
	write_sswitch_reg_no_ack(myid,0x84,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x86);
	//Wait for credit
	printf("%d[%d]: Got initial credits\n",myid,jtagid);
	while(i++ < 200000);
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x85,tv); }
	printf("%d[%d]: Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x85);
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x87,tv); }
	printf("%d[%d]: Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x87);
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x83,tv); }
	printf("%d[%d]: Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x83);
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x84,tv); }
	printf("%d[%d]: Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x84);
	tv = 0; while(!(tv & 0x04000000)) { read_sswitch_reg(myid,0x86,tv); }
	printf("%d[%d]: Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x86);
	//Reissue HELLOs
	write_sswitch_reg_no_ack(myid,0x85,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x87);
	write_sswitch_reg_no_ack(myid,0x83,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x83);
	write_sswitch_reg_no_ack(myid,0x84,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc1004008);
	printf("%d[%d]: Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1004008,0x86);
	//Hopefully we're done!

	return;
}

/* Main for core 0*/
int main(void)
{
	__initLinks();
	par
	{
		asm("freet"::);

	}
	return 0;
}
