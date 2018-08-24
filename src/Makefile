all:
	$(CC)  -c   WatchDog.c  -o WatchDog.o
	ar  -crs  libWatchDog.a WatchDog.o
	install -D libWatchDog.a ../lib/libWatchDog.a
	
	$(CC)  -fPIC  -c   WatchDog.c  -o WatchDog.o
	$(CC)  -shared     WatchDog.o  -o  libWatchDog.so
	install -D libWatchDog.so ../lib/libWatchDog.so

clean:
	rm libWatchDog.a WatchDog.o libWatchDog.so -rf 
