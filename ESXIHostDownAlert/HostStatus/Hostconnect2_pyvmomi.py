
import ssl
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from subprocess import check_output


# vCenter credentials and server information
vcenter_server = "xxx-vc02.xxx.com"
vcenter_username = "xxx"
vcenter_password = "******************"

# Connect to vCenter
si = None
try:
    si = SmartConnect(host=vcenter_server,
                           user=vcenter_username,
                           pwd=vcenter_password)
except ssl.SSLError:
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=vcenter_server, 
                      user=vcenter_username,
                      pwd=vcenter_password, 
                      port=443, 
                      sslContext=context)

except Exception as e:
    print("Could not connect to vCenter server: {}".format(e))
    exit(1)

# Get all ESXi hosts in the vCenter
content = si.RetrieveContent()
host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
esxi_hosts = host_view.view

# Check the status of each ESXi host
for host in esxi_hosts:
    summary = host.summary
    print("Host: {}".format(summary.config.name))
    print("Status: {}".format(summary.overallStatus))
    print("----")

# Disconnect from vCenter
Disconnect(si)
