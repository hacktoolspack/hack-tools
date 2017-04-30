#!/bin/bash

version=`cat bot.py | head -3 | tail -1| awk '{print $3}' | sed "s/^\([\"']\)\(.*\)\1\$/\2/g"`

echo "[+] Deploying bot v$version"

cp -f ./bot.py ./Droplet.app/Contents/Resources/bot.py
cp -Rf ./install.sh ./Droplet.app/Contents/Resources/install.sh
cp -Rf ./modules ./Droplet.app/Contents/Resources/
cp -f ./sys.daemon.connectd.plist ./Droplet.app/Contents/Resources/sys.daemon.connectd.plist

rm -f ./Droplet.app.zip

zip -q -r Droplet.app.zip Droplet.app

echo "[>] Committing changes..."
git commit -a -m "deploy of bot v$version"
echo "[>] Pushing Changes..."
git push origin master
echo "[√] Done v$version deploy." &
say Finished version $version deployment. &
exit 0
