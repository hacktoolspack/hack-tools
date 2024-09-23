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
header('Access-Control-Allow-Origin: *');
ini_set('session.use_cookies', false);
session_id('dummy'); // use PHP sessions for persistent storage
session_start();


function nocmds($v) {
    return strpos($v, '-cmd') === false;
}
if (!empty($_GET['delete'])) { // fix memory errors
    $_SESSION = array();
    die();
}

if ($_SERVER['REQUEST_METHOD'] == 'POST' && !empty($_GET['ch'])) {
    // push to channel
    if (empty($_SESSION[$_GET['ch']])) {
        $_SESSION[$_GET['ch']] = array();
    }
    $p = file_get_contents('php://input');
    $_SESSION[$_GET['ch']][] = json_decode($p);
    
    echo json_encode(count($_SESSION[$_GET['ch']]));
} else if (!empty($_GET['ch'])) {    
    // pull from channel
    if (empty($_SESSION[$_GET['ch']])) {
        echo json_encode(array());
    } else {
        echo json_encode($_SESSION[$_GET['ch']]);
        unset($_SESSION[$_GET['ch']]);
    }
} else { // echo available not-empty channels
    $list = array();
    // get channel list
    foreach (array_filter(array_keys($_SESSION), 'nocmds') as $channel) {
        $list[] = array('ch' => $channel);
    }
    
    echo json_encode($list);
}
