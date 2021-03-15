#!/bin/bash
cat /etc/passwd | cut -d':' -f1 > fileAb
while IFS= read -r line
do

	groups $line >> grupos

done < fileAb

cat grupos | cut -d':' -f1,2 | tr ':' ' '> fileB

cont=0
while IFS= read -r line
do
	string=($line)
	if [[ "${string[*]}" == *"sudo"* ]];then
		echo "${string[0]}"

	fi
done < fileB

rm fileAb fileB grupos
