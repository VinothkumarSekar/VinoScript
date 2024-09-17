import requests
import base64
import ast
import json
import tempfile
import re



def idrac_ss (esxi_host,idrac_credentials,jsd_ticket,jira_credentials):

    if re.search(".*.xxx.com", esxi_host):
        temp = esxi_host.split(".",1)
        idrac = temp[0]+ "-idrac."+temp[1]
        headers = {
            'Authorization': f"Basic {idrac_credentials}",
            'Content-Type': 'application/json'}
        
    if re.search(".*.xxx.com", esxi_host):
        temp = esxi_host.split(".",1)
        idrac = temp[0]+ "-ilo."+temp[1]
        headers = {
            'Authorization': f"Basic {idrac_credentials}",
            'Content-Type': 'application/json'
        }
    if re.search(".*.xxx.com", esxi_host):
        temp = esxi_host.split(".",1)
        idrac = temp[0]+ "-idrac.xxx.com"
        headers = {
            'Authorization': f"Basic {idrac_credentials}",
            'Content-Type': 'application/json'}

     


    

    url = f"https://{idrac}/redfish/v1/Dell/Managers/iDRAC.Embedded.1/DellLCService/Actions/DellLCService.ExportServerScreenShot"
    headers = {'Content-Type': 'application/json',
            'Authorization': f'Basic {idrac_credentials}'
            }
    #response = requests.post(url, data=json.dumps({"FileType": "ServerScreenShot"}), headers=headers, verify=False, auth=(idrac_username, idrac_password))
    idrac_response = requests.post(url, headers=headers, data=json.dumps({"FileType": "ServerScreenShot"}), verify=False) 
    print(f'Response code {idrac_response.status_code}') 
    if idrac_response.status_code == 200 :
        data = idrac_response.text
        data = ast.literal_eval(data)
        data = data['ServerScreenShotFile']
        decoded_data = base64.b64decode(data)
        jsd_url = f"https://servicedesk.xxx.com/rest/api/2/issue/{jsd_ticket}/attachments"

        jsd_headers = {
            'X-Atlassian-Token': 'nocheck',
            'Authorization': f"Basic {jira_credentials}"
        }
        with tempfile.TemporaryDirectory() as tmpdirname:
            print('created temporary directory', tmpdirname)
            with open(f"{tmpdirname}/iDRAC_console.png", 'wb') as img_file:
                img_file.write(decoded_data)
            img = open(f"{tmpdirname}/iDRAC_console.png", 'rb')
            files = {'file': ('iDRAC_console.png', img, 'multipart/form-data')}
            #jsd_response = requests.post(jsd_url, auth=(jsd_usr, jsd_pwd), files=files, headers=jsd_headers)
            jsd_response = requests.post(jsd_url, headers=jsd_headers, files=files )
            print(jsd_response.status_code)
            img.close()
            comment_body = 'Refer attachment ' + \
                    '[' + '^' + 'iDRAC_console.png' + ']' + ' for iDRAC console status'
        jira_url = "https://servicedesk.xxx.com"
        comment_api_endpoint = f"/rest/api/2/issue/{jsd_ticket}/comment"
        url = jira_url + comment_api_endpoint
        # Construct payload and header
        jsd_headers = {
        'X-Atlassian-Token': 'nocheck',
        'Authorization': f"Basic {jira_credentials}"

        }
        payload = {
            "body": comment_body
        }
        response = requests.post(url, headers=jsd_headers, json=payload)
    return idrac_response.status_code

   
def handler (context,inputs):
    jsd_ticket = inputs["jsd_ticket"]
    esxi_host = inputs["esxi_host"]
    jira_credentials = inputs["jira_credentials"]
    idrac_credentials = inputs["idrac_credentials"]
    return idrac_ss (esxi_host,idrac_credentials,jsd_ticket,jira_credentials)

#print((handler (inputs)))
