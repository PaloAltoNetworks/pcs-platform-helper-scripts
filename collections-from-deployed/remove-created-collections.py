# python3 -m venv env
# source env/bin/activate
# pip install requests pprintpp

import requests
import pprint
import json
import argparse
import os
import urllib.parse

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
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




collections = requests.get(api_endpoint+"/api/v1/collections", headers=auth_headers,  verify=CA_CERT).json()

for c in collections:
    if c["name"].startswith("NS"):
        encoded_collection = urllib.parse.quote(c["name"])
        if(args.verbose is True):print("Deleting Collection", c["name"])
        requests.delete(api_endpoint+"/api/v1/collections/"+encoded_collection, headers=auth_headers, verify=CA_CERT)


print("Exit Script")