from datetime import datetime, timedelta
import ssl
from pyVim import connect
from pyVmomi import vim
import pytz
import csv
import tempfile
import requests


def comment():
  global jsd_creds
  jira_url = f"https://servicedesk.xxx.com"
  api_endpoint = f"/rest/api/2/issue/{INTSD}/comment"
  comment_body = 'Refer attachment ' + \
                  '[' + '^' + 'event_details.csv' + ']' + ' for event details' '\n'
  comment_body += 'Refer attachment ' + \
                  '[' + '^' + 'task_details.csv' + ']' + ' for task details'
  # Construct the API endpoint URL
  url = jira_url + api_endpoint
  # Construct payload and header
  jsd_headers = {
    'X-Atlassian-Token': 'nocheck',
    'Authorization': f"Basic {jsd_creds}"

  }
  payload = {
    "body": comment_body
  }
  response = requests.post(url, headers=jsd_headers, json=payload)


def attach(csv_file, csv_file_name):
  global jsd_creds
  global jsd_url
  global INTSD
  jsd_url = f"https://servicedesk.xxx.com/rest/api/2/issue/{INTSD}/attachments"
  jsd_headers = {
    'X-Atlassian-Token': 'nocheck',
    'Authorization': f"Basic {jsd_creds}"
  }
  csv_file_uplod = open(csv_file, 'rb')
  files = {'file': (csv_file_name, csv_file_uplod, 'multipart/form-data')}
  jsd_response = requests.post(url=jsd_url, files=files,
                               headers=jsd_headers)
  print(f'Task response: {jsd_response.status_code}')
  print("details added to JIRA")
  csv_file_uplod.close()

def update_task_csv(task_list):
  csv_headers = ['Entity Name', 'TaskDescription', 'Task StartTime', 'Task State']
  with tempfile.TemporaryDirectory() as tmpdirname:
    print('created temporary task directory', tmpdirname)
    csv_file_name = "task_details.csv"
    csv_file = f"{tmpdirname}/{csv_file_name}"
    with open(csv_file, mode='w', newline='') as file:
      writer = csv.writer(file)
      writer.writerow(csv_headers)
      for event in task_list:
        writer.writerow(
          [event['Entity Name'], event['TaskDescription'], event['Task StartTime'].strftime("%Y-%m-%d %H:%M:%S"),
           event['Task State']])
    attach(csv_file, csv_file_name)



def update_event_csv(events_list):
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
#################Task
def tsk_obj():
  task_filter_spec = vim.TaskFilterSpec()
  task_filter_spec.time = vim.TaskFilterSpec.ByTime()
  task_filter_spec.time.beginTime = datetime.now() - timedelta(hours=1)
  task_filter_spec.time.endTime = datetime.now()
  task_filter_spec.time.timeType = vim.TaskFilterSpec.TimeOption.startedTime
  return task_filter_spec

def task(vc, host, vc_username, vc_password, si):
  content = si.RetrieveContent()
  task_manager = content.taskManager
  task_collector = task_manager.CreateCollectorForTasks(tsk_obj())
  tasks = task_collector.ReadNextTasks(1000)
  tasks_dict = {}
  tasks_list = []
  for task in tasks:
    if task.entityName == host:
      tasks_dict['Entity Name'] = task.entityName
      tasks_dict['TaskDescription'] = task.descriptionId
      tasks_dict['Task StartTime'] = task.startTime
      tasks_dict['Task State'] = task.state
      tasks_list.append(tasks_dict)
  return tasks_list


#################Event
def time_obj():
  time_filter = vim.event.EventFilterSpec.ByTime()
  now = datetime.now(tz=pytz.utc)
  time_filter.beginTime = now - timedelta(minutes=120)
  time_filter.endTime = now
  return time_filter

def entity_obj(si, host):
  root_folder = si.content.rootFolder
  view = si.content.viewManager.CreateContainerView(container=root_folder, type=[vim.HostSystem], recursive=True)
  for obj in view.view:
    if obj.name == host:
      hostID = obj._moId
  event_type_list = []
  host_name = vim.HostSystem(hostID)
  byEntity = vim.event.EventFilterSpec.ByEntity(entity=host_name, recursion="self")
  filter_spec = vim.event.EventFilterSpec(eventTypeId=event_type_list, time=time_obj(), entity=byEntity)
  return filter_spec


def event(vc, host, vc_username, vc_password):
  context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
  context.verify_mode = ssl.CERT_NONE
  si = connect.SmartConnect(host=vc, user=vc_username,
                    pwd=vc_password, sslContext=context)
  eventManager = si.content.eventManager
  event_collector = eventManager.CreateCollectorForEvents(entity_obj(si, host))
  page_size = 1000  # The default and also the max event number per page till vSphere v6.5, you can change it to a smaller value by SetCollectorPageSize().
  events_in_page = event_collector.ReadNextEvents(page_size)
  events_dict = {}
  events_list = []
  for event in events_in_page:
    events_dict['description'] = event.fullFormattedMessage
    events_dict['time'] = event.createdTime
    events_dict['target'] = event.host.name
    events_dict['user'] = event.userName
    events_list.append(events_dict.copy())
    return events_list, si

inputs = {
  'INTSD' : 'xxx',
  'jira_credentials' : 'xxx==',
  'esxi_host' : 'xxx-r02esx34.xxx.com',
  'vc' : 'xxx-vc07.xxx.com',
  'vc_username' : 'svc.xxx',
  'vc_password' : 'xxx'
  
}


def handler(inputs):
  global jsd_creds
  global INTSD
  INTSD = inputs["INTSD"]
  jsd_creds = inputs["jira_credentials"]
  host = inputs["esxi_host"]
  vc = inputs["vc"]
  vc_username = inputs["vc_username"]
  vc_password = inputs["vc_password"]
  event_list = event(vc, host, vc_username, vc_password)
  update_event_csv(event_list[0])
  si = event_list[1]
  task_list = task(vc, host, vc_username, vc_password, si)
  update_task_csv(task_list)
  comment()

handler(inputs)
