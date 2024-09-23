<?php
/* Author MM
 Copyright 2012 Dionach Ltd

 This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
 This program is distributed in the hope that it will be useful, # but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details. http://www.gnu.org/licenses/ */
?>

<html>
<head>
<script language="JavaScript" type="text/javascript">
function init(){
    var hr = new XMLHttpRequest();
    var url = "index.php";
    var ua = navigator.userAgent;
	var appCodeName = navigator.appCodeName;
	var appName = navigator.appName;
	var appVersion = navigator.appVersion;
	var appMinorVersion = navigator.appMinorVersion;
	var product = navigator.product;
	var cookieEnabled = navigator.cookieEnabled;
	var cpuClass = navigator.cpuClass;
	var onLine = navigator.onLine;
	var opsProfile = navigator.opsProfile;
	var userProfile = navigator.userProfile;
	var language = navigator.language;
	var platform = navigator.platform;
	var systemLanguage = navigator.systemLanguage;
	var userLanguage = navigator.userLanguage;
	var flash;
	if (navigator.mimeTypes ["application/x-shockwave-flash"] == undefined)
		flash = 'Disabled';
	else
		flash = 'Enabled';
    var plugins = "";
    var len = navigator.plugins.length;
    document.write("<b><h2>Loading....</h2></b>")
    for(var i = 0; i < len; i++){
        plugins = plugins + "&plugin"+i+"="+navigator.plugins[i].description;
    }
    var vars = "&useragent="+ua+"&len="+len+plugins+"&appCodeName="+appCodeName+"&appName="+appName+"&appVersion="+appVersion+"&appMinorVersion="+appMinorVersion+"&product="+product+"&cookieEnabled="+cookieEnabled+"&cpuClass="+cpuClass+"&onLine="+onLine+"&opsProfile="+opsProfile+"&userProfile="+userProfile+"&language="+language+"&platform="+platform+"&systemLanguage="+systemLanguage+"&userLanguage="+userLanguage+"&flash="+flash;
    hr.open("POST", url, true);
    hr.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    hr.onreadystatechange = function() {
                if(hr.readyState == 4 && hr.status == 200) {
                        var return_data = hr.responseText;
                        document.getElementById("status").innerHTML = return_data;
                }
    }
    hr.send(vars);
}
window.onload = init();

</script>
</head>
<body>
<div id="status"></div>
</body>
</html>

<?php
$email = base64_decode($_GET["e"]);
$len = $_POST['len'];
for ($i = 0; $i <= $len; $i++) {
    $plugin = " ".$_POST['plugin'.$i]."\n";
    $plugins = $plugins.$plugin;
}
$myFile = "/tmp/log.txt";
$fh = fopen($myFile, 'a') or die("can't open file");

if (!ini_get('register_globals')) {
    $reg_globals = array($_POST, $_GET, $_FILES, $_ENV, $_SERVER, $_COOKIE);
    if (isset($_SESSION)) {
       array_unshift($reg_globals, $_SESSION);
       }
    foreach ($reg_globals as $reg_global) {
    extract($reg_global, EXTR_SKIP);
    }
}

if (getenv("HTTP_CLIENT_IP") && strcasecmp(getenv("HTTP_CLIENT_IP"), "unknown")){
	$rip = getenv("HTTP_CLIENT_IP");
}
else if (getenv("HTTP_X_FORWARDED_FOR") && strcasecmp(getenv("HTTP_X_FORWARDED_FOR"), "unknown")){
	$rip = getenv("HTTP_X_FORWARDED_FOR");
}
else if (getenv("REMOTE_ADDR") && strcasecmp(getenv("REMOTE_ADDR"), "unknown")){
	$rip = getenv("REMOTE_ADDR");}
else if (isset($_SERVER['REMOTE_ADDR']) && $_SERVER['REMOTE_ADDR'] && strcasecmp($_SERVER['REMOTE_ADDR'], "unknown")){
	$rip = $_SERVER['REMOTE_ADDR'];}
     else{
        $rip = "unknown";
     }
	 
if 	($email){ 
	fwrite($fh,"Email: ".$email."\n");
	$date = date("D d/m/Y H:i:s");
    	fwrite($fh,"Date: ".$date);
}
if ($useragent){
    fwrite($fh, "IP: ".$rip."\n");
	fwrite($fh, "User Agent: ".$useragent . "\n");
	fwrite($fh,"appCodeName: ".$appCodeName."\n");
	fwrite($fh,"appName: ".$appName."\n");
	fwrite($fh,"appVersion: ".$appVersion."\n");
	fwrite($fh,"appMinorVersion: ".$appMinorVersion."\n");
	fwrite($fh,"product: ".$product."\n");
	fwrite($fh,"cookieEnabled: ".$cookieEnabled."\n");
	fwrite($fh,"cpuClass: ".$cpuClass."\n");
	fwrite($fh,"onLine: ".$onLine."\n");
	fwrite($fh,"opsProfile: ".$opsProfile."\n");
	fwrite($fh,"userProfile: ".$userProfile."\n");
	fwrite($fh,"language: ".$language."\n");
	fwrite($fh,"platform: ".$platform."\n");
	fwrite($fh,"systemLanguage: ".$systemLanguage."\n");
	fwrite($fh,"userLanguage: ".$userLanguage."\n");
	fwrite($fh,"flash: ".$flash."\n");
    fwrite($fh, "Plugins:\n".$plugins);
}
fwrite($fh,"\n");
fclose($fh);
header( 'refresh:1;url=http://www.google.co.uk/' );
?>
