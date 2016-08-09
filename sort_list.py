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
    
parser = argparse.ArgumentParser(description="Read a file print last words")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

makes_len = {}
if args.file:
    with open(args.file,'r') as f:
        for line in f:
            line = line.rstrip('\n').strip()
            if len(line) in makes_len:
                makes_len[len(line)].append(line)
            else:
                makes_len[len(line)]=[line]

for k in sorted(makes_len.keys(), reverse=True):
    for i in makes_len[k]:
        print i
