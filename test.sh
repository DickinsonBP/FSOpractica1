#!/bin/bash

echo "Generando carpeta test"

mkdir test
cd test
echo "hola" > hola1
echo "hola" > hola2
echo "hola" > hola3

chmod o+x hola1
chmod 750 hola2 hola3

tar cvf hola.tar hola1 hola2 hola3
rm hola1 hola2 hola3

echo "adios" > adios1
echo "adios" > adios2
echo "adios" > adios3

chmod o+x adios1 
chmod 750 adios2 adios3

tar cvzf adios.tgz adios1 adios2 adios3
rm adios1 adios2 adios3

echo "a" > a
echo "b" > b
echo "c" > c

chmod o+x a
chmod 750 b c

tar cvf abc.tar a b c
rm a b c

echo "e" > e
echo "f" > f
echo "g" > g

chmod o+x e 
chmod 750 f g

tar cvzf efg.tgz e f g
rm e f g

echo "tengo permiso setuid" > permisoSetuid
chmod u+s permisoSetuid

echo "tengo permiso de others" > permisoOthers
chmod o+x permisoOthers

echo "no tengo permisos de nada" > sinPermisos
chmod 000 sinPermisos

echo "permisos others y suid" > permisosOthersSuid
chmod u+s permisosOthersSuid
chmod o+x permisosOthersSuid

cd ..

chmod 777 test
