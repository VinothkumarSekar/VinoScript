import http.client

conn = http.client.HTTPSConnection("xxxx-grafana.xxxxxx.com")
payload = ''
headers = {
  'Authorization': 'Basic dmxxxxxx'
}
conn.request("GET", "/d/uSBPxIlZk/nimbus-running-vms?orgId=1&from=1692965759664&to=1693052159664&viewPanel=52", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))
