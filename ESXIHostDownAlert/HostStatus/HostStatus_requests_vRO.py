import json
import requests

def handler(context, inputs):
    vCenterName = inputs["vCenterName"]
    esx_host = inputs["esxi_host"]
    vc_user = inputs["vc_user"]
    vc_pwd = inputs["vc_pwd"]



# vCenterName = "xxx-vc24.xxx.com"
# esx_host = "xxxr12esx01.xxx.com"
# vc_user = "xxx"
# vc_pwd = "xxx"


#Generating VC API Key
    def session_key():
        session_endpoint = f"https://{vCenterName}/api/session"
        session_headers = {
         'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", session_endpoint, auth=(vc_user, vc_pwd),
                              headers=session_headers, verify=False)
        api_key = response.json()
        return api_key
#Getting host ID
    def host_id(api_key , esx_host):
        host_endpoint = f"https://{vCenterName}/api/vcenter/host"
        headers = {
            'Accept': 'application/json',
            'vmware-api-session-id': api_key
        }
        hostresponse = requests.request("GET", host_endpoint, headers=headers, verify=False)
        hosts = hostresponse.text
        hosts_list = json.loads(hosts)
        for hosts_dict in hosts_list:
            if hosts_dict["name"] == esx_host:
                print (" ")
                print(f"Below are the details of affected host: {esx_host}")
                host_name = hosts_dict["name"]
                host_id = hosts_dict["host"]
                host_state = hosts_dict["connection_state"]
                print (" ")
                print(f"Host {host_name} is in {host_state} state in vCenter")
                print (" ")

                break
        return host_name, host_id, host_state



#affectedhost = "xxx-r12esx01.xxx.com" #Need to pass affected host value from vRO
    api_key = session_key()
    host_id = host_id(api_key,esx_host)

