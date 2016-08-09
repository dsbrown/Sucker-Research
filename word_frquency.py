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
from operator import itemgetter

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
        #print words
        if words:
            self.count += 1
            #print "incrementing %s"%
            if words[0] not in self.tree:
                #print "adding %s"%words[0],
                self.tree[words[0]] = self.__class__() 
                self.tree[words[0]].name = words[0]
            if len(words) >1:
                #print "sending %s to summer camp"%words[1:]
                self.tree[words[0]].add(" ".join(words[1:]))


    def model_tree(self,model):
        for k,m in self.tree.iteritems():
            if k == model:
                return m
        return None

    # only returns first one that matches
    def model_count(self,model):
        count = 0
        model = model.lower()
        if self.name.lower() == model:
            return self.total_count()
        
        for k,m in self.tree.iteritems():
            if k.lower() == model.lower():
                return m.total_count()
            else:
                count = m.model_count(model)
                if count != 0:
                    return count
        return count

    # returns all that matches
    def total_model_count(self,model):
        count = 0
        model = model.lower()
        if self.name.lower() == model:
            #print "matches node %s"%self.name
            count += self.total_count()
        
        for k,m in self.tree.iteritems():
            #print "going recursive",
            count += m.model_count(model)

        return count


    def total_count(self):
        count = self.count
        for m in self.tree.itervalues():
            count += m.total_count()
        return count

    # returns the keys and the frequency of them for the current tree one level
    def get_key_count(self):
        allkeys = []
        if self.tree:
            for k in self.tree.iterkeys():
                allkeys.append([self.tree[k].name,self.tree[k].count])
            return sorted(allkeys, key=lambda x: x[1],reverse=True )            
        else:
            return None

def incr_on_key(d,k):
    try:
        d[k]+=1
    except:
        d[k]=1
    return d

def percentage_dict(d):
    result = []
    d_sum = sum(d.itervalues())
    for k,v in sorted(d.iteritems(), key=itemgetter(1) ,reverse=True):
        p = v*1.00/d_sum
        result.append([k,p])
    return result



d = enchant.Dict('en_US')

# Prints help if no arguments
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

body_freq = {}
model_freq = {}
make_freq = {}
make_struct = {}
if args.file:
    with open(args.file,'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            year = row[0]
            make = row[1]
            model = row[2]
            model.replace('(','')
            model.replace(')','')
            model.replace('&','')
            body_type = row[3]
            try:
                make_struct[make].add(model)
            except:
                make_struct[make] = makeTree()
                make_struct[make].add(model)

            body_freq = incr_on_key(body_freq,body_type)            
            model_freq = incr_on_key(model_freq,model)
            make_freq = incr_on_key(make_freq,make)            
    f.close

    # model_words = []
    # with open("model_words.txt",'r') as i:
    #     for line in i:
    #         model_words.append(line)
    # i.close()

    with open(args.file,'r') as f:
        reader = csv.reader(f)
        
        for row in reader:
            matchObj_and = re.match( r'(\S+?)&(\S+?)',model) 
            if matchObj_and:
                print model

            year = row[0]
            make = row[1]
            model = row[2]
            body_type = row[3]
            head = make_struct[make]
            #print "Model: %s |"%model,
            #print "Full Model: %s"%model
            words = model.split(' ')
            #print "Split Model: %s"%words
            #print "First word: %s"%words[0]
            nu_model = ""

            pos_rank = [1.0,0.5,0.25]

          

            # First look at the order of the words
            # Preserve word order
            # for i in range(0,len(words)):
            #     model_word.replace('(','')
            #     model_word.replace(')','')
            #     model.replace('&','')
            #     model_word = words[i]
                #if d.check(model_word):
                   

            for i in range(0,len(words)):
                model_word = words[i]
                model_word.replace('(','')
                model_word.replace(')','')
                model.replace('&','')
                #print ">>%s<<"%model_word,   

                score = 0                
                #print "Position %s |"%str(i+1),
                if i < len(pos_rank):
                    score = pos_rank[i]
                else:
                    score = 0

                
                matchObjA = re.match( r'[_=+*^%$#@!]+',model_word)    # Unwanted Punctuation
                matchObj1 = re.match( r'[^a-zA-Z]+',model_word)       # No letters
                matchObj2 = re.match( r'[a-zA-Z]+[0-9]+',model_word)  # Letters and numbers
                matchObj3 = re.match( r'[0-9]+[a-zA-Z]+',model_word)  # Numbers and letters

                mcount = head.total_model_count(model_word)
                tcount = head.total_count()
                wf_percent = mcount*1.0/tcount
                #print "Word frequency: {0:.6f}%".format(wf_percent*100),

                if matchObjA:     # Its unwanted punctuation
                    continue
                if matchObj1:     # Its not composed of letters, probably numbers, maybe some punctuation
                    score += 100*wf_percent
                    #print "Number  {0:.6f}".format(score),
                # Letter Number Combo
                elif matchObj2 or matchObj3:
                    # print "Its a letter-number combo: %s"%model_word
                    # print "It has a model tree word frequency of %s"%wf_percent
                    score += 100*wf_percent
                    #print "Letter Number {0:.6f}".format(score),
                #else:     # Is it an actual word?
                    #if d.check(model_word):
                        # print "Its a real word"
                        # print "It has a model tree word frequency of %s"%wf_percent
                        #score += 800*wf_percent
                        #print "Real word {0:.6f}".format(score),

                #print "Final score %f"%score
                if score > 0.8:
                    nu_model += model_word

                    # is it commonly used in the make





    f.close



    #print head.get_makes()
    # print "==============================="
    # # print head.tree.keys()
    # for k in make_struct.keys():
    #     print "%s: "%k
    #     print make_struct[k].get_key_count()
    # print "==============================="



    print "Makes"
    #print sorted( make_freq.iteritems(), key=itemgetter(1) ,reverse=True)
    count =0
    for p in percentage_dict(make_freq):
        if p[1] >0.0005:
            print p[0],
            percentage = p[1]*100
            print percentage
            print make_struct[p[0]].get_key_count()
            count += 1
    print len(make_freq),
    print count
    print "-----------------------------------------------------------------------------------------"
    # print "Models"
    # print sorted( model_freq.iteritems(), key=itemgetter(1) ,reverse=True)
    #print percentage_dict(model_freq)
    # for p in percentage_dict(model_freq):
    #     if p[1] >0.0005:
    #         print p[1]*100,
    #         print p[0]
    #         count += 1
    # print len(model_freq),
    # print count
    # print "-----------------------------------------------------------------------------------------"    
    # print "Body Styles"
    #print sorted( body_freq.iteritems(), key=itemgetter(1) ,reverse=True)
    # count =0
    # for p in percentage_dict(body_freq):
    #     if p[1] >0.0005:
    #         print p[1]*100,
    #         print p[0]
    #         count += 1
    # print len(body_freq),
    # print count
    #print percentage_dict(body_freq)
    # print "-----------------------------------------------------------------------------------------"    

    # sum = 0
    # for v in model_freq.itervalues():
    #     sum += v
    # print sum

          
