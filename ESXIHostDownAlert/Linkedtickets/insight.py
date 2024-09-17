import json
import http.client
import ssl
import re
import time


def esxi_status_in_vc(linked_tickets_list, host_vc, host):
  global vc_creds
  vc_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f'Basic {vc_creds}'
  }
  vc_key_conn = http.client.HTTPSConnection(host_vc, context=ssl._create_unverified_context())
  vc_key_conn.request("POST", url=f"/api/session", headers=vc_headers)
  vc_key_conn_res = vc_key_conn.getresponse()
  vc_key_conn_byte = vc_key_conn_res.read()
  session_key = vc_key_conn_byte.decode("utf-8")
  key = json.loads(session_key)
  vc_header_session = {
    'Accept': 'application/json',
    'xxx-api-session-id': key
  }

  vc_key_conn.request("GET", url=f"/api/vcenter/host", headers=vc_header_session)
  vc_host_conn_res = vc_key_conn.getresponse()
  vc_key_conn_byte = vc_host_conn_res.read()
  host_data = json.loads(vc_key_conn_byte.decode("utf-8"))
  for hosts_dict in host_data:
    if hosts_dict["name"] == host:
      host_state = hosts_dict["connection_state"]
      break
  host_status_in_vc = {"host_status_in_vc": host_state}
  linked_tickets_list.append(host_status_in_vc.copy())
  return linked_tickets_list



def vc_status(linked_tickets_list, headers,jsd_conn, host_vc, host):
  jsd_conn.request("GET", url=f"/rest/insight/1.0/iql/objects?objectSchemaId=1&iql=label={host_vc}", headers=headers)
  jsd_conn_host_res = jsd_conn.getresponse()
  data_jsd_host_id_byte = jsd_conn_host_res.read()
  data = json.loads(data_jsd_host_id_byte.decode("utf-8"))["objectEntries"][0]["attributes"]
  for each_dict in data:
    try:
      host_vc_status = each_dict["objectAttributeValues"][0]["value"]
      if host_vc_status == "In production" or host_vc_status == "In Maintenance" or host_vc_status == "Build In Progress" or host_vc_status == "Decommissioned":
        tickets_host_status = {"host_vc_status": host_vc_status}
        linked_tickets_list.append(tickets_host_status.copy())
        return esxi_status_in_vc(linked_tickets_list, host_vc, host)


    except KeyError:
      pass
  if host_vc_status != "In production" or host_vc_status == "In Maintenance" or host_vc_status == "Build In Progress" or host_vc_status == "Decommissioned":
    print("Host status not in jira")
    tickets_host_status = {"host_vc_status": "Host status not in jira"}
    linked_tickets_list.append(tickets_host_status.copy())
    return esxi_status_in_vc(linked_tickets_list, host_vc, host)



def get_vc_name(linked_tickets_list, headers,jsd_conn, host):
  jsd_conn.request("GET", url=f"/rest/insight/1.0/iql/objects?objectSchemaId=1&iql=label={host}", headers=headers)
  jsd_conn_host_res = jsd_conn.getresponse()
  data_jsd_host_id_byte = jsd_conn_host_res.read()
  data = json.loads(data_jsd_host_id_byte.decode("utf-8"))["objectEntries"][0]["attributes"]

  for each_dict in data:
    try:
      host_vc = each_dict["objectAttributeValues"][0]['referencedObject']['label']
      vc_match = re.search(".*.xxx.com", host_vc)
      if vc_match:
        return vc_status(linked_tickets_list, headers,jsd_conn, host_vc, host)
    except KeyError:
      pass


def host_status(linked_tickets_list, headers, jsd_conn, host):
  jsd_conn.request("GET", url=f"/rest/insight/1.0/iql/objects?objectSchemaId=1&iql=label={host}", headers=headers)
  jsd_conn_host_res = jsd_conn.getresponse()
  data_jsd_host_id_byte = jsd_conn_host_res.read()
  data = json.loads(data_jsd_host_id_byte.decode("utf-8"))["objectEntries"][0]["attributes"]
  for each_dict in data:
    try:
      host_status = each_dict["objectAttributeValues"][0]["value"]
      if host_status == "In production" or host_status == "In Maintenance" or host_status == "Build In Progress" or host_status == "Decommissioned":
        tickets_host_status = {"host_status": host_status}
        linked_tickets_list.append(tickets_host_status.copy())
        return get_vc_name(linked_tickets_list, headers,jsd_conn, host)


    except KeyError:
      pass
  if host != "In production" or host == "In Maintenance" or host == "Build In Progress" or host == "Decommissioned":
    print("Host status not in jira")
    tickets_host_status = {"host_status": "Host status not in jira"}
    linked_tickets_list.append(tickets_host_status.copy())
    return get_vc_name(linked_tickets_list, headers,jsd_conn, host)

def getting_connected_ticket(id, headers, jsd_conn, host):
  jsd_conn.request("GET",
                   url=f"https://servicedesk.xxx.com/rest/insight/1.0/objectconnectedtickets/{id}/tickets",
                   headers=headers)
  jsd_conn_tickets_res = jsd_conn.getresponse()
  jsd_conn_tickets_res_bytes = jsd_conn_tickets_res.read()
  print("Getting Connected Tickets")
  data = json.loads(jsd_conn_tickets_res_bytes.decode("utf-8"))["tickets"]
  n = 0
  linked_tickets_list = []
  for ticket in data:
    n += 1
    connected_tickets = [ticket[key] for key in ticket.keys() if
                         (key == 'key' or key == 'title' or key == 'reporter' or key == 'created')]
    tickets = {f"ticket{n}": connected_tickets}
    linked_tickets_list.append(tickets)
  print(f"Linked Tickets:{len(linked_tickets_list)}")
  return host_status(linked_tickets_list, headers, jsd_conn, host)  # This is in format [{'ticket1': ['INTSD-133892', 'JIRAUSER203701', '2023-06-19T09:43:14.000Z', 'sc2-99-r02esx19.oc.xxx.com - Host lost connectivity test']}]

def getting_ticket_key(headers, host, jsd_conn):
  jsd_conn.request("GET", url=f"/rest/insight/1.0/iql/objects?objectSchemaId=1&iql=label={host}", headers=headers)
  jsd_conn_res = jsd_conn.getresponse()
  data_jsd_id_byte = jsd_conn_res.read()
  print("Getting Object ID for the tickets related to host")
  id = json.loads(data_jsd_id_byte.decode("utf-8"))["objectEntries"][0]["id"]
  return getting_connected_ticket(id, headers, jsd_conn, host)

def handler(inputs):
  global vc_creds
  jsd_creds = inputs["jira_credentials"]
  host = inputs["esxi_host"]
  jsd = inputs["jsd_url"]
  vc_creds = inputs["vc_credentials"]
  headers = {"Accept": "application/json",
             "Authorization": f"Basic {jsd_creds}"
             }

  try:
    jsd_conn = http.client.HTTPSConnection(jsd, context=ssl._create_unverified_context())
    return getting_ticket_key(headers, host, jsd_conn)
  except:
    print("unable to connect to JSD")

inputs = {
"jira_credentials": "xx",
"esxi_host": "xxx-10-r05esx13.oc.xxx.com",
"jsd_url": "servicedesk.xxx.com",
"vc_credentials": ""
}



print(handler(inputs))    



#===================Comment section===============

