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
parser.add_argument("-n", "--number", action='store_true', default=False, help="Extract number words from the right hand side")
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()
 
two_word=[  ['United', 'States'],
            ['Czech', 'Republic'],
            ['United', 'Kingdom'],
            ['South', 'Africa'],
            ['Russian', 'Federation'],
            ['South', 'Korea'],
            ['New', 'Zealand'],
        ]

one_word=[  ['France'],
            ['Japan'],
            ['Germany'],
            ['Italy'],
            ['Sweden'],
            ['Brazil'],
            ['Spain'],
            ['Romania'],
            ['Austria'],
            ['Ecuador'],
            ['China'],
            ['Switzerland'],
            ['Australia'],
            ['Canada'],
            ['India'],
            ['Portugal'],
            ['Romania'],
            ['Netherlands'],
            ['Argentina'],
            ['Belgium'],
            ['Turkey'],
            ['Thailand'],
            ['Poland'],
            ['Denmark'],
            ['Iran'],
            ['Morocco'],
            ['Mexico'],
            ['Monaco'],
            ['Greece'],
            ['Ireland'],
            ['Malaysia'],
            ['Norway'],
            ['Indonesia'],
            ['Nigeria'],
            ['Emirates'],
            ['Finland'],
            ['Yugoslavia'],
            ['Ukraine'],
            ['Ethiopia'],
        ]

data = []
not_found = []
if args.file:
    with open(args.file,'r') as f:
        for line in f:
            found = False            
            la = line.split()
            #try to match one word
            for w in one_word:
                if la[len(la)-1] == w[0]:
                    make = {}
                    make["country"] = la.pop()
                    make["name"] = " ".join(la)
                    data.append(make)
                    found = True 
            if not found:
                #try to match two words
                for w in two_word:
                    #print "%s = %s"%(la[len(la)-1], w[1])
                    if la[len(la)-1] == w[1] and la[len(la)-2] == w[0]:
                        make = {}
                        t = la.pop()
                        make["country"] = la.pop() + " " + t
                        make["name"] = " ".join(la)
                        data.append(make)
                        #print w[0],w[1]
                        found = True 
            if not found:
                not_found.append(la)

(fp,ext)=os.path.splitext(args.file)
mf = open(fp+"_multi"+ext,'w')
sf = open(fp+"_single"+ext,'w')

      
by_country = {}
for d in data:
    if d["country"] in by_country:
        by_country[d["country"]].append(d["name"])
    else:
        by_country[d["country"]] = [d["name"]]


by_make = {}
for d in data:
    if d["name"] in by_make:
        if d["country"] not in by_make[d["name"]]:
            by_make[d["name"]].append(d["country"])
    else:
        by_make[d["name"]] = [d["country"]]


for make,countries in by_make.iteritems():
    if len(countries)>1:
        cl = '"%s"'%countries.pop()
        for country in countries:
            cl = cl+','+'"%s"'%country
        s = '"%s",%s'%(make,cl)
        mf.write(s)
    else:
        s = '"%s","%s"'%(make,countries[0])
        sf.write(s)



exit(0)
print by_country

if not_found:
    for i in not_found:
        print "['%s']"%i[-1]
else:
    for i in data:
        print i["name"]," - ",i["country"]

#print data

 #print  la[len(la)-1]
                #print w[0]
      