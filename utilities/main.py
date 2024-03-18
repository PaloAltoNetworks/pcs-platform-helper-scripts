
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

    f = open(config_file,"r")
    config_items = json.loads(f.read())
    f.close()

    r.update(config_items)

    
    if "app_stack" not in r or r["app_stack"] == "":return("Missing app_stack")    
    app_stack = r["app_stack"]

    
    if "identity" not in r or r["identity"] == "":return("Missing Identity")
    identity = r["identity"]

    #Remove from Returned Value
    
    if "secret" not in r or r["secret"] == "":return("Missing secret")
    secret = r["secret"]
    r.pop("secret")

    #Optional
    if "ca_cert" not in r or r["ca_cert"] == "":
        ca_cert=False
    else:
        ca_cert = r["CA_CERT"]


    user_auth = {
    'username':identity,
    'password':secret
    }

    r.update({"api_url":"https://"+app_stack.lower()+".prismacloud.io"})

    r.update({"platform_token":requests.post(r["api_url"]+"/login", json=user_auth, verify=r["CA_CERT"]).json()["token"]})

    platform_headers = {
        'x-redlock-auth': r["platform_token"],
        'Accept': 'application/json'
    }


    r.update({"twistlockUrl":requests.get(r["api_url"]+"/compute/config", headers=platform_headers, verify=r["CA_CERT"]).json()["twistlockUrl"]})

    print()

    r.update({"CWP_token":requests.post(r["twistlockUrl"]+"/api/v1/authenticate", json=user_auth, verify=r["CA_CERT"]).json()["token"]})
    

    return(r)
