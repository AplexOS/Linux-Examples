all:
	arm-linux-gnueabihf-gcc aplex.c -L /home/ARiio_5120W/test/oceanconnect/demo/lib -lpthread -ldl -lrt -luspsdk -lssl -lcrypto -o aplex_demo
	sudo cp aplex_demo  /home/ARiio_5120W/aplex/filesystem/rootfs_release/bin/aplex_demo  -rf

clean:
	rm aplex_demo
