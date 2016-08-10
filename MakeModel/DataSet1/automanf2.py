#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
###################################################################################
#                                   
#                                
# Author: David S. Brown
# v1.0  dsb      16 Jun 2016    Original
####################################################################################
# This builds the make/model/year json tables from the enclosed .dat file its kind of 
# throwaway but I am sure it will need to be adapted to other data, so here it sits for
# future use

import json
import argparse
import os
from nested_dict import nested_dict

#import re

parser = argparse.ArgumentParser(description="Output Your Qualtrics result")
parser.add_argument("-i", "--infile",  nargs="?", dest="infile", default="vehicle_years.json", help="Path to the main input file")
parser.add_argument("-c", "--checkfile", nargs="?", dest="checkfile", default="all_known_makes.dat", help="Path to the list of manufacturers input file")
parser.add_argument("-o", "--outfile", nargs="?", dest="outfile", default="more_all_known_makes.json", help="Path to the list of manufacturers input file")
parser.add_argument("-W", "--overwrite", action='store_true', default=False, dest="overwrite", help="Is it OK to replace an existing file?")
parser.add_argument("-d", "--debug",     action='store_true', default=False,    help="Set debug on")
args = parser.parse_args()

if os.path.isfile(args.infile) and not args.infile.startswith('~'):
    with open(args.infile,'r') as f:
        vehicle_years = json.load(f)
        f.close()
else:
    print "Can't open %s"%args.infile
    exit(1)

# print vehicle_years.keys()
# print len(vehicle_years.keys())

make_list = []
if os.path.isfile(args.checkfile) and not args.infile.startswith('~'):
    with open(args.checkfile,'r') as f:
        for raw in f.readlines():
            make = raw[:-1].strip()
            if len(make)==0:
                continue
            #print "[%s]"%make,
            make = make.lower()
            if make not in vehicle_years.keys():
                print "%s not in database"%make
                vehicle_years[make]={}
            make_list.append(make)
        for key in vehicle_years.keys():
            if key not in make_list:
                print "%s not in list"%key
    f.close()
else:
    print "Can't open %s"%args.infile

if not os.path.isfile(args.outfile) or args.overwrite:
    with open(args.outfile,'w') as e:
        json.dump(vehicle_years,e)
        e.close()
else:
    print "%s already exists use --overwrite to replace"%args.outfile
    exit(2)


