#!/usr/bin/env python 
# -*- coding: utf-8 -*-


import os
import sys
import argparse
import csv
import re
from operator import itemgetter

parser = argparse.ArgumentParser(description="Read a file parses it to get model names")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, required=True, help="Read from this file.")
parser.add_argument("-o", "--outfile", default=False, required=True, help="Read from this file.")

def update_struct(struct,k,v):
    if k in struct:
        print "adding %s to %s"%(v,k)
        if v not in struct[k]:
            struct[k].append(v)
    else:
        struct[k]=[v]

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

model_struct = {}
if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            body_type = row[3]
            for word in model.split():
                try:
                    model_struct[word] += 1
                except:
                    model_struct[word] = 1
            

with open(args.outfile,'w') as fo:
    for k,v in sorted(model_struct.iteritems(), key=itemgetter(1) ,reverse=True):
        fo.write("%s\n"%k)

            
