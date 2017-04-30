#!/usr/bin/perl
use strict;
use Net::IP;
use IO::Socket;
use Term::ANSIColor;
use vars qw( $PROG );
( $PROG = $0 ) =~ s/^.*[\/\\]//;
#Usage
if ( @ARGV == 0 ) {
        print "Usage: ./$PROG [START-IP] [END-IP] [PORT] [THREADS] [TIMEOUT] [OUTPUT]\n";
    exit;
}
my $threads  = $ARGV[3];
my @ip_team  = ();
$|= 1;
my $ip   = new Net::IP ("$ARGV[0] - $ARGV[1]") or die "Invaild IP Range.". Net::IP::Error() ."\n";


#Start Forking :D
while ($ip) {
push @ip_team, $ip++ ->ip();
if ( $threads == @ip_team ) { Scan(@ip_team); @ip_team = () }
}
Scan(@ip_team);

#Scan
sub Scan
{
my @Pids;

        foreach my $ip (@_)
        {
        my $pid        = fork();
        die "Could not fork! $!\n" unless defined $pid;

                if  (0 == $pid)
                {
                                alarm 1;
                #Open socket, save to list, print out open ports
                my $socket = IO::Socket::INET->new(PeerAddr => $ip , PeerPort => $ARGV[2] , Proto => 'udp' , Timeout => $ARGV[4]);


                        my $payload = "\x97\x00\x00\x00\xAA\x00\x00\x00";
                        my $good = "\x97\x00\x00\x00";

                        $socket->send($payload) or die "Nothing got sent.";

                my $data;
                $socket->recv($data,4);
                my $response = substr($data,0,8);
                $response = reverse($response);
                                open (MYFILE, ">>$ARGV[5]");
                        if ($response == $good) {
                print MYFILE "$ip\n" if $socket;
                print "Found $ip\n";
                close (MYFILE);}
                exit
                }
                else
                {
                push @Pids, $pid
                }
        }

foreach my $pid (@Pids) { waitpid($pid, 0) }
}