#!/usr/bin/env python3


import argparse
import requests
import json
import os
import pprint
import sys
from datetime import datetime, timedelta

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *
from pc_cache import *
from pc_api import *


pp = pprint.PrettyPrinter(indent=5)


argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="accounts.json", help="Define Cache File - the file does not need to be created ahead of time")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results to the <--file>")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File In the following directory (~/.prismacloud)",required=True)
argParser.add_argument("-r", "--hours", action='store',default=12, help="How many hours prior should we start the evaluation",required=False)


args = argParser.parse_args()

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = json.loads(connect(config_file))

if(args.verbose is True):print(pc)

#Looping Defaults
items = []
page_size = 50

if args.cache:
    items = create_cache(pc,args,"/api/v1/agentless/hosts-status")


#If Cache, then use file to query
print("Read from cache file", args.file)
with open(args.file, 'r') as file:
    items = json.load(file)
if(args.verbose is True):print("Total Records in Cache: ",len(items))   

if(args.verbose is True):print("Number of Records",len(items))


last_hour_date_time = datetime.now() - timedelta(hours = int(args.hours))



recent_items = []

for index, i in enumerate(items):
    scanTime = items[index]["scanTime"]
    date_object = datetime.strptime(scanTime[0:18], '%Y-%m-%dT%H:%M:%S')
    #if date_object > last_hour_date_time:
    recent_items.append(i)

#print(f"Number of Scans {len(recent_items)} since {last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S')}")


total=0
status = ["Pending","Timeout","Scanned","Permissions","Unsupported","Marketplace","Excluded","Quota","Networking","Internal","Scanned by Defender"]
for s in status:
    matching_records_count = sum(1 for record in recent_items if record.get('category') == s)
    print(f"Status: {s}: {matching_records_count}")
    total += matching_records_count

print(f"Total: {total} {len(recent_items)-total}")

# for i in recent_items:
#     if i['category'] not in status:
#         print(i['category'])


if(args.verbose is True):print("Exit Script")