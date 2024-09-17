import ssl
import subprocess
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
from subprocess import check_output

# Specify vCenter server details
host = 'xxx-vc02.xxx.com'
user = 'xxx'
password = 'xxx'
Affected_host = 'xxx-r02esx06.xxxx.com'
# Connect to vCenter server
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=host, 
                      user=user,
                      pwd=password, 
                      port=443, 
                      sslContext=context)

# Retrieve all ESXi hosts managed by vCenter
content = si.RetrieveContent()
host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
esxi_hosts = host_view.view


# Ping each ESXi host
print(" " )
print("ESXi Hosts Ping Result:" )
print(" " )
for host in esxi_hosts :
 if host.name == Affected_host:
    host_ip = host.config.network.vnic[0].spec.ip.ipAddress
    print("IP for host " + host.name + " is " + f'{host_ip}...')
    result = subprocess.run(['ping', '-c', '1', host_ip], stdout=subprocess.PIPE)
    if result.returncode == 0:
        print("Able to ping and " + f'{host_ip} is up')
    else:
        print("Not able to ping and " + f'{host_ip} is down')


# Check the status of each ESXi host
print(" " )
print("ESXi Hosts current status:" )
print(" " )
for esxi_host in esxi_hosts:
 if esxi_host.name == Affected_host:  
    summary = esxi_host.summary
    if summary.runtime.connectionState == "connected":
        print("Host: " + esxi_host.name + " is in Connected State")
        print(" " )
    else:
        print("Host: " + esxi_host.name + " is in " + summary.runtime.connectionState +  " State")
        print(" " )

# Disconnect from vCenter server
Disconnect(si)
