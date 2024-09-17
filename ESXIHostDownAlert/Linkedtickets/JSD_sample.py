import json
import http.client
import ssl
import re

def get_vc_name(cluster,jsd_creds,jsd):
    headers = {"Accept": "application/json",
             "Authorization": f"Basic {jsd_creds}"
             }
    jsd_conn = http.client.HTTPSConnection(jsd, context=ssl._create_unverified_context())
    jsd_conn.request("GET", url=f"/rest/insight/1.0/iql/objects?objectSchemaId=1&iql=label={cluster}", headers=headers)
    jsd_conn_host_res = jsd_conn.getresponse()
    data_jsd_host_id_byte = jsd_conn_host_res.read()
    data = json.loads(data_jsd_host_id_byte.decode("utf-8"))["objectEntries"][0]["attributes"]

    for each_dict in data:
        try:
            cluster_vc = each_dict["objectAttributeValues"][0]['referencedObject']['label']
            vc_match = re.search(".*.xxx.com", cluster_vc)
            if vc_match:
                return cluster_vc
            

        except KeyError:
            pass
       




jsd_creds = "xxx"
cluster = "xxx-04-vc29c01"
jsd = "servicedesk.xxx.com"
print (get_vc_name(cluster,jsd_creds,jsd))
