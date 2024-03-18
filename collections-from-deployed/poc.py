
import sys
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

from utilities.main import *

config_file = os.path.join(os.path.expanduser("~/.prismacloud/poc.json"))


my_pc = connect(config_file)


print(my_pc)