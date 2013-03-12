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

#define NCORES (16*6)
int main(void)
{

  chan c[NCORES];
  
/*  chan x;
  par
  {
    on stdcore[0]: basicTest(x,0);
    on stdcore[1]: basicTest(x,1);
  }*/
  
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: scopetest(i);
  }*/
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: tokenscope(c[i],c[(i+1)%NCORES],i);
  }*/
  /*par
  {
    on stdcore[0] : bwah(c[0],9);
    on stdcore[9] : bwah(c[0],0);
  }*/
  //Do some RTT testing between cores 15 *logical* nodes apart
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: commSpeed(c[i],i & 1);
    on stdcore[(i+15)%NCORES]: commSpeed(c[i],(i + 1) & 1);
  }*/
  
  //Do some RTT testing between cores 1 *logical* node apart
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: commSpeed(c[i+NCORES],i & 1);
    on stdcore[(i+1)%NCORES]: commSpeed(c[i+NCORES],(i + 1) & 1);
  }*/
  
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: doled();
  }
  
  par
  {
    on stdcore[80]: doled();
  }*/

  //Flash the LEDs on the appropriate cores (because not all cores have them)
  /*par (int i = 0; i < NCORES; i += 4)
  {
    on stdcore[i]: doled();
    on stdcore[i+3]: doled();
  }*/
  
  //Fill each core's pipeline with some CPU-burning code
  par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: mulkernela();
    on stdcore[i]: mulkernelb();
    on stdcore[i]: mulkernela();
    on stdcore[i]: mulkernelb();
  }
  
  /*par
  {
    on stdcore[2]: dynamic_linkup(2);
  }*/
  
  //Splat some values out of the LEDs with a token passed around
  /*par (int i = 0; i < (NCORES>>1); i += 2)
  {
    on stdcore[(i>>1)*4]: racetrack(c[i],c[i+1],(i>>1)*4);
    on stdcore[((i>>1)*4)+3]: racetrack(c[i+1],c[(i+2)%(NCORES>>1)],((i>>1)*4)+3);
  }*/
  /*par {
    on stdcore[47] : testa(c[0]);
    on stdcore[48] : testb(c[0]);
  }*/
  
  /*par
  {
    on stdcore[0]: racetrack(c[0],c[1],0);
    on stdcore[2]: racetrack(c[1],c[0],2);
  }*/
  
  par (int i = 0; i < NCORES/2 - 1; i += 1)
  {
    on stdcore[i*2]:  racetrack(c[i],c[i+1],i*2);
  }
  par (int i = NCORES-2; i < NCORES - 1; i += 1)
  {
    on stdcore[i]: racetrack(c[i/2],c[0],i);
  }
  
  //Generate traffic between switches. This loads up the network a lot.
  par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: switchChat(NCORES,NCORES,i);
  }
  
  //Generate traffic between switches. This loads up the network a lot.
  //Ideally nothing should crash or deadlock.
  /*par (int i = 0; i < NCORES; i += 1)
  {
    on stdcore[i]: switchChat(4,NCORES,i);
  }*/
  /*
  //Next three par{}s: Circular LED racetrack (TODO: Generalise for NCORES != 80)
  par (int i = 7; i < NCORES-4; i += 4)
  {
    on stdcore[((i>>2)*4)+3]: racetrack(c[(i>>2)],c[(i>>2)+1],((i>>2)*4)+3);
  }
  par (int i = 5; i < NCORES-4; i += 4)
  {
    on stdcore[((i>>2)*4)]: racetrack(c[(i>>2)+1+(NCORES>>2)],c[(i>>2)+(NCORES>>2)],((i>>2)*4));
  } */
  /*par
  {
    on stdcore[0]: racetrack(c[21],c[20],0);
    on stdcore[3]: racetrack(c[20],c[1],3);
    on stdcore[79]: racetrack(c[19],c[40],79);
    on stdcore[76]: racetrack(c[40],c[39],76);
  }*/
  //End circular LED racetrack
 
  return 0;
}
