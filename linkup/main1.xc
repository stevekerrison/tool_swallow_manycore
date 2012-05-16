#include <platform.h>
#include <stdio.h>

/* Switch registers... */
/* XLINK_X_STW: Speed Timing and Width */
#define XLINK_A_STW XS1_L_SSWITCH_XLINK_2_NUM
#define XLINK_B_STW XS1_L_SSWITCH_XLINK_3_NUM
#define XLINK_C_STW XS1_L_SSWITCH_XLINK_0_NUM
#define XLINK_D_STW XS1_L_SSWITCH_XLINK_1_NUM
#define XLINK_E_STW XS1_L_SSWITCH_XLINK_6_NUM
#define XLINK_F_STW XS1_L_SSWITCH_XLINK_7_NUM
#define XLINK_G_STW XS1_L_SSWITCH_XLINK_4_NUM
#define XLINK_H_STW XS1_L_SSWITCH_XLINK_5_NUM
/* XLINK_X_DN: Direction and Network */
#define XLINK_A_DN XS1_L_SSWITCH_SLINK_2_NUM
#define XLINK_B_DN XS1_L_SSWITCH_SLINK_3_NUM
#define XLINK_C_DN XS1_L_SSWITCH_SLINK_0_NUM
#define XLINK_D_DN XS1_L_SSWITCH_SLINK_1_NUM
#define XLINK_E_DN XS1_L_SSWITCH_SLINK_6_NUM
#define XLINK_F_DN XS1_L_SSWITCH_SLINK_7_NUM
#define XLINK_G_DN XS1_L_SSWITCH_SLINK_4_NUM
#define XLINK_H_DN XS1_L_SSWITCH_SLINK_5_NUM

unsigned getChanend(unsigned dst); //ASM
#define freeChanend(c) asm("freer res[%0]"::"r"(c));
void outChanend(unsigned c, unsigned d)
{
	asm("out res[%0],%1"::"r"(c),"r"(d));
}

void __initlinks()
{
	timer t;
	unsigned myid = 0;
	unsigned c, dst = 0x00010102, tv;
	//asm("freer res[%0]"::"r"(c));
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION0_NUM,0);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION1_NUM,0);
	write_sswitch_reg(myid,XLINK_A_DN,0);
	write_sswitch_reg(myid,XLINK_A_STW,0x80802004);
	write_sswitch_reg(myid,XLINK_E_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_F_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_G_STW,0x00002004);
	write_sswitch_reg(myid,XLINK_H_STW,0x00002004);
	read_sswitch_reg(0,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	printf("%d: 0x%08x\n",myid,tv);
	read_sswitch_reg(1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	printf("%d: 0x%08x\n",myid,tv);
	/*read_sswitch_reg(myid,XLINK_D_ST
	//read_sswitch_reg(1,XS1_L_SSWITCH_NODE_ID_NUM,tv);
	//printf("%d: 0x%08x\n",myid,tv);
	/*read_sswitch_reg(myid,XLINK_A_STW,tv);
	printf("%d: 0x%08x\n",myid,tv);
	t :> tv;
	tv += 100000000;
	t when timerafter(tv) :> void;
	c = getChanend(dst);
	printf("%d: 0x%08x\n",myid,c);
	tv = 0xf00df33d;
	outChanend(c,tv);
	printf("C: %08x\n",c);
	freeChanend(c);*/
}

int main(void)
{
	__initlinks();
	return 0;
}
