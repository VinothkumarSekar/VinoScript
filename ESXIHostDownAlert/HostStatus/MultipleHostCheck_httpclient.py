
from urllib import parse
import json
#import requests
import http.client
import ssl


vCenterName = "xxx-vc04.xxx.com"
#esx_host = "xxx-r02esx19.xxx.com"
# vc_user = inputs["vc_user"]
# vc_pwd = inputs["vc_pwd"]


def session_key():
    session_endpoint = "/api/session"
    session_headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Basic xxx'
    }
    #response = requests.request("POST", session_endpoint, auth=(vc_user, vc_pwd), headers=session_headers, verify=False)
    conn = http.client.HTTPSConnection(vCenterName, context=ssl._create_unverified_context())
    conn.request("POST", session_endpoint , headers=session_headers)
    res = conn.getresponse()
    data = res.read()
    api_key = json.loads(data.decode("utf-8"))
    print(api_key)
    # api_key = response.json()
    # print (api_key)
    return api_key
    

# #Getting host ID
def host_id(api_key):
    host_endpoint = "/api/vcenter/host"
    headers = {
        'Accept': 'application/json',
        'vmware-api-session-id': api_key
    }
    conn = http.client.HTTPSConnection(vCenterName, context=ssl._create_unverified_context())
    conn.request("GET", host_endpoint, headers=headers)
    res = conn.getresponse()
    data = res.read()
    #print(data)
    hosts_list = json.loads(data.decode("utf-8"))
    # hosts = hostresponse.text
    #hosts_list = json.loads(hosts)
    affected_hosts_list =[]
    for hosts_dict in hosts_list:
        if hosts_dict["connection_state"] == "Connected":
            print (" ")
            #print(f"Below are the details of affected host: {esx_host}")
            host_name = hosts_dict["name"]
            host_id = hosts_dict["host"]
            host_state = hosts_dict["connection_state"]
            affected_host = hosts_dict["name"].count
            affected_host_count += affected_host

            print (affected_host_count)
            affected_hosts_list += host_name
            print (" ")
            print(f"Host {host_name} is in {host_state} state in vCenter")
            print (" ")
            #break
            if affected_host_count >= 0 :
                print (f'affected hosts count {affected_host_count}')
                print (f'affected_hosts_list : {affected_hosts_list}')
                decision = "donotProceed"
            return affected_host_count , affected_hosts_list , decision

#esx_host = "xxx-r12esx01.xxx.com" #Need to pass affected host value from vRO
api_key = session_key()
host_id = host_id(api_key)

