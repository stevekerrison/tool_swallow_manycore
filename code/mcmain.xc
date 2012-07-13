/*
 * mcmain - A sample multicore main file for an XMP16 array
 * 
 * Copyright (C) 2012 Steve Kerrison <github@stevekerrison.com>
 *
 * This software is freely distributable under a derivative of the
 * University of Illinois/NCSA Open Source License posted in
 * LICENSE.txt and at <http://github.xcore.com/>
 */

//Required declaration in an XMP16 multicore main before #include mcsc_chan.h!
#include <platform.h>
#define MCMAIN
#include "mcsc_chan.h"

//Other includes must follow mcsc_chan.h
#include "ledtest.h"

#define NCORES 4

int main(void)
{

	chan c[NCORES*2];
	//Do some RTT testing between cores 15 *logical* nodes apart
	/*par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: commSpeed(c[i],i & 1);
		on stdcore[(i+15)%NCORES]: commSpeed(c[i],(i + 1) & 1);
	}*/
	
	//Do some RTT testing between cores 1 *logical* node apart
	par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: commSpeed(c[i+NCORES],i & 1);
		on stdcore[(i+1)%NCORES]: commSpeed(c[i+NCORES],(i + 1) & 1);
	}

	//Flash the LEDs on the appropriate cores (because not all cores have them)
	/*par (int i = 0; i < NCORES; i += 4)
	{
		on stdcore[i]: doled();
		on stdcore[i+3]: doled();
	}*/
	
	//Fill each core's pipeline with some CPU-burning code
	/*par (int i = 0; i < NCORES; i += 1)
	{
		on stdcore[i]: mulkernela();
		on stdcore[i]: mulkernelb();
		on stdcore[i]: mulkernela();
		on stdcore[i]: mulkernelb();
	}*/
	
	//Splat some values out of the LEDs with a token passed around
	par (int i = 0; i < (NCORES>>1); i += 2)
	{
		on stdcore[(i>>1)*4]: racetrack(c[i],c[i+1],(i>>1)*4);
		on stdcore[((i>>1)*4)+3]: racetrack(c[i+1],c[(i+2)%(NCORES>>1)],((i>>1)*4)+3);
	}
	
	//Generate traffic between switches. This loads up the network a lot.
	//Ideally nothing should crash. At the moment it causes ET_ILLEGAL_RESOURCE
	//sometimes. Obvious TODO: FIXME!
	/*par (int i = 0; i < NCORES; i += 1)
	{
	  on stdcore[i]: switchChat(0,NCORES);
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
	}
	par
	{
		on stdcore[0]: racetrack(c[21],c[20],0);
		on stdcore[3]: racetrack(c[20],c[1],3);
		on stdcore[79]: racetrack(c[19],c[40],79);
		on stdcore[76]: racetrack(c[40],c[39],76);
	}
	//End circular LED racetrack
	*/
	return 0;
}
