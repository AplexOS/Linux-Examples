export CC                  = gcc
export ROOT               := $(shell pwd)
export INCLUDE            := $(ROOT)/include
export SRC                := $(ROOT)/src
export WatchDogTest_DIR   := $(ROOT)/WatchDogExample
OBJS_DIR           := $(SRC) $(WatchDogTest_DIR)


all:libs
	make -C $(WatchDogTest_DIR) 
libs:
	make -C $(SRC)
.PHONY:clean
clean:
	-@for n in $(OBJS_DIR); do make -C $$n clean; done
	-rm lib -rf 
