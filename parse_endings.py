#!/usr/bin/env python 
# -*- coding: utf-8 -*-

###################################################################################
# Gives last one and two words in sentence
#
# Author: David S. Brown
####################################################################################

import os
import sys
import argparse
import csv
import re

parser = argparse.ArgumentParser(description="Read a file print last words")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-n", "--number", action='store_true', default=False, help="Extract number words from the right hand side")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")
parser.add_argument("-m", "--make_file", default=False, help="Read makes from this file.")

def get_makes(make_file):
    makes = []
    makes_len = {}
    if make_file:
        with open(make_file,'r') as f:
            for line in f:
                line = line.rstrip('\n').strip()
                if len(line) in makes_len:
                    makes_len[len(line)].append(line)
                else:
                    makes_len[len(line)]=[line]

    for k in sorted(makes_len.keys(), reverse=True):
        makes.extend(makes_len[k])
    return makes

def write_sort_endings(endings,filename):
    en = open(filename,'w')
    for v in sorted(endings, key=endings.get, reverse=True):
        en.write('"%s"\n'%v)
    en.close()
    return True

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

makes = get_makes(args.make_file)
 
(fp,ext)=os.path.splitext(args.file)
fo = open(fp+"_make_model"+ext,'w')
nf = open(fp+"_not_found"+ext,'w')

endings = {}
if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        for row in reader:
            found = False
            year = None
            year_str = row[0].replace("'","")
            mm_str   = row[1].replace("'","")

            # <<1934>>,Stutz CD DV32 Series Convertible Coupe
            try:
                year = int(year_str)
            except:
                year = ""
            if year:
                for make in makes:
                    # <<Stutz>> CD DV32 Series Convertible Coupe
                    matchObj = re.match( r'\s*?(%s) (.*)'%make, mm_str, re.I)
                    if matchObj and matchObj.group(1) == make:                                                
                        #match_make = " ".join(matchObj.group(1).split())
                        #model = matchObj.group(2)
                        #print "Make: %s"%match_make,
                        #print "Model: %s"%model 
                        # CD DV32 Series Convertible Coupe  
                        # or:  Series CD DV32 Convertible Coupe  
                        #
                        # <<CD DV32>> Series Convertible Coupe                                  
                        if matchObj.group(2).find("Series") >= 0:
                            matchObj2 = re.match( r'\s*?(.*?)\s+Series\s+(.*)',matchObj.group(2), re.I)
                            if matchObj2:
                                model = matchObj2.group(1)
                                model_type = matchObj2.group(2)
                                fo.write('"%s","%s","%s","%s"\n'%(year,make,model,model_type))
                                found = True
                                break
                            else:
                                # Series <<CD>>DV32 Convertible Coupe   
                                matchObj2 = re.match( r'\s*?Series\s+(\S+)\s+(.*)',matchObj.group(2), re.I)
                                if matchObj2:
                                    model = matchObj2.group(1)
                                    model_type = matchObj2.group(2)
                                    fo.write('"%s","%s","%s","%s"\n'%(year,make,model,model_type))
                                    found = True
                                    break
                                else:
                                    found = False

                # wrap up some things
                if model_type in endings:
                    endings[model_type] +=1
                else:
                    endings[model_type] = 1
                if not found:
                    nf.write('"%s","%s"\n'%(year,mm_str))

    write_sort_endings(endings,fp+"_endings"+ext)
