# pcs-platform-helper-scripts
Some helper scripts for Prisma Cloud Platform

[![license](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE) [![support](https://img.shields.io/badge/Support%20Level-Community-yellowgreen)](./SUPPORT.md)

## Description

A group of scripts used as helpers for various Prisma Cloud tasks both in CSPM and CWP. 


## Installation

Create a python virtual environment, activate the environment and install the required packages

```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## Configuration

Create an authorization file in the directory `~/.prismacloud`  Below is the syntax of the file:

```
{
    "ca_cert":"",
    "app_stack": "app",
    "identity": "",
    "secret": ""
}
```

`ca_cert` is needed to eliminate some warning messages while using global protect or other VPN services.  To create the ca_cert file you can user the following script: https://github.com/PaloAltoNetworks/prismacloud-api-python/blob/main/scripts/pcs_ssl_configure.py


`app_stack` should match the stack you are connecting to `app,app2,app3,app4`

`identity` is the Prisma Cloud access key

`secret` is the Prisma Cloud secret key

## Executing Scripts

Most of the scripts contain a `-h` option for identifying what is needed for each script, but in general here are some of the flags:

 * `-h` for help
 * `-x` to specify the name of the authentication file in the `~/.prismacloud` directory. For example `-x credentials.json`. The path is hard-coded so just specify the file name.
 * `-c` most of the scripts will build a local cache file and this option will trigger that action. On subsequent calls of the script the `-c` options may not be needed, as the data you are acting on is stored locally. 
 * `-f` will identify the cache file.  Most scripts have a default file, but this option will give you the flexibility to change the file name. 



## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details