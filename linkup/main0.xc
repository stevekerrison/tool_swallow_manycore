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

void __initlinks()
{
	timer t;
	unsigned myid = 1;
	unsigned c, dst = 0x00000102,tv;
	//asm("freer res[%0]"::"r"(c));
	write_sswitch_reg_no_ack(0,XS1_L_SSWITCH_NODE_ID_NUM,myid);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION0_NUM,0);
	write_sswitch_reg(myid,XS1_L_SSWITCH_DIMENSION_DIRECTION1_NUM,0);
	write_sswitch_reg(myid,XLINK_D_DN,0);
	write_sswitch_reg(myid,XLINK_D_STW,0x80002004);
	read_sswitch_reg(myid,XLINK_D_STW,tv);
	printf("%d: 0x%08x\n",myid,tv);
	t :> tv;
	tv += 100000000;
	t when timerafter(tv) :> void;
	c = getChanend(dst);
	printf("%d: 0x%08x\n",myid,c);
	asm("in %0,res[%1]":"=r"(c):"r"(tv));
	printf("%08x\n",tv);
	freeChanend(c);
}

int main(void)
{
	__initlinks();
	return 0;
}
