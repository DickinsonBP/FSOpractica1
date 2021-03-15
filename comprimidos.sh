#!/bin/bash

directorio=$1

mkdir descomprimir 
sudo find $directorio -name "*.tgz" > archivosTgz 2>> error
sudo find $directorio -name "*.tar" >> archivosTgz 2>> error

while IFS= read -r line
do
	tar xvf $line -C ./descomprimir > salidas
	
done < archivosTgz
sudo find ./descomprimir -type f -perm /o=x > permisosComprimidos 2>> error
cat permisosComprimidos

rm salidas error permisosComprimidos archivosTgz
rm -rf descomprimir