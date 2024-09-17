import http.client
import json

conn = http.client.HTTPSConnection("hooks.slack.com")
payload = json.dumps({
  "text": "<!vcc-cpe-sre> Post from webhook!!"
})
headers = {
  'Content-type': 'application/json'
}
conn.request("POST", "/services/T024JFTN4/B05KZ95JHJQ/e1ERTR9ZTvZQH3eqmrWZEoRX", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))

