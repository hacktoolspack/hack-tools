#!/usr/bin/perl -w
#darkcgi search for cgi files version 1.0 by mywisdom
# code reorganized by gunslinger_
use IO::Socket;  
use Socket;
use Net::hostent;
use LWP::UserAgent;
use HTTP::Response;

sub halo(){
	print "* DarkCgi version 1.0 by mywisdom[at]jasakom[dot]org\n";
	print "Scanning for paths, IIS unicodes and cgi paths\n";
	print "usage:./darkcgi.pl http://targeturl\n";
}

sub caricgi(){
#processing modul untuk cari cgi
	$daftarbrutus = "cgilist";
	open("daftarbrutus") or die("Could not open admin.txt!!!");
	$alamat=$ARGV[0];
	$slas="/";
	print "\n Testing CGI path at $alamat:\n";
	print "-----------------------------------------\n";
	foreach $line (<daftarbrutus>) {
  		chomp($line);
   		$res=$alamat.$slas.$line."";
		$useragen=LWP::UserAgent->new;
		$useragen->agent("checking");
		$hasil="404";
		my $response=$useragen->get($res);
		$hasil=$response->status_line;
   		print "Testing for url:".$res." Result:".$hasil."\n";
		open (MYFILE, '>>darkjumperlog.txt');
		 if($hasil=~/404/){
  		}
  		else{	  
		print MYFILE "\ncgi scan logs:Testing for url:".$res." Result:".$hasil."\n";
  		}
	print "Testing for url:".$res." Result:".$hasil."\n";
	close (MYFILE);     
	}
print "\n-----------Done---------------\n";
exit(1)
}


if($#ARGV<0){
	halo();   
}
else{
caricgi();
}

