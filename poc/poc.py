#!/usr/bin/env python3


import sys
import os
import pprint

pp = pprint.PrettyPrinter(indent=4)

current_dir = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(current_dir, '..', 'utilities')))
from pc_auth import *

#current_dir = os.path.dirname(os.path.abspath(__file__))
#parent_dir = os.path.dirname(current_dir)
#sys.path.append(parent_dir)
#sys.path.append(os.path.expanduser("~/repos/pcs-platform-helper-scripts"))
#from utilities.main import *

#pp = pprint.PrettyPrinter(indent=4)


config_file = os.path.join(os.path.expanduser("~/.prismacloud/credentials.json"))


pc = json.loads(connect(config_file))


#pp.pprint(my_pc)
print(my_pc)

#response = requests.get(my_pc["twistlockUrl"]+"/api/v1/images", headers=my_pc["cwp_headers"], verify=my_pc["ca_cert"]).json()

#print(response)