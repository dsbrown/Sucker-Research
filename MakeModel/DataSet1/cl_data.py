#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
###################################################################################
#                                   
#                                
# Author: David S. Brown
# v1.0  dsb      16 Jun 2016    Original
####################################################################################
# This reads the Craigslist json tables 

import json
import argparse
import os
from nested_dict import nested_dict


parser = argparse.ArgumentParser(description="Output Your Qualtrics result")
parser.add_argument("-i", "--infile",  nargs="?", dest="infile", required=True, help="Path to the input file")
parser.add_argument("-W", "--overwrite", action='store_true', default=False, dest="overwrite", help="Is it OK to replace an existing file?")
parser.add_argument("-d", "--debug",     action='store_true', default=False,    help="Set debug on")
args = parser.parse_args()

if os.path.isfile(args.infile) and not args.infile.startswith('~'):
    with open(args.infile,'r') as f:
        t = json.load(f)
        f.close()
else:
    print "Can't open %s"%args.infile
    exit(1)

for i in t:
    print i['title']
 

