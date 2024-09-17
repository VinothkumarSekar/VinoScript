import json
import http.client
import ssl
from nsxv_controller import nsx_controller_status


def handler(inputs):
    jira_url = "servicedesk.xxxx.com"
    issue_key = inputs["INTSD"]
    nsx_manager = inputs['nsx_manager']
    nsx_credential = inputs['nsx_credential']
    nsx_comment = (nsx_controller_status (nsx_manager,nsx_credential))
    
    api_endpoint = f"/rest/api/latest/issue/{issue_key}/comment"


    comment_body = '{' + 'code:title=Report from workflow:|borderStyle=solid' + '}'+'\n'
    # comment_body += inputs["comment_body"] + '{' + 'code' + '}'
    comment_body +=  nsx_comment + '{' + 'code' + '}'

  
    jsd_headers = {
                    # 'X-Atlassian-Token': 'nocheck'
                    'Content-Type': 'application/json',
                    'Authorization': f'Basic {inputs["Jira_credentials"]}',
    }

    jira_connection = http.client.HTTPSConnection(jira_url, context=ssl._create_unverified_context())
    payload = json.dumps({
            "body": comment_body
    })
    jira_connection.request("POST", api_endpoint, payload, headers=jsd_headers )
    response = jira_connection.getresponse()
    
    data = response.read()
    data = json.loads(data.decode("utf-8"))

   

    if response.status == 201:
        print("Comment added successfully.")
    else:
        print("Failed to add the comment. Status code:", response.status)
        print("Error message:", response)



inputs = {
    'INTSD' : 'Ixxxxx-168709',
    'Jira_credentials': 'xx',
    'nsx_manager': 'nsx23.xxxx.com',
    'nsx_credential' : 'xxx',

}

handler(inputs)
