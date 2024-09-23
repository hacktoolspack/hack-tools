#!/usr/bin/perl
use IO::Socket;  
use Socket;
use Net::hostent;
use LWP::UserAgent;
use HTTP::Response;
sub main(){
#pemrosesan modul pengambilan info
	print "[+] Daemon informations from common ports: 21,22,23,25,80,110 and 3306: \n";
	#info dari port 21
	$namatarget=$ARGV[0];
	open (MYFILE, '>>darkjumper.log');

	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '21',
	  Proto => 'tcp',
	  );
	if($socket){
	$pesan="help";
	$socket->send($pesan);
	
	$socket->recv($recvpesan,800);
	print "[+] Daemon response (info) from port 21 (ftp Daemon):\n $recvpesan\n";
	print MYFILE "[+] Daemon response (info) from port 21 (ftp Daemon):\n $recvpesan\n";
	
	}     

	#info dari port 22

	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '22',
	  Proto => 'tcp',
	  );
	if($socket)
	 {
	$pesan="help";
	$socket->send($pesan);
	$socket->recv($recvpesan,800);
	
	print "[+] Daemon response (info) from port 22 (ssh Daemon):\n $recvpesan\n";
	print MYFILE "\n \n[+] Daemon response (info) from port 22 (ssh Daemon):\n $recvpesan\n";
	 
 	}

	#info dari port 23
      
	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '23',
	  Proto => 'tcp',
	  );
	if($socket)
	 {
	$pesan="help";
	$socket->send($pesan);
        $socket->recv($recvpesan,800);
        
        print "[+] Daemon response (info) from port 23 (telnet Daemon):\n $recvpesan\n";
	print MYFILE "\n \n[+] Daemon response (info) from port 23 (telnet Daemon):\n $recvpesan\n";
	
 	}

	#info dari port 25
	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '25',
	  Proto => 'tcp',
	  );
	if($socket){
	$pesan="help";
	$socket->send($pesan);
	$socket->recv($recvpesan,800);
	
	print "[+] Daemon response (info) from port 25 (smtp Daemon):\n $recvpesan\n";
	print MYFILE "\n \n[+] Daemon response (info) from port 25 (smtp Daemon):\n $recvpesan\n";
	
	} 

	#info dari port 80
	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '80',
	  Proto => 'tcp',
	  );
	if($socket){
	$pesan="put \n";
	$socket->send($pesan);
	$socket->recv($recvpesan,800);
	
	print "[+] Daemon response (info) from port 80 (httpd):\n $recvpesan\n";
	print MYFILE "\n \n[+] Daemon response (info) from port 80 (httpd):\n $recvpesan\n";
	print "Important! You can see informations such as: web server version,ssl version,php version,perl version \n";
	
	} 



	#info dari port 110
	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '110',
	  Proto => 'tcp',
	  );
	if($socket){
	$pesan="help \n";
	$socket->send($pesan);
	$socket->recv($recvpesan,800);
	
	print "[+] Daemon response (info) from port 110 (pop3 server):\n $recvpesan\n";      
	
	} 

	#info dari port 3306
	$socket = IO::Socket::INET->new
	  (
	  PeerAddr => $namatarget,
	  PeerPort => '3306',
	  Proto => 'tcp',
	  );
	if($socket){
	$pesan="help";
	$socket->send($pesan);
	$socket->recv($recvpesan,800);
	
	print "[+] Daemon response (info) from port 3306 (mysql [+] Daemon):\n $recvpesan\n";
	 
	} 
exit;
}
#jalankan program !!!
main();
exit;
# end of jalankan program !!!
