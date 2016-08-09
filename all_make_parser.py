#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''###################################################################################
                Primary Parser for historical_all_car_make_model.txt

Takes a file of the format:
    '1924','Durant A-22 Series Coupe'
    '1924','Durant A-22 Series Business Coupe'

and parses it into a file of the format:
    year    make      model  body_type/style
    "1924","Durant","A-22","Coupe"
    "1924","Durant","A-22","Business Coupe"

The word Series is removed if it was on the line

The algorithm is complex ...

it uses a make file that is specially formated with the longer and more complex
brands at the top and the simple ones towards the bottom to avoid false matches

After finding the brand(make) it takes anything to the left of the word
'Series' if it exists and uses that data as the model name. It then works from
the right hand side pulling out common body type words which it gets from the
body_style_words.txt document

What is left over is added to the right hand side of model  

Author: David S. Brown
####################################################################################'''

import os
import sys
import argparse
import csv
import re
import enchant


parser = argparse.ArgumentParser(description="Read a file parses it to make model and body style")
parser.add_argument("-d", "--debug", action='store_true', default=False, help="Set debug on")
parser.add_argument("-f", "--file", default=False, required=True, help="Read from this file.")
parser.add_argument("-m", "--make_file", default=False, required=True, help="Read makes from this file.")
parser.add_argument("-b", "--body_file", default=False, required=True, help="Read makes from this file.")

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

# enchant returns true for numbers so need to short circuit that behavior
# this returns true only if all chars are alpha
def is_alpha(s):
    ACCEPTABLE = [ "2-seat", "3-seat", "4-seat"]
    if s in ACCEPTABLE:
        return True
    else:
        return all(char.isalpha() for char in s)

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

makes = get_makes(args.make_file)
 
(fp,ext)=os.path.splitext(args.file)
fo = open(fp+"_parsed"+ext,'w')
nf = open(fp+"_not_found"+ext,'w')

endings = {}
d = enchant.DictWithPWL(None,"body_style_words.txt")
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
                        #print "Make: %s"%make
                        #print "Model: %s"%model 
                        # CD DV32 Series Convertible Coupe  
                        # or:  Series CD DV32 Convertible Coupe  
                        #
                        # <<CD DV32>> Series Convertible Coupe  
                        model = ""
                        rh = None
                        if matchObj.group(2).find("Series") >= 0:  # obj.find is much faster than re so check with that first
                            matchObj2 = re.match( r'\s*?(.+?)\s+Series\s+(.*)',matchObj.group(2), re.I)
                            if matchObj2:
                                model = matchObj2.group(1)
                                rh = matchObj2.group(2)
                            else:
                                # Series <<CD>>DV32 Convertible Coupe   
                                matchObj2 = re.match( r'\s*?Series\s+(.*)\s*',matchObj.group(2), re.I)
                                if matchObj2:
                                    rh = matchObj2.group(1)
                                else:
                                    # its possible there is nothing to the right of Series
                                    matchObj2 = re.match( r'\s*?(.+?)\s+Series',matchObj.group(2), re.I)
                                    if matchObj2:
                                        model = matchObj2.group(1)
                                        body_type = ""
                                        rh = ""
                                    else:
                                        print "Failed all regex: %s - %s "%(year_str,mm_str),
                                        print matchObj.group(2)
                                        found = False
                                        break
                        else:
                            #print "No Series in line: %s - %s"%(year_str,mm_str),
                            rh = matchObj.group(2)
                            #print "Using: %s"%rh

                        '''####################################################################
                        examine each word from the right working left take maximum 4 words for 
                        body style if they are in the body style dictionary stop at the first 
                        unrecognized word.
                        so Series CD DV32 Convertible Coupe
                        Coupe, then Convertible, then DV32 is not in the dictionary so stop
                        body_type = Convertible Coupe
                        body_type = CD DV32
                        ####################################################################'''
                        if rh:
                            tokens = rh.split()
                            #print "Tokens: %s"%tokens
                            body_type_list = []
                            body_type = ""
                            # go through list right to left stop at first no dict word or after three
                            for i in range(len(tokens),0,-1):
                                if len(body_type_list)<4 and is_alpha(tokens[i-1]) and d.check(tokens[i-1]):
                                    body_type_list.append(tokens.pop(i-1))
                            # put the words in the list back together remember they are reversed
                            if len(body_type_list)>0:
                                body_type_list.reverse()
                                body_type = " ".join(body_type_list)
                            model_ext = " ".join(tokens)
                            model = model+" "+model_ext
                            model = model.strip()
                            body_type = body_type.strip()
                        
                        #print "Model: %s, Body: %s"%(model,body_type)
                        fo.write('"%s","%s","%s","%s"\n'%(year,make,model,body_type))
                        found = True

                        # wrap up some things
                        if body_type in endings:
                            endings[body_type] +=1
                        else:
                            endings[body_type] = 1
                        break

                        if not found:
                            nf.write('"%s","%s"\n'%(year,mm_str))


    write_sort_endings(endings,fp+"_endings"+ext)
