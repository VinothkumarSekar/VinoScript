import json
import requests
import csv
import tempfile
#Generating VC API Key
def session_key():
  session_endpoint = "https://xxx-vc24.xxx.com/api/session"
  session_headers = {
    'Content-Type': 'application/x-www-form-urlencoded'
  }
  response = requests.request("POST", session_endpoint, auth=("xxxxxx", "7cWxxxxxxxx"),
                              headers=session_headers, verify=False)
  api_key = response.json()
  return api_key
#Getting host ID
def host_id(api_key):
  host_endpoint = "https://xxx-vc24xxx.com/api/vcenter/host"
  headers = {
    'Accept': 'application/json',
    'vmware-api-session-id': api_key
  }
  response = requests.request("GET", host_endpoint, headers=headers, verify=False)
  hosts = response.text
  hosts_list = json.loads(hosts)
  for hosts_dict in hosts_list:
    if hosts_dict["name"] == "xx-r12esx01.xx.com":
      host_id = hosts_dict["host"]
      break
  return host_id
#Checking VMs in host from VC and adding to csv
def vms(host_id):
  vm_endpoint = "https://xxx-vc24.xxx.com.com/api/vcenter/vm"
  headers = {
    'Accept': 'application/json',
    'vmware-api-session-id': api_key
  }
  params = {
    "hosts": host_id
  }
  response = requests.request("GET", vm_endpoint, headers=headers, verify=False, params=params)
  vms = response.text
  vm_list = json.loads(vms)
  with tempfile.TemporaryDirectory() as tmpdirname:
      print('created temporary directory', tmpdirname)
      csv_file = f"{tmpdirname}/data_file.csv"
      with open(csv_file, mode='w', newline='') as data_file:
          csv_writer = csv.writer(data_file)
          count = 0
          for vm_dict in vm_list:
              if count == 0:
                  header = vm_dict.keys()
                  csv_writer.writerow(header)
                  count += 1
              csv_writer.writerow(vm_dict.values())
      #Pushing to JIRA
      jsd_url = f"https://servicedesk-.xxx/rest/api/2/issue/JIRA-239352/attachments"
      jsd_headers = {
          'X-Atlassian-Token': 'nocheck'
      }
      csv_file_uplod = open(f"{tmpdirname}/data_file.csv", 'rb')
      files = {'file': ('data_file.csv', csv_file_uplod, 'multipart/form-data')}
      jsd_response = requests.post(jsd_url, auth=("svc.boxxxx", "Sdxxxxx"), files=files, headers=jsd_headers)
      print(jsd_response.status_code)
      print("Vm details added to JIRA")
      csv_file_uplod.close()
#commenting JIRA
def comment():
    # inputs
    print("started")
    jira_url = "https://servicedesk-.xxx"
    api_endpoint = "/rest/api/2/issue/JIRA-239352/comment"
    issue_key = "JIRA-239352"  # Get Jira from vRO Inputs
    jsd_usr = 'svc.xxxx'
    jsd_pwd = 'Sd!66ZWxxxxxx'
    esx_host = 'xxx-r12esx01.xxx.com.com'
    # comment formatting
    # comment_body = "This " + "is a " + "*" + "sample comment." + "*"   # Need to customize the comment
    comment_body = '{' + 'panel:title={}|borderStyle=dashed|borderColor=#ccc|titleBGColor=#bababa|bgColor=#ededed'.format(
        'Affected host ' + esx_host + ':') + '}\n'
    comment_body += '[' + esx_host + '|' + ' https://' + \
                    esx_host + '/ui' ']' + ' is reachable over the network' '\n'
    comment_body += "This " + "is a " + "*" + "sample comment." + "*"  '\n'
    comment_body += 'Refer attachment ' + '[' + '^' + 'data_file.csv' + ']' + ' for VM details' '\n'
    # Construct the API endpoint URL
    url = jira_url + api_endpoint.replace("{jsd_ticket}", issue_key)
    # Construct payload and header
    jsd_headers = {
        'X-Atlassian-Token': 'nocheck'
    }
    payload = {
        "body": comment_body
    }
    response = requests.post(url, auth=(jsd_usr, jsd_pwd), headers=jsd_headers, json=payload)
    # Check the response status code
    if response.status_code == 201:
        print("Comment added successfully.")
    else:
        print("Failed to add the comment. Status code:", response.status_code)
        print("Error message:", response.text)
api_key = session_key()
host_id = host_id(api_key)
vms(host_id)
comment()
