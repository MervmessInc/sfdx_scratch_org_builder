# org_manager.py
__version__ = '0.0.1'

import json
import logging
import os
import sys
import threading

import sfdx_cli_utils as sfdx

# Set the working directory to the location of the file.
#
dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

# Set the Log level
#
logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S')
logger = logging.getLogger()


def clean_org_data(org):
    if "alias" not in org:
        a = { "alias" : "<blank>" }
        org.update(a)

    if "isDevHub" not in org:
        dh = { "isDevHub" : False }
        org.update(dh)

    if "defaultMarker" not in org:
        dm = { "defaultMarker" : "" }
        org.update(dm)

    if "status" not in org:
        s = { "status" : "Active" }
        org.update(s)

    return org


def print_org_details(idx, o):
    print(f"{idx} > {o['username']}, Alias : {o['alias']}, Status : {o['status']}, DevHub : {o['isDevHub']} {o['defaultMarker']}")


def print_org_list(orgs):
    for idx, o in orgs.items():
        print_org_details(idx, o)


def show_menu(org_list):

    non_scratch_orgs = org_list['result']['nonScratchOrgs']
    scratch_orgs = org_list['result']['scratchOrgs']

    print()

    orgs = {}
    index = 1

    for o in non_scratch_orgs:
        org = { index : clean_org_data(o) }
        orgs.update(org)
        index = index + 1

    for o in scratch_orgs:
        org = { index : clean_org_data(o) }
        orgs.update(org)
        index = index + 1

    print_org_list(orgs)

    return orgs


def update_org_list():
    org_list = sfdx.org_list()
    json.dump(org_list, open( "org_list.json", "w" ))

    return org_list


def main():
    logging.debug("main()")

    if os.path.isfile("org_list.json"):
        org_list = json.load(open ( "org_list.json", "r" ))
        t = threading.Thread(target=update_org_list)
        t.start()

    else:
        org_list = update_org_list()

    orgs = show_menu(org_list)
    print()

    choice = input("Enter choice > ")
    
    try:
        org = orgs.get(int(choice))
        sfdx.org_open(org['username'])
    except Exception:
        pass

if __name__ == '__main__':
    main()