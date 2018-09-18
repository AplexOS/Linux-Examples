all:
	arm-linux-gnueabihf-gcc gpio.c  -o gpio
	sudo cp gpio /home/cmi_at151/aplex/filesystem/rootfs_release/bin/ -rf
	sync
clean:
	rm gpio -rf

