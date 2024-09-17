import getpass
import pyVmomi
import pyVim.connect
from pyVmomi import vim
from pyVim.connect import SmartConnectNoSSL, Disconnect

vc_user = 'xxx.com'
vc_password = getpass.getpass("Enter vCenter password: ")
esx_user = 'myesxuser'
esx_password = 'myesxpwd'
vcenter = 'xx-vc17.xx.com'

si = None
try:
    si = SmartConnectNoSSL(host=vcenter, user=vc_user, pwd=vc_password)
    print("Connected to vCenter server")
    
    content = si.RetrieveContent()
    cluster_name = 'myvcCluster'
    cluster = None
    for obj in content.viewManager.CreateContainerView(content.rootFolder, [vim.ClusterComputeResource], True):
        if obj.name == cluster_name:
            cluster = obj
            break
    
    vsan_health_service = content.vsanHealthSystem
    vsan_health_summary = vsan_health_service.QueryVsanClusterHealthSummary(cluster=cluster, includeObjUuids=False, 
                                                                          fetchFromCache=True, viewId="defaultView")
    health_check_groups = vsan_health_summary.healthCheck
    clomd_liveness = vsan_health_summary.clomdLiveness
    
    overall_clomd_status = clomd_liveness.clomdLivenessResult
    
    print("\nCLOMD STATUS OF HOSTS")
    print(" ")
    for item in overall_clomd_status:
        print("Hostname: ", item.hostname)
        print("ClomdStat: ", item.clomdStat)
        print()
    
except Exception as e:
    print("Error: ", str(e))
finally:
    if si:
        Disconnect(si)
