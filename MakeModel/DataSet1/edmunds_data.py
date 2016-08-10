#!/usr/bin/env python 
# -*- coding: utf-8 -*-
#
###################################################################################
#                                   
#                                
# Author: David S. Brown
# v1.0  dsb      16 Jun 2016    Original
####################################################################################
# This builds the make/model/year json tables from the enclosed .dat file its kind of 
# throwaway but I am sure it will need to be adapted to other data, so here it sits for
# future use

# edmunds_format =    {
#                       "makes" : [
#                         {
#                           "id" : 200347864,
#                           "models" : [
#                             {
#                               "id" : "AM_General_Hummer",
#                               "years" : [
#                                 {
#                                   "id" : 3407,
#                                   "year" : 1998
#                                 },
#                                 {
#                                   "id" : 1140,
#                                   "year" : 1999
#                                 },
#                                 {
#                                   "id" : 305,
#                                   "year" : 2000
#                                 }
#                               ],
#                               "name" : "Hummer",
#                               "niceName" : "hummer"
#                             }
#                           ],
#                           "name" : "AM General",
#                           "niceName" : "am-general"
#                         },
#                     ],
#                       "makesCount" : 62
#                     }


import json
import argparse
import os
from nested_dict import nested_dict

#import re

parser = argparse.ArgumentParser(description="Load the django database with Make Model Year data provided by Edmunds")
parser.add_argument("-i", "--infile",  nargs="?", dest="infile", default="Edmunds_Vehicle_Make_Model_Year.json", help="Path to the main input file")
parser.add_argument("-c", "--checkfile", nargs="?", dest="checkfile", default="vehicle_years.json", help="Path to the list of manufacturers input file")
#parser.add_argument("-o", "--outfile", nargs="?", dest="outfile", default="more_all_known_makes.dat", help="Path to the list of manufacturers input file")
parser.add_argument("-W", "--overwrite", action='store_true', default=False, dest="overwrite", help="Is it OK to replace an existing file?")
parser.add_argument("-d", "--debug",     action='store_true', default=False,    help="Set debug on")
args = parser.parse_args()

if os.path.isfile(args.infile) and not args.infile.startswith('~'):
    with open(args.infile,'r') as f:
        edmunds_data = json.load(f)
        f.close()
else:
    print "Can't open %s"%args.infile
    exit(1)

for key in edmunds_data.keys():
    print key

makesCount = edmunds_data["makesCount"]

count = 0
makes = []
print "Edmunds Data"
for payload in edmunds_data["makes"]:
    print payload["id"],
    print payload["name"],
    print "/",
    print payload["niceName"]
    makes.append(payload["niceName"])
    count += 1
print "make count %s, found %s"%(makesCount,count)


print "opening %s:"%args.checkfile
if os.path.isfile(args.checkfile) and not args.checkfile.startswith('~'):
     with open(args.checkfile,'r') as f:
        vehicle_years = json.load(f)
        f.close()
else:
    print "Can't open %s"%args.infile
    exit(1)

#print vehicle_years
#print vehicle_years.keys()
print len(vehicle_years.keys())

make_list = []
new_entry = {   "id":0, 
                "models":[],
            }
new_model = {
                "id" : "",
                "years" : [],
                "name" : "",
                "niceName" : "",
            }

for make in vehicle_years.keys():
    make_list.append(make)
    if make not in makes:
        print "%s not in database"%make
        new_entry["id"]     = 0
        new_entry["models"] = []
        print vehicle_years[make]
        for models in vehicle_years[make]:
            print "Model: %s"%models
            new_model={}
            for model_key in models.keys():            
                model_list['id']       = key
                model_list["years"]    = []
                model_list['name']     = model_key.title()
                model_list["niceName"] = model_key

                for year in models[key]:
                    model_list["years"].append({
                                                "id":0,
                                                "year":year,
                                                })
            new_entry["models"].append(new_model)

print new_entry

        
# if not os.path.isfile(args.outfile) or args.overwrite:
#     with open(args.outfile,'w') as e:
#         json.dump(vehicle_years,e)
#         e.close()
# else:
#     print "%s already exists use --overwrite to replace"%args.outfile
#     exit(2)


