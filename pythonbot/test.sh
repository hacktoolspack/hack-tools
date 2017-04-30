#!/bin/bash

version=`cat bot.py | head -3 | tail -1| awk '{print $3}' | sed "s/^\([\"']\)\(.*\)\1\$/\2/g"`

echo "[+] Starting test of v$version"

cp -f ./bot.py /var/softupdated/bot.py && kill `ps -ax|grep bot.py|head -1|awk '{print $1}'` && echo "[#] Bot copied and reloaded."

sleep 2

logfile=`ls -t /var/softupdated | head -1`
echo "[#] Tailing Logfile... $logfile"

tail -f /var/softupdated/$logfile

echo "[√] Done v$version test. Bot still running."
exit 0
