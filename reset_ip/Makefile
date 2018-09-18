all:
	arm-linux-gnueabihf-gcc reset_ip.c  -o reset_ip
	sudo cp reset_ip /home/cmi_at151/aplex/filesystem/rootfs_release/bin/ -rf
	sudo cp reset_ip.sh  /home/cmi_at151/aplex/filesystem/rootfs_release/etc/init.d/ -rf
	sync

clean:
	rm reset_ip -rf

