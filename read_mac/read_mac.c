#include <stdio.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <net/if.h>
#include <string.h>
#include <unistd.h>

static int aplex_num(const char *eth, char *number)
{
    struct ifreq ifreq;
    int sock;

    if ((sock=socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        perror("socket");
        return 2;
    }

    strcpy(ifreq.ifr_name, eth);
    if (ioctl(sock, SIOCGIFHWADDR, &ifreq) < 0)
    {
        perror("ioctl");
        return 3;
    }

    sprintf(number, "%02x%02x%02x%02x%02x%02x",
            (unsigned char)ifreq.ifr_hwaddr.sa_data[0],
            (unsigned char)ifreq.ifr_hwaddr.sa_data[1],
            (unsigned char)ifreq.ifr_hwaddr.sa_data[2],
            (unsigned char)ifreq.ifr_hwaddr.sa_data[3],
            (unsigned char)ifreq.ifr_hwaddr.sa_data[4],
            (unsigned char)ifreq.ifr_hwaddr.sa_data[5]);
    close(sock);
    return 0;
}

int main(void)
{
    char eth0_mac[20], eth1_mac[20];
    char eth2_mac[20], eth3_mac[20];
    aplex_num("eth0", eth0_mac);
    aplex_num("eth1", eth1_mac);

    printf("eth0 mac :       %s    \n", eth0_mac);
    printf("eth1 mac :       %s    \n", eth1_mac);
    return 0;
}

