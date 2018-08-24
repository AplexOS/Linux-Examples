CC                  = gcc
ROOT               := $(shell pwd)
INCLUDE            := $(ROOT)/include
SRC                := $(ROOT)/src
WatchDogTest_DIR   := $(ROOT)/WatchDogExample
OBJS_DIR           := $(SRC) $(WatchDogTest_DIR)


all:libs
	make -C $(WatchDogTest_DIR) 
libs:
	make -C $(SRC)
clean:
	@for n in $(OBJS_DIR); do make -C $$n clean; done
	rm lib -rf 
