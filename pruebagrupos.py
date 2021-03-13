#!/usr/bin/env python3.9

import os

user = "pepe"
gid = 1003

grouplist = os.getgrouplist(user,gid)
print("Usuario {} esta asociado a los siguientes grupos:".format(user))
print(grouplist)

user = "paco"
gid = 1002

grouplist = os.getgrouplist(user,gid)
print("Usuario {} esta asociado a los siguientes grupos:".format(user))
print(grouplist)

user = "lola"
gid = 1004

grouplist = os.getgrouplist(user,gid)
print("Usuario {} esta asociado a los siguientes grupos:".format(user))
print(grouplist)

user = "dickinsonbp"
gid = 1000

grouplist = os.getgrouplist(user,gid)
print("Usuario {} esta asociado a los siguientes grupos:".format(user))
print(grouplist)

user = "root"
gid = 0

grouplist = os.getgrouplist(user,gid)
print("Usuario {} esta asociado a los siguientes grupos:".format(user))
print(grouplist)