#!/bin/bash

directorio=$1

sudo find $directorio -type f -perm /o=x 2> error