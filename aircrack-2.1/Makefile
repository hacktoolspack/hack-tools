CFLAGS          = -s -W -Wall -O2
OPTFLAGS        = -D_FILE_OFFSET_BITS=64

prefix          = /usr/local
bindir          = $(prefix)/bin
datadir         = $(prefix)/share
docdir          = $(datadir)/aircrack

DESTDIR         = 
BINFILES        = 802ether aircrack aireplay airodump hopper.sh
DOCFILES        = ChangeLog rawsend.patch docs/aircrack.html

all:
	$(CC) $(CFLAGS) $(OPTFLAGS) 802ether.c -o 802ether
	$(CC) $(CFLAGS) $(OPTFLAGS) aircrack.c -o aircrack
	$(CC) $(CFLAGS) $(OPTFLAGS) aireplay.c -o aireplay
	$(CC) $(CFLAGS) $(OPTFLAGS) airodump.c -o airodump

install:
	install -d $(DESTDIR)$(bindir)
	install -m 755 $(BINFILES) $(DESTDIR)$(bindir)

doc:
	install -d $(DESTDIR)$(docdir)
	install -m 644 $(DOCFILES) $(DESTDIR)$(docdir)

clean:
	rm -f *.o 802ether aircrack aireplay airodump
