#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <errno.h>

int main(void)
{

    int on_off_fd, count = 0, retval;

    on_off_fd = open("/on-off.file", O_RDWR );

    if (on_off_fd < 0)
    {
        perror("on-off.file");
        return 0;
    }

    retval = read(on_off_fd, &count, 4);
    count++;

    lseek(on_off_fd, SEEK_SET, 0);
    retval = write(on_off_fd, &count, 4);
    if (retval < 0)
    {
        perror("write of-off count error");
    }

    lseek(on_off_fd, SEEK_SET, 0);
    retval = read(on_off_fd, &count, 4);
    if(retval > 0)
    {
        printf(" on-off count : %d \n", count);
    }

    close(on_off_fd);
    system("sync");
    return 0;
}
