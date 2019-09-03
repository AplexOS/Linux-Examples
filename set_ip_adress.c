#include "cmi_at155_application.h"


int set_ipadress(void)
{
	int fd = 0 ;
	int ret = 0 ;
	char machine[2] = "00" ;
	char ipadress_set[27] = "ifconfig eth0 192.168.2.xx" ;


	fd = open("machine.txt", O_RDWR) ;
	if(fd < 0)
	{
		printf("---fail set ip---\n") ; 
		return 0 ;
	}

    lseek(fd, 0, SEEK_SET) ;
    ret = read(fd, machine, 2) ;

	ipadress_set[24] = machine[0] ;
	ipadress_set[25] = machine[1] ;

	system(ipadress_set) ;

	printf("set ipadress finish!\n") ;
	close(fd) ;

	return 1 ;

}
