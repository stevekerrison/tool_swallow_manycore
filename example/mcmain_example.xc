/*
 * mcmain - A sample multicore main file for an XMP16 array
 * 
 * Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
 *
 * This software is freely distributable under a derivative of the
 * University of Illinois/NCSA Open Source License posted in
 * LICENSE.txt and at <http://github.xcore.com/>
 */

#include <platform.h>
#define MCMAIN
#include "ledtest.h"

#define NCORES (16*1)
int main(void)
{
  chan c[NCORES];
    
  //Splat some values out of the LEDs with a token passed around
  par (int i = 0; i < (NCORES>>1); i += 2)
  {
    on stdcore[(i>>1)*4]: racetrack(c[i],c[i+1],(i>>1)*4);
    on stdcore[((i>>1)*4)+3]: racetrack(c[i+1],c[(i+2)%(NCORES>>1)],((i>>1)*4)+3);
  }
 
  return 0;
}