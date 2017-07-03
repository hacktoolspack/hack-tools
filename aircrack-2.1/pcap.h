#ifndef _COMMON_H
#define _COMMON_H

#include <sys/time.h>

#define TCPDUMP_MAGIC           0xA1B2C3D4
#define PCAP_VERSION_MAJOR      2
#define PCAP_VERSION_MINOR      4
#define LINKTYPE_ETHERNET       1
#define LINKTYPE_IEEE802_11     105
#define LINKTYPE_PRISM_HEADER   119

struct pcap_file_header
{
    unsigned int magic;
    unsigned short version_major;
    unsigned short version_minor;
    int thiszone;
    unsigned int sigfigs;
    unsigned int snaplen;
    unsigned int linktype;
};

struct pcap_pkthdr
{
    struct timeval ts;
    unsigned int caplen;
    unsigned int len;
};

#endif /* common.h */
