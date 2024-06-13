#!/usr/bin/env python3
# Setup
# ./aws-account.py -v -x bb-app4.json -a 394764345852

import argparse
import requests
import json
import os
import pprint
import sys
from datetime import datetime, timedelta
import boto3

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *
from pc_cache import *
from pc_api import *

pp = pprint.PrettyPrinter(indent=5)

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
#argParser.add_argument("-f", "--file", default="accounts.json", help="Define Cache File - the file does not need to be created ahead of time")
#argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results to the <--file>")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File In the following directory (~/.prismacloud)",required=True)
#argParser.add_argument("-r", "--hours", action='store',default=12, help="How many hours prior should we start the evaluation",required=False)
argParser.add_argument("-a", "--account", action='store', help="Account ID/Number",required=True)

args = argParser.parse_args()

account_id = str(args.account)

# Prisma Authenticate

config_file = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",config_file)
pc = json.loads(connect(config_file))

if(args.verbose is True):print(pc)



# Check Status for Prisma
# /account/505433372056/config/status
# /cloud/

response = pc_request(auth=pc,method="get",url=pc["api_url"]+"/account/"+account_id+"/config/status",platform=True,verbose=args.verbose).json()
    
print(response[0]['status'])
#if status is "ok" break


# Pull new files from Prisma
# POST /cas/v1/aws_template/
post_data = {
    "accountId": account_id,
    "accountType": "account",
    "awsPartition": "us-east-1",
    "features": [
        "Auto Protect",
        "Serverless Function Scanning",
        "Data Security",
        "Remediation"
    ],
    "customMemberRoleNameEnabled": False,
    "useTenantExternalId": False
}


cft_file = pc_request(auth=pc,method="post",url=pc["api_url"]+"/cas/v1/aws_template",platform=True,verbose=False,payload=post_data).json()
print(cft_file)

# Push new file to AWS cloud formation

stack_name = "PrismaCloudApp--10-23-23 "

session = boto3.Session(profile_name='pan-lab')
cf_client = session.client('cloudformation',region_name='us-east-1')

response = cf_client.update_stack(
    StackName=stack_name,
    TemplateBody=cft_file
  
)


cf_client.get_waiter('stack_update_complete').wait(StackName=stack_name)