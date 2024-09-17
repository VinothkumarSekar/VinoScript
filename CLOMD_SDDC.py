from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl
# import the VSAN API python bindings
import vsanmgmtObjects
import vsanapiutils




def getClusterInstance(clusterName, serviceInstance):
    content = serviceInstance.RetrieveContent()
    searchIndex = content.searchIndex
    datacenters = content.rootFolder.childEntity
    for datacenter in datacenters:
        cluster = searchIndex.FindChild(datacenter.hostFolder, clusterName)
        if cluster is not None:
            return cluster
    return None


# Start program
def clomdstat(vCenter,vcUser,vcPwd,Cluster):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    si = SmartConnect(host=vCenter,
                      user=vcUser,
                      pwd=vcPwd,
                      sslContext=context)

    vcMos = vsanapiutils.GetVsanVcMos(si._stub, context=context)
    vchs = vcMos['vsan-cluster-health-system']
    fetchFromCache = True
    cluster = getClusterInstance(Cluster, si)
    healthSummary = vchs.QueryClusterHealthSummary(
        cluster=cluster, includeObjUuids=True, fetchFromCache=fetchFromCache)
    clomdStatus = healthSummary.clomdLiveness.clomdLivenessResult
    affectedhost = []
    
    for status in clomdStatus:
        if status.clomdStat != 'alive':
            print(f'{status.hostname} is in state {status.clomdStat}')
            affectedhost.append(status.hostname)

    if affectedhost:
        return affectedhost 
    else:
        affectedhost.append("No_affected_host")
        return affectedhost

def handler (context, inputs):
    
    vcUser = inputs['vcUser']
    vcPwd = inputs['vcPwd']
    vCenter = inputs['vCenter']
    Cluster = inputs['Cluster']
    
    print (clomdstat(vCenter,vcUser,vcPwd,Cluster))

    return clomdstat(vCenter,vcUser,vcPwd,Cluster)

