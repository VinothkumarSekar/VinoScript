import json
import http.client
import ssl
import xml.etree.ElementTree as ET


class Nsx_Manager:
  def __init__(self, nsx_manager, nsx_credential, nsx_conn, INTSD, Jira_credentials, jira_connection):
    self.nsx_manager = nsx_manager
    self.nsx_credential = nsx_credential
    self.nsx_conn = nsx_conn
    self.INTSD = INTSD
    self.Jira_credentials = Jira_credentials
    self.jira_connection = jira_connection
    self.nsx_comment = None
    self.attachment_json = None


  def nsx_controller_status (self):

    payload = "<nsxcli>\n    <command>show controller list all</command>\n</nsxcli>"
    headers = {
      'Content-Type': 'application/json',
      'Authorization': f'Basic {self.nsx_credential}'
    }
    self.nsx_conn.request("GET", "/api/2.0/vdn/controller", payload, headers)
    res = self.nsx_conn.getresponse()
    data = res.read()


    formated_data = ET.fromstring(data)

    print(formated_data)



    ns_comment = ""
    final_nsx_comment= ""
    affected_controller = []
    nsx_header = f'The Workflow is ended. Current staus of the controllers of NSX Manager : {self.nsx_manager}'

    for x in formated_data.findall('controller'):
      name =x.find('name').text
      id =x.find('id').text
      ipAddress= x.find('ipAddress').text
      status= x.find('status').text


      comment = f'{name}-NSX-{id} ({ipAddress}) is in {status} state' + '\n'

      ns_comment += comment 
      nsx_comment = nsx_header + '\n' + '\n' + ns_comment 

      if status != "RUNNING":

        warning_comment = f'❌ {id} is in {status} state . Need to validate further. '
        final_nsx_comment +=   warning_comment + '\n'
        affected_controller.append(id)

      else:

        final_nsx_comment = f'✅ All the controllers are in connected state. '
        affected_controller.append("No_affected_controller")


      nsx_comment += '\n' + '\n' + final_nsx_comment + '\n'
      self.nsx_comment = nsx_comment




    print(self.nsx_comment)
  

  def nsx_jira_comment (self):

    api_endpoint = f"/rest/api/latest/issue/{self.INTSD}/comment"


    comment_body = '{' + 'code:title=Report from workflow:|borderStyle=solid' + '}'+'\n'
    # comment_body += inputs["comment_body"] + '{' + 'code' + '}'
    comment_body +=  self.nsx_comment + '{' + 'code' + '}'


    jsd_headers = {
                    # 'X-Atlassian-Token': 'nocheck'
                    'Content-Type': 'application/json',
                    'Authorization': f'Basic {self.Jira_credentials}',
    }

    payload = json.dumps({
            "body": comment_body
    })
    self.jira_connection.request("POST", api_endpoint, payload, headers=jsd_headers )
    response = self.jira_connection.getresponse()
    
    data = response.read()
    data = json.loads(data.decode("utf-8"))

    

    if response.status == 201:
        print("Comment added successfully.")
    else:
        print("Failed to add the comment. Status code:", response.status)
        print("Error message:", response)
    
    

def handler(context, inputs):
        nsx_manager = inputs['nsx_manager']
        nsx_credential = inputs['nsx_credential']
        INTSD = inputs["INTSD"]
        Jira_credentials = inputs["Jira_credentials"]
        jira_url = "servicedesk.xxx.com"
        nsx_conn = http.client.HTTPSConnection(nsx_manager, context=ssl._create_unverified_context())
        jira_connection = http.client.HTTPSConnection(jira_url, context=ssl._create_unverified_context())


        nsx_manager_obj = Nsx_Manager(nsx_manager, nsx_credential, nsx_conn ,INTSD, Jira_credentials, jira_connection)

        nsx_manager_obj.nsx_controller_status()
        nsx_manager_obj.nsx_jira_comment()
        
        return nsx_manager_obj.nsx_comment



inputs = {
  'INTSD' : 'JIRA-168709',
  'Jira_credentials': 'xxx==',
  'nsx_manager': 'xx-nsx23.xxx.com',
  'nsx_credential' : 'xxx==',

}

print (handler(inputs))
