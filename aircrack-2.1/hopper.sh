#!/bin/sh

NBHOPS=11
CHANNELS=1,6,11,2,7,3,8,4,9,5,10

if [ x"$1" == "x" ]
then
    echo "usage: $0 <interface>"
    exit 1
fi

INDEX=0

while true
do
    let INDEX=INDEX+1
    [ $INDEX -gt $NBHOPS ] && INDEX=1
    CURRENT=`echo $CHANNELS | cut -d ',' -f $INDEX`
    echo -n -e "\r\33[KCurrent channel: $CURRENT\r"
    iwconfig $1 channel $CURRENT
    sleep 1
done

