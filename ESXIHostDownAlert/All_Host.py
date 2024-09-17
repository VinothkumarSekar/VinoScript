import json
import http.client
import ssl
import re


def get_all_cluster(host_id, esxi_host, vc_api_key, old_version, vc):
  if old_version:
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    vc_endpoint = "/rest/vcenter/cluster"
    vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
    vc_conn.request("GET", url=vc_endpoint, headers=headers)
    vc_res = vc_conn.getresponse()
    cluster_list_byte = vc_res.read()
    cluster_list = json.loads(cluster_list_byte.decode("utf-8"))["value"]
    cluster_name_list = []
    for cluster_dict in cluster_list:
      cluster_name_list.append(cluster_dict["cluster"])
    return cluster_name_list

  elif not old_version:
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    vc_endpoint = "/api/vcenter/cluster"
    vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
    vc_conn.request("GET", url=vc_endpoint, headers=headers)
    vc_res = vc_conn.getresponse()
    cluster_list_byte = vc_res.read()
    cluster_list = json.loads(cluster_list_byte.decode("utf-8"))
    cluster_name_list = []
    for cluster_dict in cluster_list:
      cluster_name_list.append(cluster_dict["cluster"])
    return cluster_name_list

def get_host_cluster_name(cluster_names, esxi_host, host_id, vc_api_key, old_version, vc):
  if old_version:
    for cluster in cluster_names:
      headers = {
        'Accept': 'application/json',
        'vmware-api-session-id': vc_api_key
      }
      vc_endpoint = f"/rest/vcenter/host?filter.clusters={cluster}"
      vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
      vc_conn.request("GET", url=vc_endpoint, headers=headers)
      vc_res = vc_conn.getresponse()
      host_list_byte = vc_res.read()
      host_list = json.loads(host_list_byte.decode("utf-8"))["value"]
      for host in host_list:
        if host["host"] == host_id:
          host_cluster_name = cluster
    return host_cluster_name

  elif not old_version:
    for cluster in cluster_names:
      headers = {
        'Accept': 'application/json',
        'vmware-api-session-id': vc_api_key
      }
      vc_endpoint = f"/api/vcenter/host?clusters={cluster}"
      vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
      vc_conn.request("GET", url=vc_endpoint, headers=headers)
      vc_res = vc_conn.getresponse()
      host_list_byte = vc_res.read()
      host_list = json.loads(host_list_byte.decode("utf-8"))
      for host in host_list:
        if host["host"] == host_id:
          host_cluster_name = cluster
    return host_cluster_name

def get_cluster_host_status(host_cluster, esxi_host,host_id, vc_api_key, old_version, vc):
  if old_version:
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    vc_endpoint = f"/rest/vcenter/host?filter.clusters={host_cluster}"
    vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
    vc_conn.request("GET", url=vc_endpoint, headers=headers)
    vc_res = vc_conn.getresponse()
    host_list_byte = vc_res.read()
    host_list = json.loads(host_list_byte.decode("utf-8"))["value"]
    other_notconnected_hosts = []
    other_notconnected_hosts_count = 0
    for host in host_list:
      if host["connection_state"] != "CONNECTED":
        if host["host"] != host_id:
          other_notconnected_hosts.append(host["name"])
          other_notconnected_hosts_count = len(other_notconnected_hosts)
    other_ntconnected_host_and_count = []
    other_ntconnected_host_and_count.append(other_notconnected_hosts)
    other_ntconnected_host_and_count.append(other_notconnected_hosts_count)
    return other_ntconnected_host_and_count


  elif not old_version:
    headers = {
      'Accept': 'application/json',
      'vmware-api-session-id': vc_api_key
    }
    vc_endpoint = f"/rest/vcenter/host?clusters={host_cluster}"
    vc_conn = http.client.HTTPSConnection(vc, context=ssl._create_unverified_context())
    vc_conn.request("GET", url=vc_endpoint, headers=headers)
    vc_res = vc_conn.getresponse()
    host_list_byte = vc_res.read()
    host_list = json.loads(host_list_byte.decode("utf-8"))
    other_notconnected_hosts = []
    other_notconnected_hosts_count = 0
    for host in host_list:
      if host["connection_state"] != "CONNECTED":
        if host["host"] != host_id:
          other_notconnected_hosts.append(host["name"])
          other_notconnected_hosts_count = len(other_notconnected_hosts)
    other_ntconnected_host_and_count = []
    other_ntconnected_host_and_count.append(other_notconnected_hosts)
    other_ntconnected_host_and_count.append(other_notconnected_hosts_count)
    return other_ntconnected_host_and_count

inputs = {
    "vc_api_key" : 'xxx',
    'old_version' : 'False',
    'vc' : 'xxx-vc07.xxx.com',
    'esxi_host' : 'xxx-r02esx34.xxx.com',
    'host_id' : 'host-1031'
}

def handler(inputs):
  vc_api_key = inputs["vc_api_key"]
  old_version = inputs["old_version"]
  vc = inputs["vc"]
  esxi_host = inputs["esxi_host"]
  host_id = inputs["host_id"]
  cluster_names = get_all_cluster(host_id, esxi_host, vc_api_key, old_version, vc)
  host_cluster = get_host_cluster_name(cluster_names, esxi_host,host_id, vc_api_key, old_version, vc)
  cluster_host_status = get_cluster_host_status(host_cluster, esxi_host,host_id, vc_api_key, old_version, vc)
  print(cluster_host_status)
  return cluster_host_status

handler(inputs)
