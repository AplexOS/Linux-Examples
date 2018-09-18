
all:
	arm-linux-gnueabihf-gcc read_mac.c  -o read_mac
	sudo cp read_mac /home/cmi_at151/aplex/filesystem/rootfs_release/bin/ -rf
	sync
clean:
	rm -rf read_mac
	sync
