#!/usr/bin/env php
<?php
/*
 gets the list of most popular US extensions in chrome web store in json format
 usage: php scrap.php > addons.json

@author Krzysztof Kotowicz kkotowicz<at>gmail<dot>com
@see http://blog.kotowicz.net

*/
$url = 'https://chrome.google.com/webstore/ajax/item?hl=en&gl=US&pv={{GEN}}&count=200&token={{OFFSET}}%2C138379e14e8&marquee=false&category=popular&sortBy=0&rt=j';

$how_many = 10000;
$per_page = 200;
$ext = array();

// get webstore generation
$new_url = 'https://chrome.google.com/webstore/';
$ch = curl_init($new_url);
 
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
$response = curl_exec($ch);
curl_close($ch);

$matches = array();
if (!preg_match('#/static/(\d+)#', $response, $matches)) {
    fwrite(STDERR, "Error: couldn't find gen");
    exit(1);
}

$url = str_replace("{{GEN}}", $matches[1], $url);

for ($i = 0; $i < $how_many; $i += $per_page) {
    $new_url = str_replace('{{OFFSET}}', $i, $url);
    $ch = curl_init($new_url);
     
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS, '');
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
     
    $response = curl_exec($ch);
    curl_close($ch);
    
    process($response, $ext);
    fwrite(STDERR,'.');
}

function process($xt, &$ext) {
$matches = array();
preg_match_all('#"([a-z]{32})","(.*?)"#', $xt, $matches, PREG_SET_ORDER);

foreach ($matches as $match) {
    $ext[$match[1]] = $match[2];
}
}

echo json_encode($ext);