/*
 *  Portable 802.11 packet parser
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

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <time.h>

#include "pcap.h"

#define ARP_REQUEST_HEADER              \
    "\xAA\xAA\x03\x00\x00\x00\x08"      \
    "\x06\x00\x01\x08\x00\x06\x04"

struct AP_info
{
    struct AP_info *prev;
    struct AP_info *next;

    time_t tinit, tlast;

    int power, chanl;
    int speed, crypt;

    unsigned long nb_pkt;
    unsigned long nb_ivs;

    unsigned char bssid[6];
    unsigned char essid[33];
    unsigned char lanip[4];

    char seen_ivs[64][3];

    int s_index;
};

struct AP_info *ap_1st;
struct AP_info *ap_end;

struct AP_info *ap_cur;
struct AP_info *ap_prv;

FILE *f_cap;
FILE *f_csv;

unsigned char *mac_filter = NULL;

int airparse_initialize( char *output_prefix )
{
    int n;
    char o_filename[512];
    struct pcap_file_header pfh;

    ap_1st = NULL;
    ap_end = NULL;

    /* open or create the output pcap file */

    if( strlen( output_prefix ) >= sizeof( o_filename ) - 5 )
    {
        output_prefix[sizeof( o_filename ) - 5] = '\0';
    }

    sprintf( o_filename, "%s.cap", output_prefix );

    n = sizeof( struct pcap_file_header );

    if( ( f_cap = fopen( o_filename, "rb+" ) ) == NULL )
    {
        if( ( f_cap = fopen( o_filename, "wb+" ) ) == NULL )
        {
            fprintf( stderr, "fopen(%s) in create mode failed\n",
                     o_filename );
            return( 1 );
        }

        pfh.magic           = TCPDUMP_MAGIC;
        pfh.version_major   = PCAP_VERSION_MAJOR;
        pfh.version_minor   = PCAP_VERSION_MINOR;
        pfh.thiszone        = 0;
        pfh.sigfigs         = 0;
        pfh.snaplen         = 65535;
        pfh.linktype        = LINKTYPE_IEEE802_11;

        if( fwrite( &pfh, 1, n, f_cap ) != (size_t) n )
        {
            fprintf( stderr, "fwrite(pcap file header) failed\n" );
            return( 1 );
        }
    }
    else
    {
        if( fread( &pfh, 1, n, f_cap ) != (size_t) n )
        {
            fprintf( stderr, "fread(pcap file header) failed\n" );
            return( 1 );
        }

        if( pfh.magic != TCPDUMP_MAGIC )
        {
            fprintf( stderr, "wrong magic from pcap file header\n" );
            return( 1 );
        }

        if( pfh.linktype != LINKTYPE_IEEE802_11 )
        {
            fprintf( stderr, "wrong linktype from pcap file header\n" );
            return( 1 );
        }

        if( fseek( f_cap, 0, SEEK_END ) != 0 )
        {
            fprintf( stderr, "fseek(SEEK_END) failed\n" );
            return( 1 );
        }
    }

    /* create the output csv file */

    sprintf( o_filename, "%s.csv", output_prefix );

    if( ( f_csv = fopen( o_filename, "wb+" ) ) == NULL )
    {
        fprintf( stderr, "fopen(%s) in create mode failed\n",
                 o_filename );
        return( 1 );
    }

    return( 0 );
}

int airparse_add_packet( unsigned char *h80211, int caplen, int power )
{
    int i, n;

    struct pcap_pkthdr pkh;

    unsigned char *p;
    unsigned char bssid[6];

    ap_cur = NULL;

    pkh.caplen = pkh.len = caplen;

    /* skip packets smaller than a 802.11 header */

    if( pkh.caplen < 24 )
        goto write_packet;

    /* skip (uninteresting) control frames */

    if( ( h80211[0] & 0x0C ) == 0x04 )
        goto write_packet;

    /* skip management frames without an ESSID */

    if( ( h80211[0] & 0x0C ) == 0x00 )
        if( ( h80211[0] & 0xF0 ) != 0x00 &&
            ( h80211[0] & 0xF0 ) != 0x50 &&
            ( h80211[0] & 0xF0 ) != 0x80 )
            goto write_packet;

    /* locate the BSSID (AP's MAC) in the 802.11 header */

    switch( h80211[1] & 3 )
    {
        case  0: memcpy( bssid, h80211 + 16, 6 ); break;
        case  1: memcpy( bssid, h80211 +  4, 6 ); break;
        case  2: memcpy( bssid, h80211 + 10, 6 ); break;
        default: memcpy( bssid, h80211 +  4, 6 ); break;
    }

    /* update our chained list of access points */

    ap_cur = ap_1st;
    ap_prv = NULL;

    while( ap_cur != NULL )
    {
        if( ! memcmp( ap_cur->bssid, bssid, 6 ) )
            break;

        ap_prv = ap_cur;
        ap_cur = ap_cur->next;
    }

    /* if it's a new access point, add it */

    if( ap_cur == NULL )
    {
        if( ! ( ap_cur = (struct AP_info *) malloc(
                         sizeof( struct AP_info ) ) ) )
            return( 1 );

        memset( ap_cur, 0, sizeof( struct AP_info ) );

        if( ap_1st == NULL )
            ap_1st = ap_cur;
        else
            ap_prv->next  = ap_cur;

        memcpy( ap_cur->bssid, bssid, 6 );

        ap_cur->prev = ap_prv;

        ap_cur->tinit = time( NULL );
        ap_cur->tlast = time( NULL );
        ap_cur->power = power;
        ap_cur->chanl = -1;
        ap_cur->speed = -1;
        ap_cur->crypt = -1;

        ap_end = ap_cur;
    }

    /* every 1s, update the last time seen & receive power */

    if( time( NULL ) - ap_cur->tlast >= 1 )
    {
        ap_cur->tlast = time( NULL );
        ap_cur->power = power;
    }

    ap_cur->nb_pkt++;

    /* packet parsing: Beacon or Probe Response */

    if( h80211[0] == 0x80 ||
        h80211[0] == 0x50 )
    {
        ap_cur->crypt = ( h80211[34] & 0x10 ) >> 4;

        p = h80211 + 36;

        while( p < h80211 + pkh.caplen )
        {
            if( p + 2 + p[1] > h80211 + pkh.caplen )
                break;

            if( p[0] == 0x00 && p[2] != '\0' )
            {
                /* found a non-cloaked ESSID */

                n = ( p[1] > 32 ) ? 32 : p[1];

                memset( ap_cur->essid, 0, 33 );
                memcpy( ap_cur->essid, p + 2, n );

                for( i = 0; i < n; i++ )
                    if( ap_cur->essid[i] < ' ' )
                        ap_cur->essid[i] = '.';
            }

            if( p[0] == 0x03 )
                ap_cur->chanl = p[2];

            if( p[0] == 0x01 || p[0] == 0x32 )
                ap_cur->speed = ( p[1 + p[1]] & 0x7F ) / 2;

            if( p[0] == 0xDD )
                ap_cur->crypt++;

            p += 2 + p[1];
        }
    }

    /* packet parsing: Association Request */

    if( h80211[0] == 0x00 )
    {
        p = h80211 + 28;

        while( p < h80211 + pkh.caplen )
        {
            if( p + 2 + p[1] > h80211 + pkh.caplen )
                break;

            if( p[0] == 0x00 && p[2] != '\0' )
            {
                /* found a non-cloaked ESSID */

                n = ( p[1] > 32 ) ? 32 : p[1];

                memset( ap_cur->essid, 0, 33 );
                memcpy( ap_cur->essid, p + 2, n );

                for( i = 0; i < n; i++ )
                    if( ap_cur->essid[i] < ' ' )
                        ap_cur->essid[i] = '.';
            }

            p += 2 + p[1];
        }
    }

    /* packet parsing: non-encrypted data */

    if( ( h80211[0] & 0x0C ) == 0x08 &&
        ( h80211[1] & 0x40 ) == 0x00 )
    {
        if( memcmp( h80211 + 24, ARP_REQUEST_HEADER, 14 ) == 0 )
            memcpy( ap_cur->lanip, h80211 + 46, 4 );
    }

    /* packet parsing: WEP encrypted data */

    if( ( h80211[0] & 0x0C ) == 0x08 &&
        ( h80211[1] & 0x40 ) == 0x40 )
    {
        int z = ( ( h80211[1] & 3 ) != 3 ) ? 24 : 30;

        for( i = 0; i < 64; i++ )
            if( ! memcmp( ap_cur->seen_ivs[i], h80211 + z, 3 ) )
                return( 0 );

        n = ap_cur->s_index;
        memcpy( ap_cur->seen_ivs[n++], h80211 + z, 3 );

        ap_cur->s_index = n % 64;
        ap_cur->nb_ivs++;
    }

write_packet:

    if( mac_filter != NULL )
    {
        /* reject packets that do not contain the specified MAC */

        if( ( h80211[1] & 3 ) != 3 )
        {
            if( memcmp( h80211 +  4, mac_filter, 6 ) &&
                memcmp( h80211 + 10, mac_filter, 6 ) &&
                memcmp( h80211 + 16, mac_filter, 6 ) )
                return( 0 );
        }
        else
        {
            if( memcmp( h80211 +  4, mac_filter, 6 ) &&
                memcmp( h80211 + 10, mac_filter, 6 ) &&
                memcmp( h80211 + 16, mac_filter, 6 ) &&
                memcmp( h80211 + 24, mac_filter, 6 ) )
                return( 0 );
        }
    }

    /* finally append the packet to the pcap file */

#ifndef WIN32
    gettimeofday( &pkh.ts, NULL );
#else
    pkh.tv_sec  = time( NULL );
    pkh.tv_usec = 0;
#endif

    n = sizeof( pkh );

    if( fwrite( &pkh, 1, n, f_cap ) != (size_t) n )
    {
        fprintf( stderr, "fwrite(packet header) failed\n" );
        return( 1 );
    }

    n = pkh.caplen;

    if( fwrite( h80211, 1, n, f_cap ) != (size_t) n )
    {
        fprintf( stderr, "fwrite(packet data) failed\n" );
        return( 1 );
    }

    return( 0 );
}

void airparse_aprint( int ws_row, int ws_col )
{
    int nlines;
    char strbuf[64];

    /* print some informations about each detected AP */

    printf( "\n  BSSID              CH  MB  ENC  PWR"
            "  Packets   LAN IP / # IVs   ESSID\n\n" );

    ap_cur = ap_end;

    nlines = 0;

    while( ap_cur != NULL )
    {
        if( time( NULL ) - ap_cur->tlast > 120 )
        {
            ap_cur = ap_cur->prev;
            continue;
        }

        if( nlines++ > ws_row - 5 )
            break;

        printf( "  %02X:%02X:%02X:%02X:%02X:%02X",
                ap_cur->bssid[0], ap_cur->bssid[1],
                ap_cur->bssid[2], ap_cur->bssid[3],
                ap_cur->bssid[4], ap_cur->bssid[5] );

        printf( "  %2d %3d  ", ap_cur->chanl, ap_cur->speed );

        switch( ap_cur->crypt )
        {
            case  0: printf( "OPN" ); break;
            case  1: printf( "WEP" ); break;
            case  2: printf( "WPA" ); break;
            default: printf( "   " ); break;
        }

        printf( "  %3d %8ld  ", ap_cur->power, ap_cur->nb_pkt );

        if( ap_cur->crypt > 0 )
        {
            printf( "%15ld", ap_cur->nb_ivs );
        }
        else
        {
            strbuf[0] = '\0';

            if( *(unsigned long *)( ap_cur->lanip ) )
                sprintf( strbuf, "%3d.%3d.%3d.%3d",
                         ap_cur->lanip[0], ap_cur->lanip[1],
                         ap_cur->lanip[2], ap_cur->lanip[3] );

            printf( "%15s", strbuf );
        }

        sprintf( strbuf, "%-32s", ap_cur->essid );
        strbuf[ws_col - 68] = '\0';
        printf( "   %s\n", strbuf );

        ap_cur = ap_cur->prev;
    }
}

void airparse_finish( void )
{
    struct tm *ltime;

    ap_cur = ap_1st;

    /* write some informations about each detected AP */

    fprintf( f_csv, "BSSID, First time seen, Last time seen, Channel, Speed"
                    ", Privacy, Power, # packets, # IVs, LAN IP, ESSID\r\n" );

    while( ap_cur != NULL )
    {
        fprintf( f_csv, "%02X:%02X:%02X:%02X:%02X:%02X, ",
                 ap_cur->bssid[0], ap_cur->bssid[1],
                 ap_cur->bssid[2], ap_cur->bssid[3],
                 ap_cur->bssid[4], ap_cur->bssid[5] );

        ltime = localtime( &ap_cur->tinit );

        fprintf( f_csv, "%04d-%02d-%02d %02d:%02d:%02d, ",
                 1900 + ltime->tm_year, 1 + ltime->tm_mon,
                 ltime->tm_mday, ltime->tm_hour,
                 ltime->tm_min,  ltime->tm_sec );

        ltime = localtime( &ap_cur->tlast );

        fprintf( f_csv, "%04d-%02d-%02d %02d:%02d:%02d, ",
                 1900 + ltime->tm_year, 1 + ltime->tm_mon,
                 ltime->tm_mday, ltime->tm_hour,
                 ltime->tm_min,  ltime->tm_sec );

        fprintf( f_csv, "%2d, %3d, ",
                 ap_cur->chanl,
                 ap_cur->speed );

        switch( ap_cur->crypt )
        {
            case  0: fprintf( f_csv, "OPN, " ); break;
            case  1: fprintf( f_csv, "WEP, " ); break;
            case  2: fprintf( f_csv, "WPA, " ); break;
            default: fprintf( f_csv, "   , " ); break;
        }

        fprintf( f_csv, "%3d, %8ld, %8ld, ",
                 ap_cur->power,
                 ap_cur->nb_pkt,
                 ap_cur->nb_ivs );

        fprintf( f_csv, "%3d.%3d.%3d.%3d, ",
                 ap_cur->lanip[0], ap_cur->lanip[1],
                 ap_cur->lanip[2], ap_cur->lanip[2] );

        fprintf( f_csv, "%-32s\r\n", ap_cur->essid );

        ap_cur = ap_cur->next;
    }

    fclose( f_csv );
    fclose( f_cap );
}
