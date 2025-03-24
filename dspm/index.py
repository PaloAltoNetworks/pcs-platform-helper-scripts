# python3 -m venv env
# source env/bin/activate
# pip install requests pprintpp

import requests
import pprint
import pandas as pd

pp = pprint.PrettyPrinter(indent=4)
CA_CERT = False

api_endpoint = ""
access_key = ""

regions = [

    "australiaeast",
    "australiasoutheast",
    "australiacentral",
    "centralindia",
    "japaneast",
    "japanwest",
    "southeastasia",
    "anadacentral",
    "northeurope",
    "uksouth",
    "westeurope",
    "swedencentral",
    "centralus",
    "eastus",
    "eastus2",
    "southcentralus",
    "westus",
    "westus3",
    "northcentralus"
]


# Set Prisma Cloud Headers for Login with token
auth_headers = {
    'dig-api-key': access_key,
    'Accept': 'application/json'
}

# Looping Defaults
limit = 50
page = 1
response = True

assets = []
headers = ["name", "cloudProvider", "projectName",
           "cloudEnvironment", "serviceType"]

current_params = {
    "region.in": "",
    "page": 0,
    "size": 50
}

for reg in regions:

    current_params["region.in"] = reg

    response = requests.get(
            api_endpoint+"/v1/assets", headers=auth_headers, verify=CA_CERT, params=current_params)
    totalCount = int(response.headers["x-total-count"])
    if totalCount == 0:
            continue

    #print(f"{reg}")

    while True:

        results = response.json()

        #print(f"Total: {totalCount} {len(results)}")

        for i in results:
            item = {}
            for hd in headers:
                item[hd] = i[hd]
            item["region"] = reg
            assets.append(item)

        if totalCount <= ((current_params['page'] * current_params['size'])+current_params['size']):
            current_params['page'] = 0
            break
        else:
            current_params['page'] += 1
            response = requests.get(
            api_endpoint+"/v1/assets", headers=auth_headers, verify=CA_CERT, params=current_params)


df = pd.DataFrame(assets)

print(df)

