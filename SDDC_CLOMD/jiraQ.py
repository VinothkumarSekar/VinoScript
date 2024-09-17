import http.client
from urllib import parse
import ssl

inputs = {
    'jql': 'servicedesk.xxx.com',
    'servicedesk' : 'xxx-240158',
    "credentials": 'xxxx==',
    'fields': 'customfield_34601'
}

def handler(inputs):
    
    jql_encode = parse.quote(inputs['jql'])
    conn = http.client.HTTPSConnection(inputs['servicedesk'], context=ssl._create_unverified_context())
    payload = ''
    headers = {
    'Authorization': f'Basic {inputs["credentials"]}'
    }
    conn.request("GET", f"/rest/api/2/search?fields={inputs['fields']}&maxResults=1000&jql={jql_encode}", payload, headers)
    res = conn.getresponse()
    data = res.read()
    outputs = {
    "status": data.decode("utf-8")
    }
    print (outputs)
    return outputs

handler(inputs)
