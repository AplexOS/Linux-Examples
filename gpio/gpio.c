#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <strings.h>
#include <unistd.h>

int main(int argc, char **argv)
{
    char *argv12[7][2] = {  "gpio8", "/dev/GPIO8",
                            "gpio9", "/dev/GPIO9",
                        };
    int i, for_num = 2;
    char shell_str[128];

    if(argc < 2 || (!strcmp(argv[1], "help")))
    {
        goto HELP_FLAG;
    }

    for(i = 0; i < for_num; i++)
    {
        if(!strcasecmp(argv[1], argv12[i][0]))
        {
            if (!strcasecmp(argv[2], "on"))
            {
                sprintf(shell_str, "echo %d > %s", 1, argv12[i][1]);
                system(shell_str);
            }
            else if (!strcasecmp(argv[2], "off"))
            {
                sprintf(shell_str, "echo %d > %s", 0, argv12[i][1]);
                system(shell_str);
            }
            else
            {
                if (i == for_num)
                    goto HELP_FLAG;
            }
        }
        else
        {
            if (i == for_num)
                goto HELP_FLAG;
        }
    }

    return 0;

HELP_FLAG:
    printf("\n");
    printf("gpio gpio8/gpio9    on/off\n");
    return 0;
}

