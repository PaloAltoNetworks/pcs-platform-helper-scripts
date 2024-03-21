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
from datetime import datetime, timedelta
import pytz

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
limit = 50
offset = 0
items = []
pulled_items = []


if args.cache:
    print("Rebuilding Cache")
    if os.path.exists(args.file):
        print("Delete Cache File", args.file)
        os.remove(args.file)


    while True:

        payload = {'limit':limit,'offset':offset,'compact':True}
        
        response = requests.get(pc["twistlockUrl"]+"/api/v1/hosts", headers=pc["cwp_headers"], params=payload, verify=pc["ca_cert"],)
        if(args.verbose is True):print("Offset & Limit ",offset, limit)
        if(args.verbose is True):print("Status Code ",response.status_code)
        totalRecords = int(response.headers['Total-Count'])
        if(args.verbose is True):print("Total Records ", str(totalRecords))

        if response.status_code == 200:
            results = response.json()
            if(args.verbose is True):print("Results ", len(results))
            pulled_items += results
            

            if len(pulled_items) >= totalRecords:
                break
            else:    
                offset=offset+limit
                if(args.verbose is True):print("Loading Records", "."*int((offset/limit) )) 


    if(args.verbose is True):print("Cache Rebuilt - Saving to File", args.file)
    with open(args.file, 'w') as file:
        json.dump(pulled_items, file, indent=3)
    if(args.verbose is True):print("Finished writing to cache file")

#If Cache, then use file to query
print("Read from cache file", args.file)
with open(args.file, 'r') as file:
    items = json.load(file)
if(args.verbose is True):print("Total Records in Cache: ",len(items))    


collection = []
count=0


utc_time = datetime.now(pytz.utc)

central_timezone = pytz.timezone('US/Central')
current_datetime = datetime.now()
one_hour_ago = timedelta(minutes=10)
one_hour_ago_datetime = current_datetime - one_hour_ago

print("Current time: "+str(current_datetime))

for h in items:

    datetime_obj = datetime.strptime(h["scanTime"], '%Y-%m-%dT%H:%M:%S.%fZ')
    if datetime_obj > one_hour_ago_datetime:
        #print(h["scanTime"]+" --- "+h["hostname"])
        print(datetime_obj.replace(tzinfo=pytz.utc).astimezone(central_timezone))
        count+=1

print("Total Records "+str(count))

print("Exit Script")