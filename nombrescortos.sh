#!/bin/bash
largo=$1

sudo cat /etc/passwd | cut -d':' -f1,3 | tr ':' ' ' > fileA

#nombre demasiado corto
while IFS= read -r line
do
	string=($line)
	#echo "Nombre: ${string[0]} passwd: ${string[1]}"
	if  ((${string[1]} >= 1000 ));then
		if ((${#string[0]} < largo));then
			echo "${string[0]}"
		fi
	fi
done < fileA

rm fileA
