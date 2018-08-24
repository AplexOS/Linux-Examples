#include <sys/io.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include"../include/WatchDog.h"
int args_correctly = 0;
//User use function
static void printUsage(char *progName) 
{
	fprintf(stderr,
			"Usage: sudo %s  [options]\n", progName);
	fprintf(stderr,
			"\n"
			"Options:\n"
			"  -s               Start the watchdog, set the default value(60s)\n" 
			"  -p               Disables the Watchdog Timer function.\n"
			"  -f   <Integer>   Set the watchdog timeout(s), which is a hexadecimal\n" 
			"                   integer (i.e. 0x10).\n");
}

int main(int argc, char** argv) 
{
	unsigned char time = 0;
	int opt;
	int ret = 0;
	if(argc < 2 || strcmp(argv[1], "--help") == 0){
		printUsage(argv[0]);
		exit(0);
	}

/* Get program options */
	while((opt = getopt(argc, argv, "p::s::f:")) != -1) {
		switch (opt) {
			case 'p':
				clsoe_watchdog();
				args_correctly = 1;
				break;
			case 's': 
				open_watchdog(); 
				args_correctly = 1;
				break;
			case 'f': 
				time = strtol(optarg, NULL, 0);
				feed_watchdog(time); 
				args_correctly = 1;
				break;
			default:
				args_correctly = 0;
	
		}
	}

	if(!args_correctly)
	{
		printUsage(argv[0]);
	}

	exit(0);
}
