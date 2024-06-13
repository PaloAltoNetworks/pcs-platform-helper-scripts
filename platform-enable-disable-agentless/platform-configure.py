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
#argParser.add_argument("-f", "--file", default="policy.json", help="Define Cache File")
#argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)
argParser.add_argument("-o", "--org", action='store', help="What is the organization account ID ",required=True)
#argParser.add_argument("-a", "--account", action='store', help="Account ID ")
argParser.add_argument("-t", "--type", choices=['aws', 'azure', 'gcp'], help="Which cloud Type?",required=True)
argParser.add_argument("-f", "--feature", choices=['agentless','serverless'], help="Which cloud Scanning Feature",required=True)
argParser.add_argument("-s", "--status", choices=['enabled', 'disabled'], help="Enable or Disable?",required=True)

args = argParser.parse_args()

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = json.loads(connect(config_file))


cloud_type_type = args.type

#If Org
if args.org is not None:
    org_id = str(args.org)
    response = pc_request(auth=pc,method="get",url=pc["api_url"]+"/cloud/"+cloud_type_type+"/"+org_id+"/project",platform=True,verbose=args.verbose).json()
    
    #print(json.dumps(response))
    members=[]

    for a in response:
        if a["accountId"] != org_id and "::" not in a["accountId"]:
            members.append(a["accountId"])

    if args.feature == 'agentless':
        feature = "Agentless Scanning"
    else:
        feature = "Serverless Function Scanning"

    payload = {"memberIds":members,"features":[{"name":feature,"state":args.status}]}


    pc_request(auth=pc,method="put",url=pc["api_url"]+"/cas/api/v1/org/"+org_id+"/features",platform=True,verbose=args.verbose,payload=payload)


#If Not Org - Below is still under development. 
else:
    account_id = str(args.account)
    response = pc_request(auth=pc,method="get",url=pc["api_url"]+"/cloud/"+cloud_type_type+"/"+account_id,platform=True,verbose=args.verbose).json()
    
    print(json.dumps(response))

    response["features"]

    # payload = {"accountId":response["accountId"],
    #            "accountType":"account","name":response["name"],
    #            "roleArn":response["roleArn"],
    #            "features":[{"name":"Agentless Scanning",
    #            "state":args.agentless}]
    #         }

    #pc_request(auth=pc,method="put",url=pc["api_url"]+"/cas/v1/aws_account/"+account_id,platform=True,verbose=args.verbose,payload=payload)



if(args.verbose is True):print("Exit Script")
