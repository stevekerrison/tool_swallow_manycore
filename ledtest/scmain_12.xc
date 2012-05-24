/************* UNUSED CORE 13***************/
#include <platform.h>
#include "ledtest.h"
#include "chan.h"
#include <stdio.h>

/* __initLinks for core 13*/
void __initLinks()
{
	unsigned myid = 13, jtagid= 12,i,tv,c;
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
	write_sswitch_reg_no_ack(myid,0x85,0xc0000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0000000,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc0000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0000000,0x87);
	write_sswitch_reg_no_ack(myid,0x84,0xc0000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0000000,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc0000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0000000,0x86);
	//Route configuration
	write_sswitch_reg_no_ack(myid,0x0c,0x00000010);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x10,0xc);
	write_sswitch_reg_no_ack(myid,0x0d,0x00000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0xd);
	//Attach links to routes
	write_sswitch_reg_no_ack(myid,0x22,0x00000500);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x500,0x22);
	write_sswitch_reg_no_ack(myid,0x23,0x00000100);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x100,0x23);
	write_sswitch_reg_no_ack(myid,0x24,0x00000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0x24);
	write_sswitch_reg_no_ack(myid,0x25,0x00000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0x25);
	write_sswitch_reg_no_ack(myid,0x26,0x00000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0x26);
	write_sswitch_reg_no_ack(myid,0x27,0x00000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0x0,0x27);
	//Issue HELLO on active links
	write_sswitch_reg_no_ack(myid,0x85,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x87);
	write_sswitch_reg_no_ack(myid,0x84,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x86);
	//Wait for credit
	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x85,0xc0000000);
		}
		read_sswitch_reg(myid,0x85,tv);
	}
	printf("%d[%d]:	Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x85);
	printf("%d[%d]:	Got initial credits for %02x after %d attempts\n",myid,jtagid,0x85,i);
	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x87,0xc0000000);
		}
		read_sswitch_reg(myid,0x87,tv);
	}
	printf("%d[%d]:	Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x87);
	printf("%d[%d]:	Got initial credits for %02x after %d attempts\n",myid,jtagid,0x87,i);
	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x84,0xc0000000);
		}
		read_sswitch_reg(myid,0x84,tv);
	}
	printf("%d[%d]:	Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x84);
	printf("%d[%d]:	Got initial credits for %02x after %d attempts\n",myid,jtagid,0x84,i);
	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x86,0xc0000000);
		}
		read_sswitch_reg(myid,0x86,tv);
	}
	printf("%d[%d]:	Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x86);
	printf("%d[%d]:	Got initial credits for %02x after %d attempts\n",myid,jtagid,0x86,i);
	//Reissue HELLOs
	write_sswitch_reg_no_ack(myid,0x85,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x85);
	write_sswitch_reg_no_ack(myid,0x87,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x87);
	write_sswitch_reg_no_ack(myid,0x84,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x84);
	write_sswitch_reg_no_ack(myid,0x86,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x86);
	//Link enabling
	write_sswitch_reg_no_ack(myid,0x83,0xc0000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc0000000,0x83);
	//Issue HELLO on active links
	write_sswitch_reg_no_ack(myid,0x83,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x83);
	//Wait for credit
	tv = 0;
	i = 1;
	while((tv & 0x0c000000) != 0x04000000)
	{
		i++;
		if (tv & 0x08000000)
		{
			write_sswitch_reg_no_ack(myid,0x83,0xc0000000);
		}
		read_sswitch_reg(myid,0x83,tv);
	}
	printf("%d[%d]:	Read 0x%08x from 0x%02x\n",myid,jtagid,tv,0x83);
	printf("%d[%d]:	Got initial credits for %02x after %d attempts\n",myid,jtagid,0x83,i);
	//Reissue HELLOs
	write_sswitch_reg_no_ack(myid,0x83,0xc1000000);
	printf("%d[%d]:	Written 0x%08x to 0x%02x\n",myid,jtagid,0xc1000000,0x83);
	//Hopefully we're done!
	printf("%d[%d]:	Done link initialisation!\n",myid,jtagid);

	return;
}

/* Main for core 13*/
int main(void)
{
	__initLinks();
	par
	{
		asm("freet"::);

	}
	return 0;
}
