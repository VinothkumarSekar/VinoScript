from pyVim import connect
from pyVmomi import vim
import ssl
import atexit

def connect_to_vcenter(vcenter, vcenter_user, vcenter_password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    
    
    try:
        service_instance = connect.SmartConnect(host=vcenter,
                                                user=vcenter_user,
                                                pwd=vcenter_password,
                                                sslContext=context)
        atexit.register(connect.Disconnect, service_instance)
        print (f"Connected to vCenter")
        return service_instance.RetrieveContent()
    except Exception as e:
        print("Error connecting to vCenter: ", str(e))
        return None

def find_host(content, host_name,vcenter):
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    for host in host_view.view:
        if host.name == host_name:
            print(f"Found Host '{host_name}' on vCenter {vcenter}")
            return host
    return None

def enter_maintenance_mode(host,host_name,MM_status):
    try:

        task = host.EnterMaintenanceMode(timeout=0, evacuatePoweredOffVms=True)
        print(f"Host '{host_name}' is being placed in maintenance mode. Task: {task.info.descriptionId}")
        MM_status = "Host is moving to maintenanceMode"
        return MM_status
    except vim.fault.NoPermission:
        print("You don't have the required permission to perform this action.")
    except vim.fault.ToolsUnavailable:
        print("The host is not responding or the VMware Tools are not running.")
    except vim.fault.VmPowerOnDisabled:
        print("The host has running virtual machines that cannot be migrated.")
    except Exception as e:
        print("An error occurred while entering maintenance mode: ", str(e))
    return MM_status



def handler (inputs):
    if __name__ == "__main__":
        vcenter = inputs["vc"]
        vcenter_user = inputs["vc_username"]
        vcenter_password = inputs["vc_password"]
        host_name = inputs["esxi_host"]
        MM_status = "Not able to initiate MM task"

        content = connect_to_vcenter(vcenter, vcenter_user, vcenter_password)
        if not content:
            exit(1)

        host = find_host(content, host_name, vcenter)
        if not host:
            print(f"Host '{host_name}' not found.")
            exit(1)

        task = enter_maintenance_mode(host,host_name,MM_status)
        print (task)    
    return task
    

#handler (inputs)