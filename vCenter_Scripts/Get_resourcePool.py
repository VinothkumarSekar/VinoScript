from pyVmomi import vim
from pyVim.connect import SmartConnect, Disconnect
import ssl
import getpass

def connect_to_vcenter(host, user, password, port=443):
    context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    context.verify_mode = ssl.CERT_NONE
    service_instance = SmartConnect(host=host, user=user, pwd=password, port=port, sslContext=context)
    print(f"Connection established to vCenter: {host}")
    return service_instance

def get_cluster_resource_pools(service_instance, cluster_name):
    print(f"Gathering OvDC details from cluster : {cluster_name}"+ '\n')
    content = service_instance.RetrieveContent()
    root_folder = content.rootFolder

    # Search for the cluster in the inventory
    container_view = content.viewManager.CreateContainerView(root_folder, [vim.ClusterComputeResource], True)
    cluster = None
    for c in container_view.view:
        if c.name == cluster_name:
            cluster = c
            break
    container_view.Destroy()

    if not cluster:
        raise Exception(f"Cluster '{cluster_name}' not found.")

    # Retrieve the resource pools of the cluster
    resource_pool = cluster.resourcePool 
    #print(f'restest: {resource_pool.resourcePool.name}')
    resource_pools = resource_pool.resourcePool if hasattr(resource_pool, 'resourcePool') else []


    resource_pools_list = []

    for rp in resource_pools:
        resource_pool = rp.name.split(" ")[0]
        #print (resource_pool)
        resource_pools_list.append(resource_pool)


    #print(resource_pools_list)
    return resource_pools_list

def disconnect_vcenter(service_instance):
    Disconnect(service_instance)

if __name__ == "__main__":
    vcenter_user = input('vCenter userName: ')
    vcenter_password = getpass.getpass(prompt='vCenter Password: ')
    cluster_name = input('Cluster Name: ')
 

    clusters = cluster_name.split("-",2)
    vcpart = (str(clusters[2])[:4])
    vcenter_host = clusters[0]+'-'+clusters[1]+'-'+vcpart+ ".xxxx.com"
    
    service_instance = connect_to_vcenter(vcenter_host, vcenter_user, vcenter_password)

    try:
        
        resource_pools = get_cluster_resource_pools(service_instance, cluster_name)
        body = f'Below OvDCs are getting resource from cluster {cluster_name} :' + '\n' + '\n'

        
        for rp in resource_pools:
            
            body += rp + '\n'
        print(body)
            

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        disconnect_vcenter(service_instance)
