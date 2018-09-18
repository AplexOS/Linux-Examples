#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>

#define LED1 "/dev/LED1"
#define TRUE 1
int main(void)
{
    int fd;

    fd = open(LED1, O_RDWR);
    if (fd < 0)
    {
        perror("open error");
        return -1;
    }

    while(TRUE)
    {
        write(fd, "1", 2);
        sync();
        sleep(2);
        write(fd, "0", 2);
        sync();
        sleep(2);
    }

    close(fd);

    return 0;
}
