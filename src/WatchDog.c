#include"../include/WatchDog.h"
static int init_SuperIo()
{

	if (ioperm(EFER, 2, 1) != 0) 
	{
		perror("ioperm error.\n");
		exit(-1);
	}
	outb(EEFM, EFER);
	outb(EEFM, EFER);
	
	outb(EFIR, EFER);
	outb(WTMR, EFDR);	
	return 0;

	
}

void open_watchdog()
{
	init_SuperIo();
	outb(WTVR, EFER);
	outb(TIMEOUT, EFDR);
	
	outb(EFQR,EFER);

}


void feed_watchdog(unsigned char time)
{
	
	init_SuperIo();
	outb(WTVR, EFER);
	outb(time, EFDR);
	
	outb(EFQR,EFER);
}

void clsoe_watchdog()
{
	
	init_SuperIo();
	outb(WTVR, EFER);
	outb(0, EFDR);
	
	outb(EFQR,EFER);
}	



