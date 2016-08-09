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

    
parser = argparse.ArgumentParser(description="Read a file parse common endings")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

#Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

 
(fp,ext)=os.path.splitext(args.file)
fo = open(fp+"_singlewords"+ext,'w')

if args.file:
    with open(args.file,'r') as f:
        for line in f:
            line = line.replace('"','')
            line = line[:-1]
            for word in line.split():
                fo.write(word+"\n")
fo.close()