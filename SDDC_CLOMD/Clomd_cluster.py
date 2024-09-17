import requests
import base64
import ast
import json
import tempfile
import re
def vsan_cluster(cluster):

    if re.search("vSAN*", cluster):
        temp = cluster.split("(",1)
        vSAN_Cls= temp[1].split(")",1)
        vSAN_Cluster = vSAN_Cls[0]


        #print (vSAN_Cluster)
        return vSAN_Cluster

inputs = {
        'jsd_ticket' : 'xxx-168709',
        'cluster' : "vSAN Cluster(xxx-vc29c01)",
        'jira_credentials' : 'xxxx==',
        'idrac_credentials' : 'xxx=',
        'idrac_vendor' : 'DELL'
    }

   
def handler (inputs):

    cluster = inputs["cluster"]
    print (vsan_cluster(cluster))

handler (inputs)
