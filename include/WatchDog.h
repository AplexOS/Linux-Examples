#include <sys/io.h>
#include <stdio.h>
#include <stdlib.h>

// Function code and register
#define EFER  0x2E  //Extended Function Enable Registers
#define EFDR  0x2F  //Extended Function Data Registers
#define WTMR  0x08  //Logical Device number of The Watchdog
#define WTVR  0xF1  //Set watchdog timeout value register
#define EEFM  0x87  //the value to start the Extended Function Mode
#define EFIR  0x07  //the value to enter selection mode
#define EFQR  0xAA  //the value to quit the Extended Function Mode
#define TIMEOUT 0x3c //Set the default timeout
//int args_correctly = 0;

static int init_SuperIo();

void open_watchdog();

void feed_watchdog(unsigned char time);

void clsoe_watchdog();

