/*
 *  802.11 to Ethernet pcap translator
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

#include <stdio.h>
#include <time.h>

#include "pcap.h"

#define SWAP(x,y) { unsigned char tmp = x; x = y; y = tmp; }

char usage[] =

"\n"
"  802ether 2.1 - (C) 2004 Christophe Devine\n"
"\n"
"    usage: 802ether <pcap infile> <pcap outfile> [wep key]\n"
"\n"
"  example: 802ether wlan.cap ether.cap 99BC01FA40\n"
"\n";

unsigned char buffer[65536];

int main( int argc, char *argv[] )
{
    char *s;
    unsigned char K[64];
    unsigned char S[256];
    unsigned char *h80211;
    unsigned char arphdr[12];
    unsigned char wepkey[61];

    struct pcap_file_header pfh_in;
    struct pcap_file_header pfh_out;
    struct pcap_pkthdr pkh;

    int weplen, n;
    int i, j, p1, p2, z;
    long int cnt1, cnt2;
    time_t tm_prev;

    FILE *f_in, *f_out;

    /* check the arguments */

    if( argc != 3 && argc != 4 )
    {
    usage:
        printf( usage );
        return( 1 );
    }

    weplen = 0;

    if( argc == 4 )
    {
        s = argv[3];

        buffer[0] = s[0];
        buffer[1] = s[1];
        buffer[2] = '\0';

        while( sscanf( buffer, "%x", &n ) == 1 )
        {
            if( n < 0 || n > 255 )
                goto usage;

            wepkey[weplen++] = n;

            if( weplen >= 61 )
                break;

            s += 2;

            if( s[0] == '\0' || s[1] == '\0' ) break;

            buffer[0] = s[0];
            buffer[1] = s[1];
        }

        if( weplen !=  5 && weplen != 13 &&
            weplen != 29 && weplen != 61 )
            goto usage;
    }

    /* open the input file and check the pcap header */

    if( ( f_in = fopen( argv[1], "rb" ) ) == NULL )
    {
        fprintf( stderr, "fopen(%s,rb) failed\n", argv[1] );
        return( 1 );
    }

    n = sizeof( struct pcap_file_header );

    if( fread( &pfh_in, 1, n, f_in ) != (size_t) n )
    {
        fprintf( stderr, "fread(pcap header) failed\n" );
        return( 1 );
    }

    if( pfh_in.magic != TCPDUMP_MAGIC )
    {
        fprintf( stderr, "wrong magic from pcap file header\n"
                         "(got 0x%08X, expected 0x%08X)\n",
                         pfh_in.magic, TCPDUMP_MAGIC );
        return( 1 );
    }

    if( pfh_in.linktype != LINKTYPE_IEEE802_11 &&
        pfh_in.linktype != LINKTYPE_PRISM_HEADER )
    {
        fprintf( stderr, "unsupported linktype %d from pcap input file\n",
                 pfh_in.linktype );
        fprintf( stderr, "are you sure this a 802.11 capture file ?\n" );
        return( 1 );
    }

    /* attempt to open or create the output file */

    n = sizeof( struct pcap_file_header );

    if( ( f_out = fopen( argv[2], "rb+" ) ) == NULL )
    {
        if( ( f_out = fopen( argv[2], "wb+" ) ) == NULL )
        {
            fprintf( stderr, "fopen(%s,wb+) failed\n", argv[2] );
            return( 1 );
        }

        /* newly created file, so append the pcap header */

        pfh_out.magic           = TCPDUMP_MAGIC;
        pfh_out.version_major   = PCAP_VERSION_MAJOR;
        pfh_out.version_minor   = PCAP_VERSION_MINOR;
        pfh_out.thiszone        = 0;
        pfh_out.sigfigs         = 0;
        pfh_out.snaplen         = 65535;
        pfh_out.linktype        = LINKTYPE_ETHERNET;

        if( fwrite( &pfh_out, 1, n, f_out ) != (size_t) n )
        {
            fprintf( stderr, "fwrite(pcap header) failed\n" );
            return( 1 );
        }
    }
    else
    {
        /* existing file, check the pcap header contents */

        if( fread( &pfh_out, 1, n, f_out ) != (size_t) n )
        {
            fprintf( stderr, "fread(pcap header) failed\n" );
            return( 1 );
        }

        if( pfh_out.magic != TCPDUMP_MAGIC )
        {
            fprintf( stderr, "wrong magic from pcap file header\n"
                             "(got 0x%08X, expected 0x%08X)\n",
                             pfh_out.magic, TCPDUMP_MAGIC );
            return( 1 );
        }

        if( pfh_out.linktype != LINKTYPE_ETHERNET )
        {
            fprintf( stderr, "wrong linktype from pcap file header\n"
                             "(got %d, expected LINKTYPE_ETHERNET)\n",
                     pfh_out.linktype );
            return( 1 );
        }

        if( fseek( f_out, 0, SEEK_END ) < 0 )
        {
            fprintf( stderr, "fseek(SEEK_END) failed\n" );
            return( 1 );
        }
    }

    memcpy( K + 3, wepkey, weplen );

    tm_prev = time( NULL );

    cnt1 = cnt2 = 0;

    while( 1 )
    {
        /* every 2s, update the display */

        if( time( NULL ) - tm_prev >= 2 )
        {
            tm_prev = time( NULL );

            printf( "\rRead %ld packets, wrote %ld packets\r",
                    cnt1, cnt2 );

            fflush( stdout );
        }

        /* read one packet */

        n = sizeof( pkh );

        if( fread( &pkh, 1, n, f_in ) != (size_t) n )
            break;

        n = pkh.caplen;

        if( fread( buffer, 1, n, f_in ) != (size_t) n )
            break;

        cnt1++;

        h80211 = buffer;

        if( pfh_in.linktype == LINKTYPE_PRISM_HEADER )
        {
            /* remove the prism header if necessary */

            n = *(int *)( h80211 + 4 );

            if( n < 8 || n >= (int) pkh.caplen )
                continue;

            h80211 += n; pkh.caplen -= n;
        }

        if( pkh.caplen < 32 ) continue;

        /* only consider data packets */

        if( ( h80211[0] & 0x0C ) != 0x08 ) continue;

        /* if the packet in encrypted, decrypt it */

        if( ( h80211[1] & 0x40 ) == 0x40 )
        {
            if( weplen == 0 ) continue;

            z = ( ( h80211[1] & 3 ) != 3 ) ? 24 : 30;

            /* skip packets with an extended IV (TKIP/CCMP) */

            if( ( h80211[z + 3] & 0x20 ) == 0x20 ) continue;

            /* setup the RC4 key schedule */

            memcpy( K, h80211 + z, 3 );

            for( i = 0; i < 256; i++ )
                S[i] = i;

            for( i = j = 0; i < 256; i++ )
            {
                j = ( j + S[i] + K[i & (2 + weplen)]) & 0xFF;
                SWAP( S[i], S[j] );
            }

            /* remove the WEP IV/KeyID + ICV and decrypt */

            pkh.len    -= 4 + 4;
            pkh.caplen -= 4 + 4;

            p1 = p2 = 0;

            for( i = 1, j = 0; i <= (int) pkh.caplen - z; i++ )
            {
                p1 = ( p1 + 1     ) & 0xFF;
                p2 = ( p2 + S[p1] ) & 0xFF;
                SWAP( S[p1], S[p2] );
                h80211[z + i - 1] = h80211[z + i + 3] ^
                                    S[(S[p1] + S[p2]) & 0xFF];
            }

            /* check if the key is correct */

            if( h80211[ z + 2 ] != 0x03 )
                continue;

            if( h80211[ z     ] != 0xAA && h80211[ z     ] != 0xE0 )
                continue;

            if( h80211[ z     ] == 0xAA && h80211[ z + 1 ] != 0xAA )
                continue;

            if( h80211[ z     ] == 0xE0 && h80211[ z + 1 ] != 0xE0 )
                continue;
        }

        /* create the Ethernet link layer (MAC dst+src) */

        switch( h80211[1] & 3 )
        {
            case  0:    /* To DS = 0, From DS = 0: DA, SA, BSSID */

                memcpy( arphdr + 0, h80211 +  4, 6 );
                memcpy( arphdr + 6, h80211 + 10, 6 );
                break;

            case  1:    /* To DS = 1, From DS = 0: BSSID, SA, DA */

                memcpy( arphdr + 0, h80211 + 16, 6 );
                memcpy( arphdr + 6, h80211 + 10, 6 );
                break;

            case  2:    /* To DS = 0, From DS = 1: DA, BSSID, SA */

                memcpy( arphdr + 0, h80211 +  4, 6 );
                memcpy( arphdr + 6, h80211 + 16, 6 );
                break;

            default:    /* To DS = 1, From DS = 1: RA, TA, DA, SA */

                memcpy( arphdr + 0, h80211 + 16, 6 );
                memcpy( arphdr + 6, h80211 + 24, 6 );
                break;
        }

        pkh.len    += 12;
        pkh.caplen += 12;

        memcpy( buffer, arphdr, 12 );

        /* remove the 802.11 + LLC header */

        if( ( h80211[1] & 3 ) != 3 )
        {
            pkh.len    -= 24 + 6;
            pkh.caplen -= 24 + 6;

            memcpy( buffer + 12, h80211 + 30, pkh.caplen - 12 );
        }
        else
        {
            pkh.len    -= 30 + 6;
            pkh.caplen -= 30 + 6;

            memcpy( buffer + 12, h80211 + 36, pkh.caplen - 12 );
        }

        /* finally write the Ethernet packet */

        n = sizeof( pkh );

        if( fwrite( &pkh, 1, n, f_out ) != (size_t) n )
        {
            fprintf( stderr, "fwrite(packet header) failed\n" );
            return( 1 );
        }

        n = pkh.caplen;

        if( fwrite( buffer, 1, n, f_out ) != (size_t) n )
        {
            fprintf( stderr, "fwrite(packet data) failed\n" );
            return( 1 );
        }

        cnt2++;
    }

    printf( "\rRead %ld packets, wrote %ld packets.\n", cnt1, cnt2 );

    return( 0 );
}
