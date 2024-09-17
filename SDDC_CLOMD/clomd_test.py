from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl
import atexit



# Connect to vCenter server

# context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# context.verify_mode = ssl.CERT_NONE

# service_instance = SmartConnect(host=vc, 
#                         user=vc_username,
#                         pwd=vc_password, 
#                         port=443, 
#                         sslContext=context)
# context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# context.verify_mode = ssl.CERT_NONE
# content = service_instance.RetrieveContent()
# from pyVim.connect import SmartConnect, Disconnect
# from pyVmomi import vim

# # vCenter Server details
# vc_host = "xxx-vc04.xxx.com"
# vc_user = "administrator@vsphere.local"
# vc_pass = "xx"
# context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
# context.verify_mode = ssl.CERT_NONE

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import ssl

def main():
    inputs = {
        "Cluster": "xxx-vc04c01",
        "Username": "administrator@vsphere.local",
        "Password": "xxx"
    }

    cluster_name = inputs["Cluster"]
    username = inputs["Username"]
    password = inputs["Password"]
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE

    try:
        si = SmartConnect(
            host="xxx-vc04.xxx.com",
            user=username,
            pwd=password,
            port=443,
            sslContext=context
        )
        
        content = si.RetrieveContent()
        cluster = None
        for child in content.rootFolder.childEntity:
            if hasattr(child, 'hostFolder'):
                cluster = find_cluster(child.hostFolder, cluster_name)
                if cluster:
                    break

        if cluster:
            vsan_health_service = content.vsanHealthSystem
            cluster_view = cluster._GetMoId()
            results = vsan_health_service.VsanQueryVcClusterHealthSummary(cluster_view, None, None, True, None, None, 'defaultView')
            health_check_groups = results.groups
            clomd_liveness = results.clomdLiveness

            overall_clomd_status = clomd_liveness.clomdLivenessResult

            print("CLOMD STATUS OF HOSTS")
            print(" ")

            for entity in overall_clomd_status:
                host_name = entity.hostname
                clomd_stat = entity.clomdStat

                print(f"{host_name} CLOMD status: {clomd_stat}")

        else:
            print(f"Cluster '{cluster_name}' not found.")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        Disconnect(si)

def find_cluster(folder, cluster_name):
    for entity in folder.childEntity:
        if isinstance(entity, vim.ComputeResource) and entity.name == cluster_name:
            return entity
        elif hasattr(entity, 'hostFolder'):
            result = find_cluster(entity.hostFolder, cluster_name)
            if result:
                return result

if __name__ == "__main__":
    main()
