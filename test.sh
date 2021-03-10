#!/bin/bash

echo "Generando carpeta test"

mkdir test
cd test
echo "hola" > hola1
echo "hola" > hola2
echo "hola" > hola3

chmod o+x hola1 hola2 hola3

tar cvf hola.tar hola1 hola2 hola3
rm hola1 hola2 hola3

echo "adios" > adios1
echo "adios" > adios2
echo "adios" > adios3

chmod o+x adios1 adios2 adios3

tar cvzf adios.tgz adios1 adios2 adios3
rm adios1 adios2 adios3

echo "tengo permiso setuid" > permisoSetuid
chmod u+s permisoSetuid

echo "tengo permiso de others" > permisoOthers
chmod o+x permisoOthers
cd ..
