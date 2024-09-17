
import argparse
import getpass
import json
import logging
import os
import re
import requests
import sys
import time
import warnings

from pprint import pprint
from datetime import datetime

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser(description="Python script using Redfish API to get iDRAC System Event Logs (SEL) logs.")
parser.add_argument('-ip',help='iDRAC IP address', required=False)
parser.add_argument('-u', help='iDRAC username', required=False)
parser.add_argument('-p', help='iDRAC password. If you do not pass in argument -p, script will prompt to enter user password which will not be echoed to the screen.', required=False)
parser.add_argument('-x', help='Pass in X-Auth session token for executing Redfish calls. All Redfish calls will use X-Auth token instead of username/password', required=False)
parser.add_argument('--ssl', help='SSL cert verification for all Redfish calls, pass in value \"true\" or \"false\". By default, this argument is not required and script ignores validating SSL cert for all Redfish calls.', required=False)
parser.add_argument('--script-examples', help='Get executing script examples', action="store_true", dest="script_examples", required=False)
parser.add_argument('--get', help='Get current iDRAC SEL log', action="store_true", required=False)
parser.add_argument('--clear', help='Clear iDRAC SEL log', action="store_true", required=False)
args = vars(parser.parse_args())
logging.basicConfig(format='%(message)s', stream=sys.stdout, level=logging.INFO)

def get_iDRAC_version():
    global iDRAC_version
    response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1' % idrac_ip, verify=False,auth=(idrac_username,idrac_password))
    data = response.json()
    if response.status_code == 401:
        print("- ERROR, status code 401 detected, check to make sure your iDRAC script session has correct username/password credentials or if using X-auth token, confirm the session is still active.")
        return
    elif response.status_code != 200:
        print("\n- WARNING, unable to get current iDRAC version installed")
        sys.exit(0)
    server_generation = int(data["Model"].split(" ")[0].replace("G",""))
    if server_generation <= 13:
        iDRAC_version = "old"
    else:
        iDRAC_version = "new"

def check_supported_idrac_version():
    if args["x"]:
        response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Entries' % idrac_ip, verify=False, headers={'X-Auth-Token': args["x"]})
    else:
        response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Entries' % idrac_ip, verify=False, auth=(idrac_username, idrac_password))
    data = response.json()
    if response.status_code == 401:
        logging.warning("\n- WARNING, status code %s returned. Incorrect iDRAC username/password or invalid privilege detected." % response.status_code)
        sys.exit(0)
    elif response.status_code != 200:
        logging.warning("\n- WARNING, iDRAC version installed does not support this feature using Redfish API")
        sys.exit(0)

def get_SEL_logs():
    try:
        os.remove("iDRAC_SEL_logs.txt")
    except:
        logging.info("- INFO, unable to locate file %s, skipping step" % "iDRAC_SEL_logs.txt")
    open_file = open("iDRAC_SEL_logs.txt","w")
    date_timestamp = datetime.now()
    logging.info("\n- INFO, getting iDRAC SEL details, this may take 15-30 seconds to complete depending on log size")
    current_date_time = "- Data collection timestamp: %s-%s-%s  %s:%s:%s\n" % (date_timestamp.month, date_timestamp.day, date_timestamp.year, date_timestamp.hour, date_timestamp.minute, date_timestamp.second)
    open_file.writelines(current_date_time)
    open_file.writelines("\n\n")
    if iDRAC_version == "old":
        uri = "/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel"
    elif iDRAC_version == "new":
        uri = "/redfish/v1/Managers/iDRAC.Embedded.1/LogServices/Sel/Entries"
    if args["x"]:
        response = requests.get('https://%s%s' % (idrac_ip, uri), verify=False, headers={'X-Auth-Token': args["x"]})
    else:
        response = requests.get('https://%s%s' % (idrac_ip, uri), verify=False, auth=(idrac_username, idrac_password))
    if response.status_code != 200:
        logging.error("\n- ERROR, GET command failed to get iDRAC SEL entries, status code %s returned" % response.status_code)
        sys.exit(0)
    data = response.json()
    for i in data['Members']:
        for ii in i.items():
            SEL_log_entry = ("%s: %s" % (ii[0],ii[1]))
            print(SEL_log_entry)
            open_file.writelines("%s\n" % SEL_log_entry)
        print("\n")
        open_file.writelines("\n")
    if iDRAC_version == "old":
        number_list = [i for i in range (1,100001) if i % 50 == 0]
        for seq in number_list:
            if args["x"]:
                response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel?$skip=%s' % (idrac_ip, seq), verify=verify_cert, headers={'X-Auth-Token': args["x"]})
            else:
                response = requests.get('https://%s/redfish/v1/Managers/iDRAC.Embedded.1/Logs/Sel?$skip=%s' % (idrac_ip, seq), verify=verify_cert, auth=(idrac_username, idrac_password))
            data = response.json()
            if "Members" not in data or data["Members"] == [] or response.status_code == 400:
                break
            for i in data['Members']:
                for ii in i.items():
                    SEL_log_entry = ("%s: %s" % (ii[0], ii[1]))
                    print(SEL_log_entry)
                    open_file.writelines("%s\n" % SEL_log_entry)
                print("\n")
                open_file.writelines("\n")
    logging.info("\n- INFO, system event logs also captured in \"iDRAC_SEL_logs.txt\" file")
    open_file.close()
    sys.exit(0)


if __name__ == "__main__":
    idrac_ip = "xxx-r07esx01-idrac.xxx.com"
    idrac_username = "xx"
    idrac_password = "xxx"
    check_supported_idrac_version()
    get_iDRAC_version()
    get_SEL_logs()
