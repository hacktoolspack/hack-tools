#!/bin/bash
for (( c=1; c<=9; c++ ))
{
	portnum=9050
for (( x=1; x<=$c; x++ ))
{
        (( portnum++ ))
}
	mkdir ~/tor/data${c}
	datadir="data${c}"
	./tor SocksPort ${portnum} DataDirectory ${datadir} &
}
