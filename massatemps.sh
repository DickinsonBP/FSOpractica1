#!/bin/bash
let dias=$1

sudo cat /etc/shadow | cut -d':' -f1,3 | tr ':' ' ' > fileC
numDiasHastaHoy=$(($(date --utc --date "$1" +%s)/86400))
while IFS= read -r line
do
	string=($line)
	let restaDias=$numDiasHastaHoy-${string[1]} 
	if [ $restaDias -gt $dias ];then
		echo "${string[0]}"
	fi
done < fileC

rm fileC