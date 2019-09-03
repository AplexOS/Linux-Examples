#ifndef  __POST_TO_SERVICE_H
#define  __POST_TO_SERVICE_H

void ftpget_mes_dll(void) ;
void set_machine_id(int machineid) ;
int postDatesToService(int sockfd, char* pathname, char* inputbuf, int flag, char mode) ;
int SystemPowerOn_ParemerRead() ;
int SystemPowerOff_ParemerWrite(int post_status, char* postcount) ;
int read_powerdown_paramer(void) ;
void show_log(void) ;

#endif


