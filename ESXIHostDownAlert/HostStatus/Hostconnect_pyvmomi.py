import ssl
from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
# from subprocess import check_output

def mmstatus (vc,vc_username,vc_password,Affectedhost):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    si = SmartConnect(host=vc, 
                        user=vc_username,
                        pwd=vc_password, 
                        port=443, 
                        sslContext=context)

    # Retrieve all ESXi hosts managed by vCenter
    content = si.RetrieveContent()
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    esxi_hosts = host_view.view

    # Check the status of each ESXi host
    print(" " )
    print("ESXi Hosts current status:" )
    print(" " )

    for esxi_host in esxi_hosts:
        if esxi_host.name == Affectedhost:
            summary = esxi_host.summary
            #if summary.runtime.connectionState == "connected":
            if summary.runtime.inMaintenanceMode == True :
            
                print("Host: " + esxi_host.name + " is in Maintenance mode")
                MM_status = True
            else:
                print("Host: " + esxi_host.name + " is not in MM")
                MM_status = False
    Disconnect(si)            
    return MM_status


def handler (context,inputs):
    vc = inputs["vc"]
    vc_username = inputs["vc_username"]
    vc_password = inputs["vc_password"]
    Affectedhost = inputs["Affectedhost"]
    ESXI_MM = mmstatus (vc,vc_username,vc_password,Affectedhost)
    print (ESXI_MM)

#handler (inputs)    

