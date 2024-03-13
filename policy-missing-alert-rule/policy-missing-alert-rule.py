
import argparse
import pandas as pd
import requests
import json
import pygsheets
import os

#If you want to send results to Google Sheets
googleSheetsTitle = "Customer - Missing Policies"
googleSheetsAuthFile = "google-sheets.json"

argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="policy.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)
argParser.add_argument("-g", "--google", action='store_true', help="Send Results to Google sheets")

args = argParser.parse_args()

if (args.google is True):
    gc = pygsheets.authorize(service_file=googleSheetsAuthFile)
    sh = gc.open(googleSheetsTitle)

configfile = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)
if(args.verbose is True):print("Auth Config File >",configfile)


#Verify that authorization file exists and load into memory
if(args.verbose is True):print("Checking if auth config file exists")
if(os.path.isfile(configfile)):
    if(args.verbose is True):print("Auth config file exists")
    f = open(configfile,"r")
    configitems = json.loads(f.read())
    f.close()
    if(args.verbose is True):print("API URL",configitems['url'])
    api_url = "https://"+configitems['url']
    if(args.verbose is True):print("Access Key",configitems['identity'])
    access_key = configitems['identity']
    if(args.verbose is True):print("Secret Key","*********")
    secret_key = configitems['secret']
else:
    if(args.verbose is True):print("Auth config does not file exists")
    exit();

payload = {
    'username':access_key,
    'password':secret_key
}

if(args.verbose is True):print("Start Authentication")
#Generate a Token for access to Prisma Cloud Compute. 
TOKEN = requests.post(api_url+"/login", json=payload).json()['token']
if(args.verbose is True):print("TOKEN", TOKEN)
if(args.verbose is True):print("End Authentication")

#Set Prisma Cloud Headers for Login with token
pceHeaders = {
    'x-redlock-auth': TOKEN,
    'Accept': 'application/json'
}

if args.cache:
    if(args.verbose is True):print("Rebuilding Cache")

    params = {
        'policy.enabled' : True,
        'policy.subtype' : ["run", "run_and_build", "audit", "data_classification", "dns", "malware", "network_event", "network", "ueba", "permissions", "identity"]

    }

    response = requests.get(api_url+"/v2/policy", headers=pceHeaders,params=params)
    if(args.verbose is True):print("Status code",response.status_code)
    if(args.verbose is True):print("Response Data",response.text)

    if(args.verbose is True):print("Write to cache file", args.file)
    f = open(args.file,"w")
    f.write(response.text)
    f.close()
    if(args.verbose is True):print("Finished writing to cache file")


#If Cache, then use file to query
if(args.verbose is True):print("Read from cache file", args.file)
f = open(args.file,"r")
policy_items = json.loads(f.read())
if(args.verbose is True):print("Total Records in Cache: ",len(policy_items))


if(args.verbose is True):print("Gather policyId from policy json")
policy_ids = []
for i in policy_items:
    policy_ids.append(i['policyId'])
    
if(args.verbose is True):print("Total PolicyIDs: ",len(policy_ids))    


#Query for enabled Alert Rules
params = {
    'enabled' : True
}

if(args.verbose is True):print("Query for Alert rules")
response = requests.get(api_url+"/v2/alert/rule", headers=pceHeaders,params=params)
if(args.verbose is True):print("Status code",response.status_code)
if(args.verbose is True):print("Response Data",response.text)


#Create list of policies from alert rule(s)
alert_rule_policies = []
for i in json.loads(response.text):
    for p in i['policies']:
        alert_rule_policies.append(p)

if(args.verbose is True):print("Number of policies in alert rules",len(alert_rule_policies))

data=[]
#Start the match process
if(args.verbose is True):print("Start on matching logic")
for i in policy_ids:
    match = False
    for v in alert_rule_policies:
        if i in v:
            match = True
    if match == False:
        for x in policy_items:
            if i == x['policyId']:
                list = [x['policyId'],x['severity'],x['cloudType'],x['policyType'],x['name']]
                data.append(list)

df = pd.DataFrame(data,columns = ["policyId","Severity","cloudType","policyType","PolicyName"])

df.sort_values(by=['Severity'],ascending=True,inplace=True)
print(df)

#Sending Data to Google Sheets
if (args.google is True):
    wks = sh[0]
    wks.set_dataframe(df,(1,1))

if(args.verbose is True):print("Exit Script")
