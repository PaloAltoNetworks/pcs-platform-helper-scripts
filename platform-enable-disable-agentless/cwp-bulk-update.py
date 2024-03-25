#!/usr/bin/env python3


import argparse
import requests
import json
import os
import pprint
import sys


current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *
from pc_cache import *
from pc_api import *


pp = pprint.PrettyPrinter(indent=5)


argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="accounts.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)
argParser.add_argument("-t", "--type", choices=['aws', 'azure', 'gcp'], help="Which cloud Type?",required=True)


args = argParser.parse_args()

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = json.loads(connect(config_file))

payload = {'cloudProviders':args.type,'hubAccount':False}

#Looping Defaults
items = []
page_size = 50

if args.cache:
    items = create_cache(pc,args,"/api/v1/cloud-scan-rules",extra_params=payload)


#If Cache, then use file to query
print("Read from cache file", args.file)
with open(args.file, 'r') as file:
    items = json.load(file)
if(args.verbose is True):print("Total Records in Cache: ",len(items))   


# Pull agentless spec from file
with open("oxy.json", 'r') as file:
    spec_items = json.load(file)

# Enumerate all agentless scan items and make update
for index, i in enumerate(items):
    

    items[index]["agentlessScanSpec"]["regions"] = ["us-east-1"]
    items[index]["agentlessScanSpec"]["scanNonRunning"] = True
    items[index]["agentlessScanSpec"]["skipPermissionsCheck"] = True


    items[index]["agentlessScanSpec"]["hubCredentialID"] = spec_items["hubCredentialID"]
    items[index]["agentlessScanSpec"]["customTags"] = spec_items["customTags"]
    items[index]["agentlessScanSpec"]["proxyCA"] = spec_items["proxyCA"]


# paginate api put by api limits of 'page_size'
for i in range(0, len(items), page_size):
    page_data = items[i:i+page_size]
    pc_request(auth=pc,method="put",url=pc["twistlockUrl"]+"/api/v1/cloud-scan-rules",platform=False,verbose=args.verbose,payload=page_data)
    print("Put Page/Records", len(page_data))