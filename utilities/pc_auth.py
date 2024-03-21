
import requests
import json

import logging
import contextlib
from http.client import HTTPConnection

# HTTPConnection.debuglevel = 1

# logging.basicConfig()
# logging.getLogger().setLevel(logging.DEBUG)
# requests_log = logging.getLogger("requests.packages.urllib3")
# requests_log.setLevel(logging.DEBUG)
# requests_log.propagate = True


def connect(config_file):
    r = {}

    try:
        f = open(config_file,"r")
        config_items = json.loads(f.read())
        f.close()
        r.update(config_items)
    except:
        a = """
    {   
    "ca_cert"  : "", #(Optional)
    "app_stack": "app,app2,app3", #See URLs https://pan.dev/prisma-cloud/api/cspm/api-urls/
    "identity" : "", #https://docs.prismacloud.io/en/enterprise-edition/content-collections/administration/create-access-keys
    "secret"   : ""
    }"""

        return "File does not exist; Create a file here: "+config_file+" In this format "+a


    if "app_stack" not in r or r["app_stack"] == "":return("Missing app_stack")    
    app_stack = r["app_stack"].lower()
    if app_stack.find("app") >= 0:
        app_stack = app_stack.replace("app","api")
    
    if "identity" not in r or r["identity"] == "":return("Missing Identity")
    identity = r["identity"]

    #Remove from Returned Value
    
    if "secret" not in r or r["secret"] == "":return("Missing Secret")
    secret = r["secret"]
    r.pop("secret")

    #Optional
    if "ca_cert" not in r or r["ca_cert"] == "":
        ca_cert=False
    else:
        ca_cert = r["ca_cert"]

    user_auth = {
    'username':identity,
    'password':secret
    }

    r.update({"api_url":"https://"+app_stack+".prismacloud.io"})

    try:
        r.update({"platform_token":requests.post(r["api_url"]+"/login", json=user_auth, verify=ca_cert).json()["token"]})
    except:
        return "Failed to authenticate to the platform" 

    platform_headers = {
        'x-redlock-auth': r["platform_token"],
        'Accept': 'application/json'
    }

    r.update({"platform_headers":platform_headers})

    try:
        r.update({"twistlockUrl":requests.get(r["api_url"]+"/compute/config", headers=r["platform_headers"], verify=ca_cert).json()["twistlockUrl"]})
    except: 
        return "Failed to GET the compute/config settings"
    
    try:
        r.update({"CWP_token":requests.post(r["twistlockUrl"]+"/api/v1/authenticate", json=user_auth, verify=ca_cert).json()["token"]})
    except:
        return "Failed to authenticate with the CWP console"    
    
    cwp_headers = {
        'Authorization': 'Bearer '+ r["CWP_token"],
        'Accept': 'application/json'
    }

    r.update({"cwp_headers":cwp_headers})

    return(r)
