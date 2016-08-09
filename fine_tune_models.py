#!/usr/bin/env python 
# -*- coding: utf-8 -*-

'''###################################################################################
                       Fine Tune Model Names

        Takes a file that has been parsed by all_make_parser.py of the format:
            year    make      model  body_type/style
            "1924","Durant","A-22","Coupe"
            "1924","Durant","A-22","Business Coupe"

        and tries to adjust the model names for maximum alignment 

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
parser.add_argument("-f", "--file", default=False, help="Read from this file.")

def is_alpha(s):
    return all(char.isalpha() for char in s)

class makeTree(object):
    #head = {}
    def __init__(self):
        self.tree = {}
        self.count = 0
        self.name = ""
        
    def __repr__(self):
        l = ""
        for k,v in self.tree.iteritems():
            l = l  + k +  ":" +str(v.tree.keys()) + "\n"
        return l

    def __str__(self):
        return "tree: %s"%self.name

    def add(self,sentence):
        words = sentence.split()
        print words
        if words:
            self.count += 1
            #print "incrementing %s"%
            if words[0] not in self.tree:
                #print "adding %s"%words[0],
                self.tree[words[0]] = self.__class__() 
                self.tree[words[0]].name = words[0]
            if len(words) >1:
                print "sending %s to summer camp"%words[1:]
                self.tree[words[0]].add(" ".join(words[1:]))
    
    def add_make_model(self,make,model):
        if make:
            s = "'%s' %s"%(make,model)
            self.add(s)
            return True 
        return False

    def make_count(self,make):
        pass

    def count_all(self,make,model):
        pass

    def get_keys(self):
        allkeys = []
        if self.tree:
            for k in self.tree.keys():
                allkeys.append(k)
                if self.tree[k]:
                    subkeys = self.tree[k].get_keys()
                    if subkeys:
                        allkeys.append(subkeys)
            return allkeys
        else:
            return None

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()


make_struct = {}
if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            body_type = row[3]
            try:
                make_struct[make].add(model)
            except:
                make_struct[make] = makeTree()
                make_struct[make].add(model)

    #print head.get_makes()
    print "==============================="
    # print head.tree.keys()
    for k in make_struct.keys():
        print "%s: "%k,
        print make_struct[k].get_keys()


          
