import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import re


def vSANIP (Affected_host, vc , vc_user , vc_pwd):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    service_instance = SmartConnect(host=vc, 
                        user=vc_user,
                        pwd=vc_pwd, 
                        port=443, 
                        sslContext=context)


    content = service_instance.RetrieveContent()
    host_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.HostSystem], True)
    esxi_hosts = host_view.view

    host_ip = ''
    vsan = "vsan no"
    for esxi_host in esxi_hosts:
        if esxi_host.name == Affected_host:
            
            for datastore in esxi_host.datastore:
                if re.search( 'vsan' , datastore.name) :
                 vsanCheck = datastore.name
                 print (vsanCheck)
                 vsan = "vsan yes"
                 host_ip = esxi_host.config.network.vnic[1].spec.ip.ipAddress
                 print (" ")
                 print (f'vSAN IP of Affected ESXI host {esxi_host.name}: {host_ip}')
                 print (" ")  

    for esxi_host in esxi_hosts:    
        print (f'ESXI {esxi_host.name}: host connection state : {esxi_host.summary.runtime.connectionState}')
        if esxi_host.name != Affected_host and esxi_host.summary.runtime.connectionState == "connected":

            ActiveHost = esxi_host.name
            print (" ")
            print (f'One of the healthy hosts : {ActiveHost}')
            print (" ")
            break

    Disconnect(service_instance)
    return host_ip , vsan, ActiveHost

inputs = {
    'esxi_host' : 'xxx-r02esx19.xxx.com',
    'vc' : 'xxx-vc04.xxx.com',
    'vc_username' : 'administrator@vsphere.local',
    'vc_password' : 'xxx'
}

def handler (inputs):
    Affected_host = inputs["esxi_host"]
    vc = inputs["vc"]
    vc_user = inputs["vc_username"]
    vc_pwd = inputs["vc_password"]
    #print (vSANIP (Affected_host, vc , vc_user , vc_pwd ))
    vSANIP (Affected_host, vc , vc_user , vc_pwd)

handler(inputs)

