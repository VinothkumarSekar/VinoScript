import requests
import json
url = "https://vrop-xxxx.com/suite-api/api/auth/token/acquire"
payload = json.dumps({
  "username": "admin",
  "password": "xxxx"
})
headers = {
  'Content-Type': 'application/json'
}
response = requests.request("POST", url, headers=headers, data=payload)
print(response.text)
