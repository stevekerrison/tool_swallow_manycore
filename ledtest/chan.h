#ifndef _CHAN_H
#define _CHAN_H

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


unsigned getChanend(unsigned dst);
void resetChans(void);
void cResetChans(unsigned myid);
void txCloseChan(unsigned c);
void rxCloseChan(unsigned c);
void freeChanend(unsigned c);
#endif //_CHAN_H
