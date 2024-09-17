from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim

def unassign_vmnic_from_dvs(host, username, password, dvs_name, vmnic_name):
    try:
        # Connect to vCenter server
        service_instance = SmartConnect(host=host, user=username, pwd=password)
        
        # Search for the Distributed Virtual Switch (DVS)
        dvs = None
        for dvs_obj in service_instance.content.viewManager.CreateContainerView(
            service_instance.content.rootFolder, [vim.DistributedVirtualSwitch], True
        ).view:
            if dvs_obj.name == dvs_name:
                dvs = dvs_obj
                break
        
        if not dvs:
            print(f"DVS named '{dvs_name}' not found.")
            return
        
        # Search for the physical NIC (vmnic)
        host_obj = None
        for host_obj in service_instance.content.viewManager.CreateContainerView(
            service_instance.content.rootFolder, [vim.HostSystem], True
        ).view:
            if host_obj.name == host:
                break
        
        if not host_obj:
            print(f"Host named '{host}' not found.")
            return
        
        network_system = host_obj.configManager.networkSystem
        
        # Find the vDS uplink (vmnic) by name
        uplinks = network_system.networkInfo.vswitch[0].pnic
        target_uplink = None
        for uplink in uplinks:
            if uplink.device == vmnic_name:
                target_uplink = uplink
                break
        
        if not target_uplink:
            print(f"Uplink '{vmnic_name}' not found on host '{host}'.")
            return
        
        # Remove the uplink from the DVS
        dvs_spec = vim.dvs.HostMember.ConfigSpec()
        dvs_spec.operation = vim.ConfigSpecOperation.remove
        dvs_spec.host = host_obj
        dvs_spec.backing = vim.dvs.HostMember.PnicBackingSpec(pnicSpec=[target_uplink])
        dvs_spec.host = host_obj
        
        dvs_config = vim.dvs.ConfigSpec()
        dvs_config.host = [dvs_spec]
        
        dvs.ReconfigureDvs_Task(spec=dvs_config)
        
        print(f"Uplink '{vmnic_name}' successfully removed from DVS '{dvs_name}' on host '{host}'.")
    
    except Exception as e:
        print("An error occurred:", str(e))
    
    finally:
        if service_instance:
            Disconnect(service_instance)

# Update these values with your vCenter and VMNIC information
vcenter_host = "vcenter.example.com"
vcenter_username = "your_username"
vcenter_password = "your_password"
dvs_name = "Your_DVS_Name"
vmnic_name = "vmnic1"

unassign_vmnic_from_dvs(vcenter_host, vcenter_username, vcenter_password, dvs_name, vmnic_name)
