SHELL                  :=/bin/bash
Distributor_Id         := $(shell  lsb_release -i)
Distributor_Type       := $(findstring Ubuntu,$(Distributor_Id))
Distributor_Type_Strip := $(strip $(Distributor_Type))
Libc_a                 := $(shell ls /usr/lib/libc.a)



all:install_glic
	$(CC) main.c  -o SuperIoWatchDog   -L  ../lib   -lWatchDog -static

install_glic:
	@if [ "$(Distributor_Type_Strip)x" != "Ubuntux" ];then \
		if [ "$(Libc_a)x"    != "/usr/lib/libc.ax" ];then \
			echo "please run 'sudo yum install glibc-static' to install libc.a";\
		fi \
	fi
clean:
	rm SuperIoWatchDog -rf
