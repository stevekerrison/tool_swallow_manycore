#ifndef _LEDTEST_H
#define _LEDTEST_H

#include "chan.h"

void doled(void);

void switchChat(unsigned i, unsigned max);

void testComms(chanend c, unsigned role);

void commSpeed(chanend c, unsigned role);

#endif //_LEDTEST_H
