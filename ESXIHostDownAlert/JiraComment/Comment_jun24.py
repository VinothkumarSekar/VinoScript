import json
import http.client
import ssl
import re
#inputs
  # Get Jira from vRO Inputs
jira_url = "servicedesk-xxx.com"
issue_key = "xxx2"
api_endpoint = f"/rest/api/latest/issue/{issue_key}/comment"
esx_host = 'xx-r12esx01.xxx.com'
#api_endpoint = "/rest/api/latest/issue/xx"
#for each_dict in commentdata:
#   for key in each_dict.keys():
#     if re.search("ticket*", key):
#       print(each_dict[key])
#       firstdata = each_dict[key]
#       table = '||Connected ticket|| User||Creation Time||Description||\n'
#       table += f'{firstdata}'
#     else:
#       print(each_dict)

# data = json.dumps({'body': f"{{panel:title=Linked ticket and User and Creation time and Description |borderStyle=dashed|borderColor=#ccc|titleBGColor=#bababa|bgColor=#ededed}}\n{{noformat}}{firstdata} \n{{noformat}}\n{{panel}}"})
# data += json.dumps({'body': f"||VM Name|| Power Status||\n{firstdata}"})

data = '{' + 'code:title=Final report from workflow:|borderStyle=solid' + '}'+'\n'
data += "vCenter or ESXi is not in production on CMDB. The workflow is ended " + '{' + 'code' + '}'
# // Some comments here
# public String getFoo()
# {
#     return foo;
# }
# {code}
#comment formatting 
# comment_body = "This " + "is a " + "*" + "sample comment." + "*"   # Need to customize the comment
# comment_body = '{' + 'panel:title={}|borderStyle=dashed|borderColor=#ccc|titleBGColor=#bababa|bgColor=#ededed'.format(
#             'Affected host ' + esx_host + ':') + '}\n'
# comment_body += '[' + esx_host + '|' + ' https://' + \
#             esx_host + '/ui' ']'+ ' is reachable over the network' '\n'
# comment_body +=  "This " + "is a " + "*" + "sample comment." + "*"  '\n'
# comment_body +=  'Refer attachment ' + '[' + '^' + 'data-export(5).csv' + ']'  + ' for VM details' '\n'
#comment_body = table 



# API Response call
jsd_headers = {
                # 'X-Atlassian-Token': 'nocheck'
                'Content-Type': 'application/json',
                'Authorization': f'Basic dxxxx',
}

jira_connection = http.client.HTTPSConnection(jira_url, context=ssl._create_unverified_context())
payload = json.dumps({
         "body": data
})
jira_connection.request("POST", api_endpoint, payload, headers=jsd_headers )
response = jira_connection.getresponse()
#print(response)
data = response.read()
data = json.loads(data.decode("utf-8"))

#print(data)

# Check the response status code
if response.status == 201:
    print("Comment added successfully.")
else:
    print("Failed to add the comment. Status code:", response.status)
    print("Error message:", response)

  
