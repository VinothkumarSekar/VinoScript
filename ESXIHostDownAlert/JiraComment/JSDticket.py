import http.client
import json
conn = http.client.HTTPSConnection("servicedesk-xxx.com")
payload = ''
jira_ticket = None
if jira_ticket is None:
    jira_ticket = str(input("Enter the Jira Ticket Number: "))
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Basic xx',
}
conn.request("GET", "/rest/api/2/issue/{}?fields=summary".format(jira_ticket), payload, headers)
res = conn.getresponse()
data = res.read()
dataResonse = data.decode("utf-8")
#print(dataResonse)
jsonResponse = json.loads(dataResonse)
# print(jsonResponse)
# print(type(jsonResponse))
ticketSummary = jsonResponse['fields']['summary']
print(ticketSummary)
def generateVcenterDetails(vSANCluster:str=None):
    """Generate the vCenter Name, vCenter Cluster Name from vSAN Cluster Name
    Args:
        vSANCluster (str, optional): vSAN Cluster Name, like: xy2-02-vc14z01-vsan. Defaults to None.
    Returns:
        List: Return the names of the vCenter, vCenter Cluster, vSAN Cluster in a single list of string.
    """
    if vSANCluster is None:
        vSANCluster= str(input("Enter vSAN Cluster Name: "))
    vCenterClusterName= vSANCluster.split("-vsan")[0]
    vCenterName = vCenterClusterName[0:-3]+".oc.xxx.com"
    print('\nvCenter: {}'.format(vCenterName))
    print("Cluster Name: {}".format(vCenterClusterName))
    print("vSAN Cluser Name: {}".format(vSANCluster))
    return [vCenterName,vCenterClusterName,vSANCluster]
def filtevSANClusterName(jiraTicketSummary:str=None):
    vSANClusterName = jiraTicketSummary.split(" ")[2]
    print(vSANClusterName)
    return vSANClusterName
Cluster = filtevSANClusterName(jiraTicketSummary=ticketSummary)
clusterDetails = generateVcenterDetails(Cluster)
