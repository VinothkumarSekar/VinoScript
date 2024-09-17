from datetime import datetime, timedelta
import ssl
from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim
import pytz
import csv
import tempfile
import pandas as pd
import time
import requests
# Set the vCenter server details
vc_host = "xxx-vc04.xxx.com"
vc_user = "administrator@vsphere.local"
vc_pwd = "xxx"
esxi_name = "xxx-r01esx18.xxx.com"


def attach(csv_file, csv_file_name): 
    global comment
    jsd_url = f"https://servicedeskxxx.com/rest/api/2/issue/xxx-239352/attachments"
    jsd_headers = {
    'X-Atlassian-Token': 'nocheck'
    }
    csv_file_uplod = open(csv_file, 'rb')
    files = {'file': (csv_file_name, csv_file_uplod, 'multipart/form-data')}
    jsd_response = requests.post(url=jsd_url, auth=("xx", "xx"), files=files,
                                headers=jsd_headers)
    print(f'Task response: {jsd_response.status_code}')
    print("Task details added to JIRA")
    csv_file_uplod.close() 
       
def comment():
        # inputs
        jira_url = "https://servicedesk-xxx.com"
        api_endpoint = f"/rest/api/2/issue/xxx-239352/comment"
    # comment formatting
    # comment_body = "This " + "is a " + "*" + "sample comment." + "*"   # Need to customize the comment
        # comment_body = '{' + 'panel:title={}|borderStyle=dashed|borderColor=#ccc|titleBGColor=#bababa|bgColor=#ededed'.format(
        #     'Affected host ' + esx_host + ':') + '}\n'
        # comment_body += '[' + esx_host + '|' + ' https://' + \
        #                 esx_host + '/ui' ']' + ' is reachable over the network' '\n'
        # comment_body += "This " + "is a " + "*" + "sample comment." + "*"  '\n'
        comment_body = 'Refer attachment ' + \
            '[' + '^' + 'task_details.csv' + ']' + ' for task details' '\n'
        comment_body += 'Refer attachment ' + \
            '[' + '^' + 'event_details.csv' + ']' + ' for even details' '\n'
    # Construct the API endpoint URL
        url = jira_url + api_endpoint
    # Construct payload and header
        jsd_headers = {
            'X-Atlassian-Token': 'nocheck'
        }
        payload = {
            "body": comment_body
        }
        response = requests.post(url, auth=("svc.xxx", "xxx"), headers=jsd_headers, json=payload)    

# Connect to the vCenter server
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_NONE
si = SmartConnect(host=vc_host, user=vc_user, pwd=vc_pwd, sslContext=context)
# root_folder = si.content.rootFolder
# Retrieve the task manager from the content object
task_manager = si.content.taskManager
# Retrieve the recent tasks from the task manager
recent_tasks = task_manager.recentTask
# Connect to the ESXi host
content = si.RetrieveContent()
# Define the task filter
def tsk_obj():
  task_filter_spec = vim.TaskFilterSpec()
  task_filter_spec.time = vim.TaskFilterSpec.ByTime()
  task_filter_spec.time.beginTime = datetime.now() - timedelta(hours=1)
  task_filter_spec.time.endTime = datetime.now()
  task_filter_spec.time.timeType = vim.TaskFilterSpec.TimeOption.startedTime
  return task_filter_spec
# Create the task collector
task_manager = content.taskManager
task_collector = task_manager.CreateCollectorForTasks(tsk_obj())

# Retrieve the task details
tasks = task_collector.ReadNextTasks(1000)
tasks_dict = {}
tasks_list = []
for task in tasks:
  if task.entityName == esxi_name:
    # if task.descriptionId == MMTask or task.descriptionId == ExitMM or task.descriptionId == hostReboot :
    # print(f"Entity Name: {task.entityName}")
    # print(f"Task Description: {task.descriptionId}")
    # print(f"Task StartTime: {task.startTime}")
    # print(f"Task State: {task.state}")
    # print("---------------------------------------")
    tasks_dict['Entity Name'] = task.entityName
    tasks_dict['TaskDescription'] = task.descriptionId
    tasks_dict['Task StartTime'] = task.startTime
    tasks_dict['Task State'] = task.state
    tasks_list.append(tasks_dict)
    returndata = task.descriptionId

csv_headers = ['Entity Name', 'TaskDescription', 'Task StartTime', 'Task State']
with tempfile.TemporaryDirectory() as tmpdirname:
        print('created temporary task directory', tmpdirname)
        csv_file_name = "task_details.csv"
        csv_file = f"{tmpdirname}/{csv_file_name}"
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(csv_headers)
            for event in tasks_list:
                writer.writerow([event['Entity Name'], event['TaskDescription'], event['Task StartTime'].strftime("%Y-%m-%d %H:%M:%S"), event['Task State']])
        attach(csv_file, csv_file_name)    


         

# ====================================================================================================================================================
# ============================================ EVENT DETAILS GATHER ==================================================================================
def time_obj():
  time_filter = vim.event.EventFilterSpec.ByTime()
  now = datetime.now(tz=pytz.utc)
  time_filter.beginTime = now - timedelta(minutes=120)
  time_filter.endTime = now
  return time_filter



def entity_obj():
  si = SmartConnect(host="xxx-vc04.xxx.com", user="administrator@vsphere.local",
                    pwd="xxx", sslContext=context)
  root_folder = si.content.rootFolder
  view = si.content.viewManager.CreateContainerView(container=root_folder, type=[vim.HostSystem], recursive=True)
  for obj in view.view:
    if obj.name == "xxx-r01esx18.xxx.com":
        hostID = obj._moId
        #print (obj._moId)
  event_type_list = []
  host = vim.HostSystem(hostID)
  byEntity = vim.event.EventFilterSpec.ByEntity(entity=host, recursion="self")
  filter_spec = vim.event.EventFilterSpec(eventTypeId=event_type_list, time=time_obj(), entity=byEntity)
  return filter_spec
def event():
  print("executed EVENT")
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_NONE
  si = SmartConnect(host="xxx-vc04.xxx.com", user="administrator@vsphere.local",
                    pwd="xxx", sslContext=context)
  current_time = si.CurrentTime()
  eventManager = si.content.eventManager
  # root_folder = si.content.rootFolder
  event_collector = eventManager.CreateCollectorForEvents(entity_obj())
  page_size = 1000  # The default and also the max event number per page till vSphere v6.5, you can change it to a smaller value by SetCollectorPageSize().
  events = []
  # while True:
  # If there's a huge number of events in the expected time range, this while loop will take a while.
  events_in_page = event_collector.ReadNextEvents(page_size)

  num_event_in_page = len(events_in_page)
  # if num_event_in_page == 0:
  events_dict = {}
  events_list = []
  for event in events_in_page:
    events_dict['description'] = event.fullFormattedMessage
    events_dict['time'] = event.createdTime
    events_dict['target'] = event.host.name
    events_dict['user'] = event.userName
    events_list.append(events_dict.copy())
  #print(events_list)
  return update_csv(events_list)

def update_csv(events_list):
  csv_headers = ['Description', 'Time', 'Target', 'User']
  with tempfile.TemporaryDirectory() as tmpdirname:
    print('created event temporary directory', tmpdirname)
    csv_file_name = "event_details.csv"
    csv_file = f"{tmpdirname}/{csv_file_name}"
    with open(file=csv_file, mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(csv_headers)
      for event in events_list:
        writer.writerow(
          [event['description'], event['time'].strftime("%Y-%m-%d %H:%M:%S"), event['target'], event['user']])
        
    attach(csv_file, csv_file_name)
    comment()

# Clean up
task_collector.DestroyCollector()

Disconnect(si)
event()
