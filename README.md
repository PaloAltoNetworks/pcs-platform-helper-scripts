# pcs-platform-helper-scripts
Some helper scripts for Prisma Cloud Platform

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description

Script to help find polices that are not attached to alert rules. 

## Installation

`
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
`

## Executing Script

Must use the `-c` option the first time to pull down all the policies data. This will store the policy data in a file called `policy.json`

`policy.json `is the default, but can be defined with the `-f` flag

`
python policy-missing-alert-rule.py -c 
`


## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details