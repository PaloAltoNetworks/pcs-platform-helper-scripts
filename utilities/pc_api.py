
import requests
import json

import logging
import contextlib
from http.client import HTTPConnection



def pc_request(**kwargs):

    if kwargs["verbose"] is True:

        HTTPConnection.debuglevel = 1

        logging.basicConfig()
        logging.getLogger().setLevel(logging.DEBUG)
        requests_log = logging.getLogger("requests.packages.urllib3")
        requests_log.setLevel(logging.DEBUG)
        requests_log.propagate = True


    ca_cert = kwargs["auth"]["ca_cert"]


    if kwargs["platform"] is True:
        headers = kwargs["auth"]["platform_headers"]
    else:
        headers = kwargs["auth"]["cwp_headers"] 

    if kwargs["method"] == "get":

        response = requests.get(kwargs["url"], headers=headers,verify=ca_cert)

    if kwargs["method"] == "put":
        payload = kwargs["payload"]

        response = requests.put(kwargs["url"], headers=headers,verify=ca_cert,json=payload)


    return response

