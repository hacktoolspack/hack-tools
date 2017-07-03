/*
 *  pcap-compatible 802.11 packet sniffer
 *
 *  Copyright (C) 2004  Christophe Devine
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 */

#include <netpacket/packet.h>
#include <sys/ioctl.h>
#include <arpa/inet.h>
#include <net/if.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>

#include "airparse.c"

#ifndef ETH_P_ALL
#define ETH_P_ALL 3
#endif

#ifndef ARPHRD_IEEE80211
#define ARPHRD_IEEE80211 801
#endif

#ifndef ARPHRD_IEEE80211_PRISM
#define ARPHRD_IEEE80211_PRISM 802
#endif

#define ARP_REQUEST_HEADER              \
    "\xAA\xAA\x03\x00\x00\x00\x08"      \
    "\x06\x00\x01\x08\x00\x06\x04"

#define REFRESH_TIMEOUT  100000

char usage[] =

"\n"
"  airodump 2.1 - (C) 2004 Christophe Devine\n"
"\n"
"  usage: airodump <wifi interface> <output filename> [mac filter]\n"
"\n";

unsigned char buffer[65536];

int do_exit = 0;

void sighandler( int signum )
{
    if( signum == SIGWINCH )
    {
        printf( "\33[2J" );
        fflush( stdout );
    }

    if( signum == SIGINT || signum == SIGTERM )
        do_exit = 1;
}

int main( int argc, char *argv[] )
{
    int i, n;
    int power;          /* strength of signal if Prism2 header  */
    int fd_raw;         /* file descriptor of the raw socket    */
    int caplen;         /* length of captured packet            */
    int arptype;        /* hardware linktype (packet header)    */
    long time_slept;    /* counter used to refresh the screen   */

    char *s;
    unsigned char *h80211;

    struct ifreq ifr;
    struct packet_mreq mr;
    struct sockaddr_ll sll;
    struct winsize ws;
    struct timeval tv;

    fd_set rfds;

    /* create the raw socket */

    if( ( fd_raw = socket( PF_PACKET, SOCK_RAW,
                             htons( ETH_P_ALL ) ) ) < 0 )
    {
        perror( "socket(PF_PACKET)" );
        return( 1 );
    }

    /* drop privileges */

    setuid( getuid() );

    /* check the arguments */

    if( argc < 3 || argc > 4 )
    {
    usage:
        printf( usage );
        return( 1 );
    }

    if( argc == 4 )
    {
        i = 0;
        s = argv[3];

        mac_filter = (unsigned char *) malloc( 6 );

        if( mac_filter == NULL )
        {
            perror( "malloc(6 bytes)\n" );
            return( 1 );
        }

        while( sscanf( s, "%x", &n ) == 1 )
        {
            if( n < 0 || n > 255 )
                goto usage;

            mac_filter[i] = n; i++;

            s = strchr( s, ':' );

            if( i == 6 || ! s ) break;

            s++;
        }

        if( i != 6 ) goto usage;
    }

    /* open or create the output files */

    if( airparse_initialize( argv[2] ) != 0 )
        return( 1 );

    /* find the interface index */

    memset( &ifr, 0, sizeof( ifr ) );
    strncpy( ifr.ifr_name, argv[optind], sizeof( ifr.ifr_name ) - 1 );

    if( ioctl( fd_raw, SIOCGIFINDEX, &ifr ) < 0 )
    {
        perror( "ioctl(SIOCGIFINDEX)" );
        return( 1 );
    }

    /* bind the raw socket to the interface */

    memset( &sll, 0, sizeof( sll ) );
    sll.sll_family   = AF_PACKET;
    sll.sll_ifindex  = ifr.ifr_ifindex;
    sll.sll_protocol = htons( ETH_P_ALL );

    if( bind( fd_raw, (struct sockaddr *) &sll,
              sizeof( sll ) ) < 0 )
    {
        perror( "bind(ETH_P_ALL)" );
        return( 1 );
    }

    /* lookup the hardware type */

    if( ioctl( fd_raw, SIOCGIFHWADDR, &ifr ) < 0 )
    {
        perror( "ioctl(SIOCGIFHWADDR)" );
        return( 1 );
    }

    arptype = ifr.ifr_hwaddr.sa_family;

    if( arptype != ARPHRD_IEEE80211 &&
        arptype != ARPHRD_IEEE80211_PRISM )
    {
        fprintf( stderr, "unsupported hardware link type %d\n",
                 ifr.ifr_hwaddr.sa_family );
        fprintf( stderr, "expected ARPHRD_IEEE80211 or "
                 "ARPHRD_IEEE80211_PRISM\n" );
        fprintf( stderr, "did you put your card in monitor mode ?\n" );
        return( 1 );
    }

    /* enable promiscuous mode */

    memset( &mr, 0, sizeof( mr ) );
    mr.mr_ifindex = sll.sll_ifindex;
    mr.mr_type    = PACKET_MR_PROMISC;

    if( setsockopt( fd_raw, SOL_PACKET, PACKET_ADD_MEMBERSHIP,
                    &mr, sizeof( mr ) ) < 0 )
    {
        perror( "setsockopt(PACKET_MR_PROMISC)" );
        return( 1 );
    }

    signal( SIGINT,   sighandler );
    signal( SIGWINCH, sighandler );

    power = -1;

    time_slept = 0;

    printf( "\33[2J" );
    fflush( stdout );

    while( 1 )
    {
        if( do_exit ) break;

        /* wait for incoming packets */

        FD_ZERO( &rfds );
        FD_SET( fd_raw, &rfds );

        tv.tv_sec  = 0;
        tv.tv_usec = REFRESH_TIMEOUT;

        if( select( fd_raw + 1, &rfds, NULL, NULL, &tv ) < 0 )
        {
            if( errno == EINTR ) continue;
            perror( "select" );
            return( 1 );
        }

        time_slept += REFRESH_TIMEOUT - tv.tv_usec;

        if( time_slept > REFRESH_TIMEOUT )
        {
            time_slept = 0;

            /* display the list of access points we have */

            if( ioctl( 0, TIOCGWINSZ, &ws ) < 0 )
            {
                ws.ws_row = 25;
                ws.ws_col = 80;
            }

            printf( "\33[1;1H" );

            airparse_aprint( ws.ws_row, ws.ws_col );

            printf( "\33[J" );
            fflush( stdout );
            continue;
        }

        if( ! FD_ISSET( fd_raw, &rfds ) )
            continue;

        /* one packet available for reading */

        memset( buffer, 0, 128 );

        if( ( caplen = read( fd_raw, buffer, sizeof( buffer ) ) ) < 0 )
        {
            perror( "read" );
            return( 1 );
        }

        /* skip the prism header if present */

        h80211 = buffer;

        if( arptype == ARPHRD_IEEE80211_PRISM )
        {
            power = *(int *)( buffer + 0x5C );

            n = *(int *)( buffer + 4 );

            if( n < 8 || n >= (int) caplen )
                continue;

            h80211 += n;
            caplen -= n;
        }

        airparse_add_packet( h80211, caplen, power );
    }

    airparse_finish();

    return( 0 );
}
