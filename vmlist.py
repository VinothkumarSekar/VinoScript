from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import subprocess
import ssl
import csv


# Connect to host
def get_vm (host, user, password):
 context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
 context.verify_mode = ssl.CERT_NONE
 si = SmartConnect(host=host, 
                      user=user,
                      pwd=password, 
                      port=443, 
                      sslContext=context)
 content = si.RetrieveContent()
 container = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
 for c in container.view:
  print(c.name)
  if c.name == None:
    vm = c
    break

get_vm (host='vc-xxxxx.com',  user='***', password='***') 

   
    



