import json
import requests
import csv
import tempfile


#Getting host ID
def host_id(vc_api_key, old_version, vc, esxi_host):
  if old_version:
    host_endpoint = f"https://{vc}/rest/vcenter/host"
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    response = requests.request("GET", host_endpoint, headers=headers, verify=False)
    hosts = response.text
    hosts_list = json.loads(hosts)["value"]
    for hosts_dict in hosts_list:
      if hosts_dict["name"] == esxi_host:
        host_id = hosts_dict["host"]
        break
    return host_id, hosts_list
  elif not old_version:
    host_endpoint = f"https://{vc}/api/vcenter/host"
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    response = requests.request("GET", host_endpoint, headers=headers, verify=False)
    hosts = response.text
    hosts_list = json.loads(hosts)
    for hosts_dict in hosts_list:
      if hosts_dict["name"] == esxi_host:
        host_id = hosts_dict["host"]
        break
    return host_id, hosts_list






#Checking VMs in host from VC and adding to csv
def vms(host_id, vc, vc_api_key, old_version, jira_credentials, hosts_list):
  if old_version:
    vm_endpoint = f"https://{vc}/rest/vcenter/vm"
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    params = {
      "filter.hosts": host_id
    }
    response = requests.request("GET", vm_endpoint, headers=headers, verify=False, params=params)
    vms = response.text
    vm_list = json.loads(vms)["value"]
    total_vms_count = len(vm_list)
    power_on_vms = 0
    for vm_dict in vm_list:
      for status in vm_dict.values():
        if status == 'POWERED_ON':
          power_on_vms += 1
    if total_vms_count > 0:
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
        # Pushing to JIRA
        jsd_url = f"https://servicedesk-xxxx.com/rest/api/2/issue/xxxx-239352/attachments"
        jsd_headers = {
          'X-Atlassian-Token': 'nocheck',
          "Authorization": f"Basic {jira_credentials}"
        }
        csv_file_uplod = open(f"{tmpdirname}/data_file.csv", 'rb')
        files = {'file': ('data_file.csv', csv_file_uplod, 'multipart/form-data')}
        jsd_response = requests.post(jsd_url, files=files,
                                     headers=jsd_headers)
        print(jsd_response.status_code)
        print("Vm details added to JIRA")

        csv_file_uplod.close()
      if power_on_vms == 0:
        return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)
      elif power_on_vms > 0:
        return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)

    else:
      return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)

  elif not old_version:
    vm_endpoint = f"https://{vc}/api/vcenter/vm"
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    params = {
      "hosts": host_id
    }
    response = requests.request("GET", vm_endpoint, headers=headers, verify=False, params=params)
    vms = response.text
    vm_list = json.loads(vms)
    total_vms_count = len(vm_list)
    power_on_vms = 0
    for vm_dict in vm_list:
      for status in vm_dict.values():
        if status == 'POWERED_ON':
          power_on_vms += 1
    if total_vms_count > 0:
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
        # Pushing to JIRA
        jsd_url = f"https://servicedesk-xxxx.com/rest/api/2/issue/xxxx-239352/attachments"
        jsd_headers = {
          'X-Atlassian-Token': 'nocheck',
          "Authorization": f"Basic {jira_credentials}"
        }
        csv_file_uplod = open(f"{tmpdirname}/data_file.csv", 'rb')
        files = {'file': ('data_file.csv', csv_file_uplod, 'multipart/form-data')}
        jsd_response = requests.post(jsd_url, files=files,
                                     headers=jsd_headers)
        print(jsd_response.status_code)
        print("Vm details added to JIRA")

        csv_file_uplod.close()
      if power_on_vms == 0:
        return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)
      elif power_on_vms > 0:
        return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)
    else:
      return comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list)

def comment(total_vms_count, power_on_vms, host_id, jira_credentials, hosts_list):
  global jsd_creds
  jira_url = "https://servicedesk-.xxxx.com"
  api_endpoint = f"/rest/api/2/issue/xxxx-239352/comment"
  if total_vms_count > 0:
    comment_body = 'Refer attachment ' + \
                   '[' + '^' + 'data_file.csv' + ']' + ' for vm details' + f" There are total {total_vms_count} vms"
  else:
    comment_body = 'No vms in the host'
  # Construct the API endpoint URL
  url = jira_url + api_endpoint
  # Construct payload and header
  jsd_headers = {
    'X-Atlassian-Token': 'nocheck',
    'Authorization': f"Basic {jira_credentials}"

  }
  payload = {
    "body": comment_body
  }
  response = requests.post(url, headers=jsd_headers, json=payload)
  poweronvms_hostid_hostlist = []
  poweronvms_hostid_hostlist.append(power_on_vms)
  poweronvms_hostid_hostlist.append(host_id)
  poweronvms_hostid_hostlist.append(hosts_list)
  return poweronvms_hostid_hostlist

inputs = {
  'vc_api_key' : 'xxx',
  'old_version' : 'True',
  'vc' : 'xxx-vc09.xxxx.com',
  'esxi_host' : 'xxx-r02esx04.xxxx.com',
  'jira_credentials' : 'xx'

}

def handler(inputs):
  vc_api_key = inputs["vc_api_key"]
  old_version = inputs["old_version"]
  vc = inputs["vc"]
  esxi_host = inputs["esxi_host"]
  jira_credentials = inputs["jira_credentials"]
  host_id_esxi_hostlist = host_id(vc_api_key, old_version, vc, esxi_host)
  host_id_esxi = host_id_esxi_hostlist[0]
  hosts_list = host_id_esxi_hostlist[1]
  return vms(host_id_esxi, vc, vc_api_key, old_version, jira_credentials, hosts_list)

handler(inputs)
