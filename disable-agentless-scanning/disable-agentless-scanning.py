
import argparse
import requests
import json
import os
import pprint
import time


CA_CERT = '/Users/sgordon/globalprotect_certifi.txt'
pp = pprint.PrettyPrinter(indent=5)


argParser = argparse.ArgumentParser()
argParser.add_argument("-v", "--verbose", action='store_true', help="Print Verbose Messages")
argParser.add_argument("-f", "--file", default="policy.json", help="Define Cache File")
argParser.add_argument("-c", "--cache", action='store_true', help="Cache Results")
argParser.add_argument("-x", "--config", action='store', help="Authorization - Config File (~/.prismacloud)",required=True)


args = argParser.parse_args()

configfile = os.path.join(os.path.expanduser('~/.prismacloud'),args.config)

#Verify that authorization file exists and load into memory
if(args.verbose is True):print("Checking if auth config file exists")
if(args.verbose is True):print("Auth Config File >",args.config)
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
TOKEN = requests.post(api_url+"/login", json=payload, verify=CA_CERT).json()['token']
if(args.verbose is True):print("TOKEN", TOKEN)
if(args.verbose is True):print("End Authentication")

#Set Prisma Cloud Headers for Login with token
pceHeaders = {
    'x-redlock-auth': TOKEN,
    'Accept': 'application/json'
}


#response = requests.get(api_url+"/cloud", headers=pceHeaders,verify=CA_CERT).json()

# payload = json.dumps({
#   "accountId": "832533561029",
#   "accountType": "organization",
#   "enabled": True,
#   "name": "AWS - OXY.COM",
#   "roleArn": "arn:aws:iam::832533561029:role/PrismaCloudRole-1209121601476751360"
# })

org_id = "832533561029"
#org_id = "24df34ab-a358-4b62-ba14-e5dfb43b9d63"
org_type = "aws"
#org_type = "azure"

payload = json.dumps({})
#response = requests.post(api_url+"/cas/v1/aws_account/540789011280/children", headers=pceHeaders,verify=CA_CERT,data=payload)

response = requests.get(api_url+"/cloud/"+org_type+"/"+org_id+"/project", headers=pceHeaders,verify=CA_CERT).json()
#response = requests.get(api_url+"/cloud/azure/24df34ab-a358-4b62-ba14-e5dfb43b9d63/project", headers=pceHeaders,verify=CA_CERT).json()

#print(response)
#pp.pprint(response)

for a in response:
    if a["accountType"] == "account":
        if(args.verbose is True):print("Account Name", a["name"],"Account ID",a["accountId"])
        #print(a["accountId"])

        #Get features
        output = requests.get(api_url+"/cloud/aws/"+a["accountId"], headers=pceHeaders,verify=CA_CERT).json()

        payload = {"memberIds":[a["accountId"]],"features":[{"name":"Agentless Scanning","state":"disabled"}]}

        #output = requests.put(api_url+"/cas/api/v1/org/832533561029/features", headers=pceHeaders,verify=CA_CERT,json=payload)
        #time.sleep(1)
        #output = requests.put(api_url+"/cas/api/v1/org/24df34ab-a358-4b62-ba14-e5dfb43b9d63/features", headers=pceHeaders,verify=CA_CERT,json=payload)
        #print(output.text)
        for f in output["features"]:
            if f["name"] == "compute-agentless":
                if f["state"] == "enabled":
                    output_features = requests.put(api_url+"/cas/api/v1/org/"+org_id+"/features", headers=pceHeaders,verify=CA_CERT,json=payload)
                    print(output_features.text)
                    #print(f["state"])



if(args.verbose is True):print("Exit Script")