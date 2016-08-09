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
    head = {}
    def __init__(self):
        self.model_tree = {}
        self.model_count = 0
        
    def __repr__(self):
        l = ""
        for k,v in makeTree.head.iteritems():
            l = l  + k +  ":" +str(v.model_tree.keys()) + "\n"
        return l

    def __str__(self):
        return "model_tree:" 

    def add(self,make,model):
        if make not in makeTree.head:
            #temp = self.__class__()
            #print "Adding %s"%make
            makeTree.head[make]=self.__class__()
            #print makeTree.head
        m = makeTree.head[make]
        #print makeTree.head
        words = model.split()
        print words
        if words:
            m.model_count += 1
            print "incrementing %s"%
            if words[0] not in m.model_tree:
                #print "adding %s"%words[0],
                m.model_tree[words[0]] = self.__class__() 
            if len(words) >1:
                #print "sending %s to summer camp"%words[1:]

                m.model_tree[words[0]].add(make," ".join(words[1:]))
                

    def make_count(self,make):
        pass

    def model_count_all(self,make,model):
        pass

    def get_models_by_make(self,make):
        if make not in makeTree.head:
            raise ValueError
        l = []
        for k1,v1 in makeTree.head[make].model_tree.iteritems():
            #print "1: %s"%k1 
            for k2,v2 in v1.model_tree.iteritems():
                l.append(k2)
        return l

    def print_models_by_make(self,make):
        if make not in makeTree.head:
            raise ValueError
        for k1,v1 in makeTree.head[make].model_tree.iteritems():
            print "1: %s(%s)"%(k1,v1.model_count)
            for k2,v2 in v1.model_tree.iteritems():
                print "2: %s(%s)"%(k2,v2.model_count)
        

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()


if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        head = makeTree()
        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            body_type = row[3]
            head.add(make,model)

    #print head.get_makes()
    print "==============================="
    head.print_models_by_make("American Motors Corporation")


          
