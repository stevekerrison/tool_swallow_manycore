#ifndef _LEDTEST_H
#define _LEDTEST_H

#include "mcsc_chan.h"

void doled(void);

void switchChat(unsigned i, unsigned max);

void testComms(chanend c, unsigned role);

void commSpeed(chanend c, unsigned role);

void latencyTest(unsigned len);

void nonsense(unsigned x);

void racetrack(chanend cin, chanend cout, unsigned cid);

void mulkernela(void);
void mulkernelb(void);

#endif //_LEDTEST_H
