import os
import ssl
import atexit
from pyVim import connect
from pyVmomi import vim, vmodl


# Disable SSL certificate verification
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
context.verify_mode = ssl.CERT_NONE

# Get environment variables
vc_user = os.environ.get('vc_user')
vc_pwd = os.environ.get('vc_pwd')
esx_user = os.environ.get('esx_user')
esx_pwd = os.environ.get('esx_pwd')
vcenter_name = os.environ.get('vCenter_name')
cluster_name = os.environ.get('Cluster_name')

# Connect to vCenter
vc_secure = vim.vm.auth.Credentials(
    plainText=vc_pwd.encode('utf-8')
)
vc_cred = vim.vm.auth.UsernamePassword(
    username=vc_user,
    password=vc_secure
)
try:
    si = connect.SmartConnect(
        host=vcenter_name,
        user=vc_user,
        pwd=vc_pwd,
        sslContext=context
    )
    atexit.register(connect.Disconnect, si)
except vmodl.MethodFault as ex:
    print("Caught vmodl fault : " + ex.msg)
    return

# Get VSAN health summary for the cluster
vsan_health_service = si.content.vsanHealthSystem
cluster = si.content.searchIndex.FindByInventoryPath(
    f"/{vcenter_name}/host/{cluster_name}"
)
query = vim.vsan.QueryVsanClusterHealthSummaryRequest()
query.cluster = cluster
result = vsan_health_service.QueryVsanClusterHealthSummary(query)
health_check_groups = result.groups
clomd_liveness = result.clomdLiveness
overall_clomd_status = clomd_liveness.clomdLivenessResult

# Print CLOMD status of hosts
print("\nCLOMD STATUS OF HOSTS")
print("=====================")
for host_status in overall_clomd_status:
    print(f"{host_status.hostname} {host_status.clomdStat}")

# Get affected ESXi hosts
clomd_health = [h for h in overall_clomd_status if h.clomdStat != 'alive']
if clomd_health:
    print("\nAffected Host Details:")
    print("======================")
    for affected_esxi in clomd_health:
        print(f"\nAffected host {affected_esxi.hostname} is in {affected_esxi.connectionState} state")
        print(f"{affected_esxi.hostname} CLOMD STATUS is not healthy")

        # Restart CLOMD service on the affected ESXi hosts
        esx_host = affected_esxi.hostname
        esx_secure = vim.vm.auth.Credentials(
            plainText=esx_pwd.encode('utf-8')
        )
        esx_cred = vim.vm.auth.UsernamePassword(
            username=esx_user,
            password=esx_secure
        )
        try:
            esx_si = connect.SmartConnect(
                host=esx_host,
                user=esx_user,
                pwd=esx_pwd,
                sslContext=context
            )
            atexit.register(connect.Disconnect, esx_si)
        except vmodl.MethodFault as ex:
            print("Caught vmodl fault : " + ex.msg)
            return

        ssh_service = esx_si.content.guestOperationsManager.processManager
        ssh_program_spec = vim.vm.guest.ProcessManager.ProgramSpec(
            programPath='/etc/init.d/clomd',
            arguments=['status', 'start', 'restart', 'status']
        )
        auth = vim.vm.guest.AuthManager.AuthCredentials(
            username=esx_user,
