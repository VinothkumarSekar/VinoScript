from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import subprocess
import ssl
import csv


# Connect to host
def get_poweron_vm_count (host, user, password):
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
 print("Collecting details from the VMs...")
 vm_list = content.viewManager.CreateContainerView(content.rootFolder, [vim.VirtualMachine], True)
 vms = vm_list.view
 print(vms)


 csv_file = 'vm_details.csv'
 csv_headers = ['Name', 'Power State', 'Memory Size (GB)', 'CPU Count']
 poweredOn_count = 0
 poweredOff_count = 0

 

 with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(csv_headers)

    for vm in vms:
        vm_name = vm.name
        power_state = vm.runtime.powerState
        memory_size_gb = vm.config.hardware.memoryMB / 1024
        cpu_count = vm.config.hardware.numCPU

        # Write VM details to the CSV file
        writer.writerow([vm_name, power_state, memory_size_gb, cpu_count])
        if vm.summary.runtime.powerState == 'poweredOn':
          poweredOn_count += 1
        elif vm.summary.runtime.powerState == 'poweredOff':
          poweredOff_count += 1
        
    
    print("")
    print("VM count and powerstate details: ")
    print(f"PoweredOn VM count: {poweredOn_count}")
    print(f"PoweredOff VM count: {poweredOff_count}")      


 print(f"VM details exported to {csv_file}")

#


# Disconnect from host
 Disconnect(si)
 print(poweredOn_count)
 return poweredOn_count


get_poweron_vm_count (host='xxx-r26esx05.xxx.com', user='root', password='xxxx')
