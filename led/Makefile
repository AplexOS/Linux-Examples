all:
	arm-linux-gnueabihf-gcc led.c  -o led
	sudo cp led /home/cmi_at151/aplex/filesystem/rootfs_release/bin/ -rf
	sync
clean:
	rm led -rf

