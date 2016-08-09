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
import re


    
parser = argparse.ArgumentParser(description="Read a file parse common endings")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

#Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

doubles = [
            ["Coupe","Cabriolet"],
            ["Roadster","Runabout"],
            ["Brougham","Town Car"],
            ["Coupe","Couplet"],
          ]

 
(fp,ext)=os.path.splitext(args.file)
fo = open(fp+"_edited"+ext,'w')

if args.file:
    with open(args.file,'r') as f:
        for line in f:
            found = False
            line = line[:-1]
            #Coupe or Cabriolet
            matchObj = re.match( r'^(\'\S+\'\,\'.*?\s+)(\w+)\s+or\s+(\w+)\'$',line, re.I)
            if matchObj:
                fo.write(matchObj.group(1)+ matchObj.group(2)+"\n")
                fo.write(matchObj.group(1)+ matchObj.group(3)+"\n")
                found = True
            else:
                matchObj = re.match( r'^(\'\S+\'\,\'.*?\s+)(\w+)\s+or\s+(\w+\s+\w+)\'$',line, re.I)
                if matchObj:
                    fo.write(matchObj.group(1)+ matchObj.group(2)+"\n")
                    fo.write(matchObj.group(1)+ matchObj.group(3)+"\n")
                    found = True
            #X (or V)
            matchObj = re.match( r'^(\'\S+\'\,\'.*?\s+)(\S+)\s+\(or\s+(\S+)\)(.*)\'$',line, re.I)
            if matchObj:
                fo.write(matchObj.group(1)+ matchObj.group(2)+matchObj.group(4)+"\n")
                fo.write(matchObj.group(1)+ matchObj.group(3)+matchObj.group(4)+"\n")
                found = True
                
            if not found:
                fo.write(line+"\n")
                
           