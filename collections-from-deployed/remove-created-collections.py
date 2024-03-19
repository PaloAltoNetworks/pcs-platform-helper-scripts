#!/usr/bin/env python3

# python3 -m venv env
# source env/bin/activate
# pip install requests pprintpp

import requests
import pprint
import argparse
import os
import urllib.parse
import sys

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)


args = argParser.parse_args()

pp = pprint.PrettyPrinter(indent=4)


config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = connect(config_file)





collections = requests.get(pc["twistlockUrl"]+"/api/v1/collections", headers=pc["cwp_headers"],  verify=pc["ca_cert"]).json()

for c in collections:
    if c["name"].startswith("NS"):
        encoded_collection = urllib.parse.quote(c["name"])
        if(args.verbose is True):print("Deleting Collection", c["name"])
        requests.delete(pc["twistlockUrl"]+"/api/v1/collections/"+encoded_collection, headers=pc["cwp_headers"], verify=pc["ca_cert"])


print("Exit Script")