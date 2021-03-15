#!/bin/bash

directorio=$1

sudo find $directorio -type f -perm /4000 2>> error