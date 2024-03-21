#!/usr/bin/env python3

# python3 -m venv env
# source env/bin/activate
# pip install requests pprintpp

import requests
import pprint
import json
import argparse
import os
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="results.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)


args = argParser.parse_args()

pp = pprint.PrettyPrinter(indent=4)

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = connect(config_file)

#pp.pprint(pc)

#Looping Defaults
items = []

if args.cache:
    items = create_cache(pc,args,"/api/v1/hosts")


#If Cache, then use file to query
print("Read from cache file", args.file)
with open(args.file, 'r') as file:
    items = json.load(file)
if(args.verbose is True):print("Total Records in Cache: ",len(items))    

collection = []

for item in items:
   for h in item["hosts"]:
        
        if "cluster" in item["hosts"][h] and "namespaces" in item["hosts"][h]:
            cluster = item["hosts"][h]["cluster"]
            namespace = item["hosts"][h]["namespaces"][0]
            #if(args.verbose is True):print("Cluster={};Namespace={};".format(cluster,namespace))
            collection_item = [cluster,namespace]
            if collection_item not in collection:
                collection.append(collection_item)

print("Number of collections to create",len(collection))

for c in collection:

    collection_data = {
    'name':"NS - "+c[0]+" - "+c[1],
    'description':"NS - "+c[0]+" - "+c[1],
    'clusters':[c[0]],
    'namespaces':[c[1]]
    }

    if(args.verbose is True):print(collection_data)



    requests.post(pc["twistlockUrl"]+"/api/v1/collections", headers=pc["cwp_headers"], json=collection_data, verify=pc["ca_cert"])

print("Exit Script")