
all:
	arm-linux-gnueabihf-gcc sysrunled.c  -o sysrunled
	sudo cp sysrunled /home/cmi_at151/aplex/filesystem/rootfs_release/bin/ -rf
	sync

clean:
	rm sysrunled -rf
