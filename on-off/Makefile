
all:
	arm-linux-gnueabihf-gcc on-off.c -o on-off
	sudo cp on-off /home/cmi_at151/aplex/filesystem/rootfs_release/bin  -rf
	sudo cp on-off.sh  /home/cmi_at151/aplex/filesystem/rootfs_release/root/  -rf
	sync

clean:
	rm on-off
