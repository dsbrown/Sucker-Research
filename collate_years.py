#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''###################################################################################
                    Collate Years out of historical_all_car_make_model.txt

Takes a file that has been parsed by all_make_parser.py of the format:
    year    make      model  body_type/style
    "1924","Durant","A-22","Coupe"
    "1924","Durant","A-22","Business Coupe"

and tries to combine all the years for a make, model and body-type

Author: David S. Brown
####################################################################################'''

import os
import sys
import argparse
import csv
import re

parser = argparse.ArgumentParser(description="Read a file parses it to make model and body style")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

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

year_struct = {}
body_struct = {}
if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            body_type = row[3]
            make_model = make+"_"+model
            update_struct(year_struct,make_model,year)
            update_struct(body_struct,make_model,body_type)

(fp,ext)=os.path.splitext(args.file)
fo = open(fp+"_collated"+ext,'w')

all_keys  = frozenset(year_struct.keys()) | frozenset(body_struct.keys())

for k in all_keys:
    print '"%s",'%k,
    if k in year_struct:
        print year_struct[k],
    print ",",
    if k in body_struct:
        print body_struct[k]
    

            
