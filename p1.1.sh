#!/bin/bash
#parametros 1--> debe ser /etc/passwd o /etc/shadow (con sudo)

#comprobacion de parametros
if(($# == 2));then
	largo=$1
	dias=$2

else
	largo=5
	dias=300
fi

directorio=./test

#sudo cat /etc/passwd | cut -d':' -f1,3 | tr ':' ' ' > fileA

#nombre demasiado corto
echo '--------------------------------'
echo "1.Nombres cortos < $largo letras" 
sudo ./nombrescortos.sh $largo

#comprobar permisos de sudoers
echo '--------------------------------'
echo "2.Ususarios sudoers" 

sudo ./sudoers.sh

echo '--------------------------------'
echo '3. Usuarios que hace demasiados que no cambian la contraseña'
#sudo cat /etc/shadow | cut -d':' -f1,3 | tr ':' ' ' > fileC
echo "$dias dias"

sudo ./massatemps.sh $dias

echo '--------------------------------'
echo '4. Archivos con permisos de ejecucion others'

sudo ./execothers.sh $directorio

echo '--------------------------------'
echo '5. Archivos con permisos SUID activado'

sudo ./setuidactiu.sh $directorio

echo '--------------------------------'
echo '6. Bit X activado de archivos comprimidos'

sudo ./comprimidos.sh $directorio
