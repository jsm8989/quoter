#!/usr/bin/env python
# -*- coding: utf-8 -*-

# scan-maildir.py
# Jim Bagrow
# Last Modified: 2019-10-15

import sys, os
import re
import csv


if __name__ == "__main__":
    
    path = 'maildir'

    re_mid = re.compile(r"Message-ID: <(.+)>")
    re_fr  = re.compile(r"From: (.*)")
    re_to  = re.compile(r"To: (.*)") 

    try:
        JOBNUM, NUMJOBS = map(int, sys.argv[1:])
    except IndexError:
        sys.exit("Usage: %s JOBNUM NUMJOBS" % sys.argv[0] )

    ##JOBNUM = 0
    ##NUMJOBS = 1
            
    ##print("scanning files")
    fout = open('jobCSVs/emails__from_to_mid%i.csv' % JOBNUM, 'w', newline='')
    csvwriter = csv.writer(fout)
    num_bad_mid = 0
    num_bad_fr = 0
    num_bad_to = 0

    job_files = os.walk(path)
    job_files = [(r,d,f) for i,(r,d,f) in enumerate(job_files) if i % NUMJOBS == JOBNUM]

    for r, d, f in job_files:
    ##    sys.stdout.write("\r%s\r%s" % (" "*100,r)); sys.stdout.flush()
        
        for file in f:
            txt = open(os.path.join(r, file), 'r', encoding='utf-8', errors='ignore').read()
            
            try:
                mid = re_mid.search(txt)[1]
            except:
                num_bad_mid += 1
                continue
            try:
                fr = re_fr.search(txt)[1]
            except:
                num_bad_fr += 1
                continue
            try:
                to = re_to.search(txt)[1]
                tos = [t.strip() for t in to.strip().split(",") if t]
            except:
                num_bad_to += 1
                continue
            
            for t in tos:
                csvwriter.writerow([fr, t, mid])
                # ^^^ may include self-loops, non-enron addresses

    fout.close()



