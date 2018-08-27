
define BUILD_LIB_WatchDog
	make -C ../src
endef
	
define BUILD_APP
	$(CC) main.c  -o SuperIoWatchDog   -L  ../lib   -lWatchDog -static
endef

define CHECK_LIB_C
	@if [ ! -e /usr/lib/libc.a ];then echo "please run 'sudo yum install glibc-static' to install libc.a";fi
endef

define CHECK_LIB_WatchDog
	@if [ ! -e ../lib/libWatchDog.a ];then $(call BUILD_LIB_WatchDog);fi
endef

all:
ifeq ($(findstring Ubuntu,$(shell  lsb_release -i)), Ubuntu)
	$(call CHECK_LIB_WatchDog)
	$(call BUILD_APP)
else
	$(call CHECK_LIB_C)
	$(call CHECK_LIB_WatchDog)
	$(call BUILD_APP)
endif

.PHONY:clean
clean:
	rm SuperIoWatchDog -rf
