import requests

#inputs
jira_url = "https://servicedesk-xxx.com"
api_endpoint = "/rest/api/2/issue/{jsd_ticket}/comment"
issue_key = "xxx"  # Get Jira from vRO Inputs

jsd_usr = 'xxx'
jsd_pwd = ''

esx_host = 'xxx-r12esx01.xxx.com'

#comment formatting 
#comment_body = "This " + "is a " + "*" + "sample comment." + "*"   # Need to customize the comment
comment_body = '{' + 'panel:title={}|borderStyle=dashed|borderColor=#ccc|titleBGColor=#bababa|bgColor=#ededed'.format(
            'Affected host ' + esx_host + ':') + '}\n'
comment_body += '[' + esx_host + '|' + ' https://' + \
            esx_host + '/ui' ']'+ ' is reachable over the network' '\n'
comment_body +=  "This " + "is a " + "*" + "sample comment." + "*"  '\n'
comment_body +=  'Refer attachment ' + '[' + '^' + 'data-export(5).csv' + ']'  + ' for VM details' '\n'



# Construct the API endpoint URL
url = jira_url + api_endpoint.replace("{jsd_ticket}", issue_key)

# Construct payload and header
jsd_headers = {
                'X-Atlassian-Token': 'nocheck'
            }

payload = {
    "body": comment_body
}

response = requests.post(url, auth=(jsd_usr, jsd_pwd), headers=jsd_headers, json=payload)

# Check the response status code
if response.status_code == 201:
    print("Comment added successfully.")
else:
    print("Failed to add the comment. Status code:", response.status_code)
    print("Error message:", response.text)

