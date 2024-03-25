import requests
import json
import os




def create_cache(pc,args,endpoint,extra_params=None):

    limit = 50
    offset = 0
    pulled_items = []

    print("Rebuilding Cache")
    if os.path.exists(args.file):
        print("Delete Cache File", args.file)
        os.remove(args.file)

    while True:

        payload = {'limit':limit,'offset':offset,'compact':True}
        if extra_params is not None:
            payload.update(extra_params)
        
        response = requests.get(pc["twistlockUrl"]+endpoint, headers=pc["cwp_headers"], params=payload, verify=pc["ca_cert"],)
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

