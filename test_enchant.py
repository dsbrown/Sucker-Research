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
import enchant

    
parser = argparse.ArgumentParser(description="Read a file parse common endings")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

#Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

 
(fp,ext)=os.path.splitext(args.file)
#fo = open(fp+"_edit"+ext,'w')
#d = enchant.Dict("en_US")
d = enchant.DictWithPWL(None,"body_style_words.txt")

if args.file:
    with open(args.file,'r') as f:
        for line in f:
            found = False
            line = line[:-1]
            line = line.replace('"',"")
            new_line = []
            for word in line.split():
                print word,
                if d.check(word):
                    print " is OK"
                else:
                    print " is Bad"

print "check numbers"
print "50 ",
print d.check("50")