from pyVim import connect
from pyVmomi import vim
import ssl
import atexit

def connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    
    try:
        service_instance = connect.SmartConnect(host=vcenter_host,
                                                user=vcenter_user,
                                                pwd=vcenter_password,
                                                sslContext=context)
        atexit.register(connect.Disconnect, service_instance)
        return service_instance.RetrieveContent()
    except Exception as e:
        print("Error connecting to vCenter: ", str(e))
        return None

def find_host(content, host_name):
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    for host in host_view.view:
        if host.name == host_name:
            return host
    return None

def enter_maintenance_mode(host):
    try:
        task = host.EnterMaintenanceMode(timeout=0, evacuatePoweredOffVms=True)
        return task
    except vim.fault.NoPermission:
        print("You don't have the required permission to perform this action.")
    except vim.fault.ToolsUnavailable:
        print("The host is not responding or the VMware Tools are not running.")
    except vim.fault.VmPowerOnDisabled:
        print("The host has running virtual machines that cannot be migrated.")
    except Exception as e:
        print("An error occurred while entering maintenance mode: ", str(e))
    return None

if __name__ == "__main__":
    vcenter_host = "xxx-vc04.xxx.com"
    vcenter_user = "administrator@vsphere.local"
    vcenter_password = "xxx"
    host_name = "xxx-r01esx18.xxx.com"

    content = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)
    if not content:
        exit(1)

    host = find_host(content, host_name)
    if not host:
        print(f"Host '{host_name}' not found.")
        exit(1)

    task = enter_maintenance_mode(host)
    if task:
        print(f"Host '{host_name}' is being placed in maintenance mode. Task: {task.info.descriptionId}")
