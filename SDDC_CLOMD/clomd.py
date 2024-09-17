from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

# Function to get the VSAN view
def get_vsan_view(content):
    return content.viewManager.CreateContainerView(content.rootFolder, [vim.VsanClusterHealthSystem], True)


# Connect to vCenter server

vc= 'xxx-vc04.oc.vmware.com'
vc_username =  'administrator@vsphere.local'
vc_password = 'xxxx'
port =  443

context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE

service_instance = SmartConnect(host=vc, 
                        user=vc_username,
                        pwd=vc_password, 
                        port=443, 
                        sslContext=context)
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE
content = service_instance.RetrieveContent()

cluster_name = "xxx-vc04c01"

vsan_health_service = get_vsan_view(content)
cluster_view = content.viewManager.CreateContainerView(content.rootFolder, [vim.ClusterComputeResource], True)

for cluster in cluster_view.view:
    if cluster_name == cluster.name:
        cluster_moref = cluster
        break

results = vsan_health_service[0].VsanQueryVcClusterHealthSummary(cluster_moref, None, None, True, None, None, 'defaultView')
health_check_groups = results.groups
clomd_liveness = results.clomdLiveness
overall_clomd_status = clomd_liveness.clomdLivenessResult

print("CLOMD STATUS OF HOSTS")
print("")

for entity in overall_clomd_status:
    host_name = entity.hostname
    clomd_status = entity.clomdStat

    print(host_name, "CLOMD status:", clomd_status)

# Disconnect from vCenter server
Disconnect(service_instance)
