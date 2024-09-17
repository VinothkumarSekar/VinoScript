import json
import http.client
import ssl
import re

class GetVcName:
  def __init__(self, host, vrops_username, vrops_password, headers):
    self.host = host
    self.vrops_username = vrops_username
    self.vrops_password = vrops_password
    self.headers = headers
    self.host_id_vrops = None
    self.vrops_token = None
    self.host_vc = None


  def get_vro_token(self):
    print("Getting vROPS Token")
    VROPS = "vrops-xxx.com"
    TOKEN_ENDPOINT = "/suite-api/api/auth/token/acquire"
    TOKEN_PAYLOAD = json.dumps({
      "username": self.vrops_username,
      "password": self.vrops_password
    })
    TOKEN_HEADERS = {
      'Content-Type': 'application/json'
    }
    vrops_token_conn = http.client.HTTPSConnection(VROPS, context=ssl._create_unverified_context())
    vrops_token_conn.request("POST", url=TOKEN_ENDPOINT, headers=TOKEN_HEADERS, body=TOKEN_PAYLOAD)
    vrops_token_res = vrops_token_conn.getresponse()
    vrops_token = vrops_token_res.read()
    vrops_token_str = vrops_token.decode("utf-8").split("<ops:token>")[1].split("</ops:token>")[0]
    self.vrops_token = vrops_token_str

  def vrops_esx_id(self):
    print("Getting Esx ID From vROPS")
    VROPS = "vrops-xxx.com"
    ESX_ID_ENDPOINT = f"/suite-api/api/adapterkinds/Vino/resourcekinds/Datastore/resources?name={self.host}"
    esx_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'vRealizeOpsToken {self.vrops_token}'
    }
    vrops_esxi_conn = http.client.HTTPSConnection(VROPS, context=ssl._create_unverified_context())
    vrops_esxi_conn.request("GET", url=ESX_ID_ENDPOINT, headers=esx_headers)
    vrops_esxi_res = vrops_esxi_conn.getresponse()
    data_esxi = vrops_esxi_res.read()
    data_esxi = json.loads(data_esxi.decode("utf-8"))

    self.host_id_vrops = data_esxi["resourceList"][0]["identifier"]

  def vrops_vc_name(self):
    print("Getting VC name from vROPS")
    VROPS = "vrops-xxxx.com"
    vc_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'vRealizeOpsToken {self.vrops_token}'
    }
    vc_name_endpoint = f"/suite-api/api/resources/{self.host_id_vrops}/relationships/parents"
    vrops_vc_conn = http.client.HTTPSConnection(VROPS, context=ssl._create_unverified_context())
    vrops_vc_conn.request("GET", url=vc_name_endpoint, headers=vc_headers)
    vrops_vc_res = vrops_vc_conn.getresponse()
    data_vc = vrops_vc_res.read()
    data_vc = json.loads(data_vc.decode("utf-8"))['resourceList']
    #print(data_vc)
    for each_dict in data_vc:
      for key in each_dict.keys():
        if key == 'resourceKey':
          vc_details = each_dict['resourceKey']
          vc_name = vc_details['name']
          #print(vc_name)
          if re.search("PoweredOn", vc_name):
            vc = vc_name.split(":")[1]
            self.host_vc = vc
            break

def handler(inputs):
  jsd_creds = inputs["jira_credentials"]
  host = inputs["esxi_host"]
  jsd = inputs["jsd_url"]
  vrops_username = inputs["vrops_username"]
  vrops_password = inputs["vrops_password"]
  headers = {"Accept": "application/json",
             "Authorization": f"Basic {jsd_creds}"
             }

  datastore_vc_name_obj = GetVcName( host, vrops_username, vrops_password, headers)
  #host_vc_name_obj.get_vc_name()
  if datastore_vc_name_obj.host_vc == None:
    print(f"Gathering VC details of Datastore from vRops ")
    datastore_vc_name_obj.get_vro_token()
    datastore_vc_name_obj.vrops_esx_id()
    datastore_vc_name_obj.vrops_vc_name()
  return datastore_vc_name_obj.host_vc


inputs = {
    'jira_credentials' : "jira_credentials",
  'esxi_host' :'W2Cxx-XIO-xxxx',
  "jsd_url" : 'servicedesk.xxxxx.com',
  "vrops_username" : "admin",
  "vrops_password" : 'xxxxx'
}

print (handler(inputs))
