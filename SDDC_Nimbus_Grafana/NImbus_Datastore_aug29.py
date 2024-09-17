import json
import http.client
import ssl
import re
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect

class GetVcName:
  def __init__(self, datastore, vrops_username, vrops_password, headers, vc_username, vc_password):
    self.datastore = datastore
    self.vrops_username = vrops_username
    self.vrops_password = vrops_password
    self.headers = headers
    self.vc_username = vc_username
    self.vc_password = vc_password
    self.datastore_id_vrops = None
    self.vrops_token = None
    self.datastore_vc = None


  def get_vro_token(self):
    print("Getting vROPS Token")
    VROPS = "vrops-xxxx.com"
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
    DS_ID_ENDPOINT = f"/suite-api/api/adapterkinds/VMWARE/resourcekinds/Datastore/resources?name={self.datastore}"
    datastore_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'vRealizeOpsToken {self.vrops_token}'
    }
    vrops_esxi_conn = http.client.HTTPSConnection(VROPS, context=ssl._create_unverified_context())
    vrops_esxi_conn.request("GET", url=DS_ID_ENDPOINT, headers=datastore_headers)
    vrops_esxi_res = vrops_esxi_conn.getresponse()
    data_esxi = vrops_esxi_res.read()
    data_esxi = json.loads(data_esxi.decode("utf-8"))

    self.datastore_id_vrops = data_esxi["resourceList"][0]["identifier"]

  def vrops_vc_name(self):
    print("Getting VC name from vROPS")
    VROPS = "vrops-xxxx.com"
    vc_headers = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': f'vRealizeOpsToken {self.vrops_token}'
    }
    vc_name_endpoint = f"/suite-api/api/resources/{self.datastore_id_vrops}/relationships/parents"
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
            self.datastore_vc = vc
            break

            
  def get_ds_usage (self):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=self.datastore_vc, 
                        user=self.vc_username,
                        pwd=self.vc_password, 
                        port=443, 
                        sslContext=context)

    content = si.RetrieveContent()
    #print (content)
    datastore_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.Datastore], True)
    nimbusDatastore = datastore_view.view
    print(" " )
    print("Datastore current status:" )
    print(" " )
    vmOwners_dict = {}
    for ds in nimbusDatastore:
        name = ds.name
        capacity = round(ds.summary.capacity / (1024 * 1024 * 1024 * 1024))
        freespace = round(ds.summary.freeSpace / (1024 * 1024 * 1024 * 1024))
        usedspace = capacity - freespace
        usedpercentage = round((usedspace*100/capacity),2)
        Total_VMs = ds.vm
        vm_sizes = {}
        vm_list = []


        for vm in Total_VMs:
            vm_sizes[vm.summary.config.name] = vm.summary.storage.committed


        top_5_vms = sorted(vm_sizes.items(), key=lambda x: x[1], reverse=True)[:5]



        for vm_name, vm_size in top_5_vms:
            print(f"VM: {vm_name}, Size: {vm_size} bytes")
            vm_list = vm_name 
            vm_list.append()
            annotation = vm.config.annotation
            #target = "test_owner:"
            target = "manager:"
            if (target in annotation):
              
              words = annotation.split()
              for i,w in enumerate(words):
                if w == target:
                    # next word
                    print (words[i+1])
                    print (vm_list)

        # for eachVM in Total_VMs:
        #   vmName = eachVM.config.name
        #   annotation = eachVM.config.annotation
        #   target = "test_owner:"
        #   if (target in annotation):
            
        #     words = annotation.split()
        #     for i,w in enumerate(words):
        #       if w == target:
        #           # next word
        #           print (words[i+1])
        #     break
          
        #   #print("test_owner:" in annotation)
        #   print(vmName)

        

    print(f'name: {name}')
    print(f'capacity: {capacity} TB')
    print(f'freespace : {freespace} TB')
    print(f'usedpercentage: {usedpercentage} %')
    #print(Total_VMs)



def handler(inputs):
  jsd_creds = inputs["jira_credentials"]
  datastore = inputs["datastore"]
  vrops_username = inputs["vrops_username"]
  vrops_password = inputs["vrops_password"]
  vc_username = inputs["vc_username"]
  vc_password = inputs["vc_password"]
  headers = {"Accept": "application/json",
             "Authorization": f"Basic {jsd_creds}"
             }

  datastore_vc_name_obj = GetVcName( datastore, vrops_username, vrops_password, headers, vc_username,  vc_password)
  if datastore_vc_name_obj.datastore_vc == None:
    print(f"Gathering VC details of Datastore from vRops ")
    datastore_vc_name_obj.get_vro_token()
    datastore_vc_name_obj.vrops_esx_id()
    datastore_vc_name_obj.vrops_vc_name()
    datastore_vc_name_obj.get_ds_usage()
  return datastore_vc_name_obj.datastore_vc


inputs = {
    'jira_credentials' : "jira_credentials",
  'datastore' :'W2Ixx-XIO-xxxx',
  "jsd_url" : 'servicedesk.xxxx.com',
  "vrops_username" : "admin",
  "vrops_password" : 'xxxxxx',
  "vc_username" : "administrator@vsphere.local",
  "vc_password" : "xxxxxx"
}

print (handler(inputs))
