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
argParser.add_argument("-f", "--file", default="purge_accounts.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)

args = argParser.parse_args()

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = json.loads(connect(config_file))


#Looping Defaults
items = []
page_size = 50

if args.cache:
    items = create_cache(pc,args,"/api/v1/cloud-scan-rules")


#If Cache, then use file to query
print("Read from cache file", args.file)
with open(args.file, 'r') as file:
    items = json.load(file)
if(args.verbose is True):print("Total Records in Cache: ",len(items))   

action_items = []

for index, i in enumerate(items):
    account = items[index]["deleted"]
    if account is True:
        print("Removing Account: ",i["credential"]["accountName"])   
        action_items.append(i)
        pc_request(auth=pc,method="delete",url=pc["twistlockUrl"]+"/api/v1/cloud-scan-rules/"+i["credential"]["accountID"],platform=False,verbose=False)

if(args.verbose is True):print("Total Accounts Deleted",len(action_items))



# with open("action_items.json", 'w') as file:
#     json.dump(action_items, file, indent=3)