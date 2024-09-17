from pyVim.connect import SmartConnect, Disconnect
import ssl
import atexit
from pyVmomi import vim
import time

def connect(vc,vc_username,vc_password):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=vc, user=vc_username, pwd=vc_password, port=443, sslContext=context)
    atexit.register(Disconnect, si)
    content = si.RetrieveContent()
    return content

def get_obj(content, vimtype, name ):
    """
    Return an object by name, if name is None the
    first found object is returned
    """
    obj = None
    container = content.viewManager.CreateContainerView(
        content.rootFolder, vimtype, True)
    for c in container.view:
        if name:
            if c.name == name:
                obj = c
                break
        else:
            obj = c
            break

    container.Destroy()
    return obj

def ssh_enable (content,ssh_host):
    host_system = get_obj(content, [vim.HostSystem], ssh_host)
    service_system = host_system.configManager.serviceSystem
    ssh_service = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
    service_system.Stop(ssh_service.key)
    #time.sleep(10)
    ssh_result = [x for x in service_system.serviceInfo.service if x.key == 'TSM-SSH'][0]
    print (ssh_result.running)
    return ssh_result.running 

inputs = {
    'vc' : 'xxx9-vc04.xxx.com',
    'vc_username' : 'administrator@vsphere.local',
    'vc_password' : 'xxx',
    'ssh_host' : 'xxx-r02esx19.xxx.com'
}

def handler (inputs):
    vc = inputs["vc"]
    vc_username = inputs["vc_username"]
    vc_password = inputs["vc_password"]
    ssh_host = inputs["ssh_host"]
    content = connect(vc,vc_username,vc_password)
    print (ssh_enable (content,ssh_host))
handler (inputs)   
