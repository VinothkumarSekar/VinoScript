from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import subprocess
import ssl


# Inputs
host = 'xx-r12esx01.xxx.com'
user = 'root'
password = 'xx'


# Connect to host
print("")
print(f"Connecting to ESXi host: {host}")
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=host, 
                      user=user,
                      pwd=password, 
                      port=443, 
                      sslContext=context)

# Retrieve the root folder
content = si.RetrieveContent()

# Get all the virtual machines
print("")
print("Collecting details from all the VMs...")
vm_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
vms = vm_list.view

#Get the VM status and count
poweredOn_count = 0
poweredOff_count = 0

for vm in vms:
    if vm.summary.runtime.powerState == 'poweredOn':
        poweredOn_count += 1
    elif vm.summary.runtime.powerState == 'poweredOff':
        poweredOff_count += 1

# Print the counts
print("")
print("VM count and powerstate details: ")
print(f"PoweredOn VM count: {poweredOn_count}")
print(f"PoweredOff VM count: {poweredOff_count}")


# Get the IP addresses of all virtual machines
print("")
print("Below are the details of poweredOn VMs:")
print("")
for vm in vms:
    vm_name = vm.summary.config.name
    vm_power_state = vm.summary.runtime.powerState
    stateCheck = 'poweredOff'
    #print(f"VM {vm_name} is in {vm_power_state}")
    if vm.summary.guest != None and vm.summary.guest.ipAddress != None and vm.summary.runtime.powerState != stateCheck:
        ip_address = vm.summary.guest.ipAddress
        print(f"VM {vm_name} has IP Address: {ip_address}")
        
        # Ping the virtual machine
        try:
            output = subprocess.check_output(f"ping -c 1 {ip_address}", shell=True)
            print(f"VM {vm_name} is up and reachable over the network")
            print("")
        except subprocess.CalledProcessError:
            print(f"VM {vm_name} is not responding")
            print("")

# Disconnect from host
Disconnect(si)




