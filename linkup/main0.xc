#include <platform.h>
#include <stdio.h>

#include "chan.h"



void __initlinks()
{
	timer t;
	unsigned myid = 0, i;
	unsigned c, dst = 0x00000102,tv;

	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	resetChans();
	for (i = XS1_L_SSWITCH_XLINK_0_NUM; i <= XS1_L_SSWITCH_XLINK_7_NUM; i += 1)
	{
		write_sswitch_reg_no_ack(myid,i,0);
	}
	write_sswitch_reg_no_ack(myid,XLINK_D_STW,0x80002004);
	write_sswitch_reg_no_ack(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION0_NUM,0);
	write_sswitch_reg_no_ack(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION1_NUM,0);
	write_sswitch_reg_no_ack(myid,XLINK_D_DN,0);
	write_sswitch_reg_no_ack(myid,XLINK_D_STW,0x81002004);
	tv = 0;
	while (!(tv & 0x04000000))
	{
		read_sswitch_reg(myid,XLINK_D_STW,tv);
	}
	write_sswitch_reg_no_ack(myid,XLINK_D_STW,0x81002004);
	printf("%08x: %08x\n",myid,tv);
	printf("%08x: Done!\n",myid);
	read_sswitch_reg(1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	printf("%08x: %08x\n",myid,tv);
	while(1)
	{
		read_sswitch_reg(!myid,XS1_L_SSWITCH_NODE_ID_NUM,tv);
		printf("%08x: %08x\n",myid,tv);
	}
	return;

	//asm("freer res[%0]"::"r"(c));
	/*write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION0_NUM,0);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION1_NUM,0);
	write_sswitch_reg(myid,XLINK_A_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_B_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_C_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_E_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_F_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_G_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_H_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_D_DN,0);
	write_sswitch_reg(myid,XLINK_D_STW,0x81802004);*/
	
	/*read_sswitch_reg(0,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	printf("%d: 0x%08x\n",myid,tv);
	read_sswitch_reg(1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	printf("%d: 0x%08x\n",myid,tv);*/
	/*read_sswitch_reg(myid,XLINK_D_STW,tv);
	printf("%d: 0x%08x\n",myid,tv);
	t :> tv;
	tv += 100000000;
	t when timerafter(tv) :> void;
	c = getChanend(dst);
	printf("%d: 0x%08x\n",myid,c);
	asm("in %0,res[%1]":"=r"(c):"r"(tv));
	printf("%08x\n",tv);
	freeChanend(c);*/
}

int main(void)
{
	__initlinks();
	return 0;
}
