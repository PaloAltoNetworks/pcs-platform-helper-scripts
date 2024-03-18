# python3 -m venv env
# source env/bin/activate
# pip install requests pprintpp

import requests
import pprint
import json
import argparse
import os

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="results.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)


args = argParser.parse_args()

pp = pprint.PrettyPrinter(indent=4)
CA_CERT = '/Users/sgordon/globalprotect_certifi.txt'

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)


# Verify that authorization file exists and load into memory
# This block of code is checking if the authorization config file exists.

if(args.verbose is True):print("Checking if auth config file exists")
if(os.path.isfile(config_file)):
    if(args.verbose is True):print("Auth config file exists")
    f = open(config_file,"r")
    config_items = json.loads(f.read())
    f.close()
    if(args.verbose is True):print("API URL",config_items['url'])
    api_endpoint = "https://"+config_items['url']
    if(args.verbose is True):print("Access Key",config_items['identity'])
    access_key = config_items['identity']
    if(args.verbose is True):print("Secret Key","*********")
    secret_key = config_items['secret']
else:
    if(args.verbose is True):print("Auth config does not file exists")
    exit();


user_auth = {
    'username':access_key,
    'password':secret_key
}

#Generate a Token for access to Prisma Cloud CSWP.
print("Start Authentication")
TOKEN = requests.post(api_endpoint+"/api/v1/authenticate", json=user_auth, verify=CA_CERT).json()['token']
if(args.verbose is True):print("TOKEN", TOKEN)
if(args.verbose is True):print("End Authentication")

#Set Prisma Cloud Headers for Login with token
auth_headers = {
    'Authorization': 'Bearer '+TOKEN,
    'Accept': 'application/json'
}

#Looping Defaults
limit = 50
offset = 0
response = True
items = []

#response = requests.get(api_endpoint+"/api/v1/images", headers=auth_headers, verify=CA_CERT).json()
#pp.pprint(response)

if args.cache:
    print("Rebuilding Cache")

    while response:

        payload = {
            'limit':limit,
            'offset':offset,
            'compact':True
        }
        
        response = requests.get(api_endpoint+"/api/v1/images", headers=auth_headers, params=payload, verify=CA_CERT)
        if(args.verbose is True):print("Status code",response.status_code)
        if(args.verbose is True):print("Response Data",response.text)

        offset=offset+limit
        totalRecords = response.headers['Total-Count']
        if(args.verbose is True):print("Total Records", totalRecords)
        items += json.loads(response.text)  

        if int(totalRecords) <= len(items):
            response = False
        else:    
            if(args.verbose is True):print("Offset & Limit",offset, limit)
            if(args.verbose is True):print("Loading Records", "."*int((offset/limit) ))  


    if(args.verbose is True):print("Cache Rebuilt - Saving to File", args.file)
    f = open(args.file,"w")
    f.write(json.dumps(items))
    f.close()
    if(args.verbose is True):print("Finished writing to cache file")

#If Cache, then use file to query
print("Read from cache file", args.file)
f = open(args.file,"r")
items = json.loads(f.read())
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

    #requests.post(api_endpoint+"/api/v1/collections", headers=auth_headers, json=collection_data, verify=CA_CERT)


print("Exit Script")