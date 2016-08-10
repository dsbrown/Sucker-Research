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
parser.add_argument("-i", "--infile",  nargs="?", dest="infile", required=True, help="Path to the input file")
#parser.add_argument("-o", "--outfile", nargs="?", dest="outfile",required=True, help="Path to the input file")
parser.add_argument("-W", "--overwrite", action='store_true', default=False, dest="overwrite", help="Is it OK to replace an existing file?")
parser.add_argument("-d", "--debug",     action='store_true', default=False,    help="Set debug on")
args = parser.parse_args()

vehicle_makes = {}
vehicle_years = nested_dict()

if os.path.isfile(args.infile) and not args.infile.startswith('~'):
    with open(args.infile,'r') as f:
        for l in f.readlines():
            yp = l.find(",")
            year   = l[0:yp]
            mp = l.find(",",yp+1)
            make =  l[yp+3:mp-1]
            make_l = make.lower()
            model = l[mp+3:len(l)-2]
            model_l = model.lower()

            if not vehicle_years[make_l][model_l]:
                vehicle_years[make_l][model_l] = [year]
            else:
                vehicle_years[make_l][model_l].append(year)

            if make not in vehicle_makes.keys():
                vehicle_makes[make_l]=[model_l]
            else:
                vehicle_makes[make_l].append(model_l)
    f.close()
else:
    print "Can't open %s"%args.infile
    exit(1)

vehicle_years_dict = vehicle_years.to_dict()

# for make in vehicle_years_dict.keys():
#     print "[",
#     print make, 
#     print ":",
#     for model in vehicle_years_dict[make].keys():
#         print model,
#         print ",",
#     print "]"

# for make in vehicle_makes.keys():
#     print "[",
#     print make, 
#     print ":",
#     print vehicle_makes[make],
#     print ",",
#     print "]"

fname1 = "vehicle_years.json"
fname2 = "vehicle_makes.json"
if not os.path.isfile(fname1) or args.overwrite:
    with open(fname1,'w') as e:
        json.dump(vehicle_years_dict,e)
        e.close()

if not os.path.isfile(fname2) or args.overwrite:
    with open(fname2,'w') as e:
        json.dump(vehicle_makes,e)
        e.close()
else:
    print "%s already exists use --overwrite to replace"%args.outfile
    exit(2)
