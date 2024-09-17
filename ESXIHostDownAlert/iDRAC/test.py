import http.client

import ssl
import json
import requests
import csv
import tempfile

    
conn = http.client.HTTPSConnection("xxx-r07esx12-idrac.xxx.com",context = ssl._create_unverified_context())
payload = ''
headers = {
  'Authorization': 'Basic xxx='
}
conn.request("GET", "/redfish/v1/Systems/WZP233505SC/LogServices/SEL/Entries", payload, headers)
res = conn.getresponse()
data = res.read()
logdata = json.loads(data.decode("utf-8"))['Members']
logdata = logdata[0:30]
print(len(logdata))
csv_file = 'vm_details.csv'
csv_headers = ['Message', 'EventType', 'Created']

with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        csv_file = f"{tmpdirname}/data_file.csv"
        with open(csv_file, mode='w', newline='') as data_file:
          csv_writer = csv.writer(data_file)
          count = 0
          #print(data)
        
            
          for log_dict in logdata :
                       
            if count == 0:
              header = csv_headers
              csv_writer.writerow(header)
              count += 1
            Message = log_dict['Message']
            EventType = log_dict['EventType']
            Created = log_dict['Created']

            csv_writer.writerow([Message,EventType,Created]) 


              
             
        # Pushing to JIRA
        jsd_url = f"https://servicedesk.xxx.com/rest/api/2/issue/INTSD-168709/attachments"
        jsd_headers = {
          'X-Atlassian-Token': 'nocheck',
          "Authorization": 'Basic xxxx=='
        }
        csv_file_uplod = open(f"{tmpdirname}/data_file.csv", 'rb')
        files = {'file': ('data_file.csv', csv_file_uplod, 'multipart/form-data')}
        jsd_response = requests.post(jsd_url, files=files,
                                    headers=jsd_headers)
        print(jsd_response.status_code)
        print("Vm details added to JIRA")

        csv_file_uplod.close()
