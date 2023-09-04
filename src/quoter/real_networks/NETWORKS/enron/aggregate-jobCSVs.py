#!/usr/bin/env python
# -*- coding: utf-8 -*-

# aggregate-jobCSVs.py
# Tyson Pond
# Last Modified: 2019-10-21

NUMJOBS = 100

fout=open("emails__from_to_mid.csv","w")
for JOBNUM in range(NUMJOBS):
    for line in open('jobCSVs/emails__from_to_mid%i.csv' % JOBNUM, "r"):
         fout.write(line)
fout.close()
