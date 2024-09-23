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
header('Content-Type: text/xml');

echo "<" . '?xml version="1.0" encoding="utf-8" ?' . '>';
echo "\n<snippets>\n";

$snippets = array();

foreach (glob("./snippets/*/*.js") as $filename) {
    if (is_file($filename)) {
        $snippets[] = array(
            'type' => basename(dirname($filename)),
            'name' => basename($filename, '.js'),
            'contents' => file_get_contents($filename),
        );
    }
}

foreach ($snippets as $snippet) {
    echo '<snippet type="' . htmlspecialchars($snippet['type'])
               . '" name="' . htmlspecialchars($snippet['name']) . '">'
               . htmlspecialchars($snippet['contents'])
               . "</snippet>\n";

}
echo "</snippets>";
?>