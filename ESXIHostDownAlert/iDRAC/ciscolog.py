import http.client

import ssl
import json
import requests
import csv
import tempfile

    
conn = http.client.HTTPSConnection("xxxx-r07esx12-idrac.xxxx.com",context = ssl._create_unverified_context())
payload = ''
headers = {
  'Authorization': 'Basic xxx'
}
conn.request("GET", "/redfish/v1/Systems/WZP233505SC/LogServices/SEL/Entries", payload, headers)
res = conn.getresponse()
data = res.read()
logdata = json.loads(data.decode("utf-8"))['Members']
logdata = logdata[0:30]
print(len(logdata))
#print(data.decode("utf-8"))
#print(logdata['Members'][0])
with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary directory', tmpdirname)
        csv_file = f"{tmpdirname}/data_file.csv"
        with open(csv_file, mode='w', newline='') as data_file:
          csv_writer = csv.writer(data_file)
          count = 0
          #print(data)
        
            
          for vm_dict in logdata :
                       
            #print (vm_dict)
            if count == 0:
              header = vm_dict.keys()
              csv_writer.writerow(header)
              count += 1
            csv_writer.writerow(vm_dict.values())
            

