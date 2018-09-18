#include <unistd.h>
#include <stdio.h>
#include <fcntl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <errno.h>
#include <stdlib.h>

#define VAL_FILE  "/dev/RESET_IP"

int main(void)
{
    int val_fd, ret_val;
    char val;

    val_fd = open(VAL_FILE, O_RDONLY);
    if (val_fd < 0)
    {
        perror("open device");
        return -1;
    }

    while(1)
    {
        lseek(val_fd, SEEK_SET, 0);
        ret_val = read(val_fd, &val, 1);
        if (val == '0')
        {
            system("/etc/init.d/reset_ip.sh");
            sleep(1);
        }
        usleep(500000);
    }

    close(val_fd);
    return 0;
}
