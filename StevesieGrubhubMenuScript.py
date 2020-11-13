import requests
import json
from dataclasses import dataclass


r = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/92e9a78f-8e40-46c1-bc5c-f3b37ecb33de/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json" })

response_json = r.json()
response_json = response_json['object']['response']['response_json']
# print("Auth:\n",response_json,'\n')

r = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/e35c15d5-0ff5-4d8d-bc16-7da5f22ff866/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json", "inputs": { "restaurant_id": "290029", "auth_token": response_json["session_handle"]["access_token"] } })
    # 1684504 - Wendys
    # 2124365 - Chipotle
    # 290029 - Thai Thai

response_json = r.json()
response_json = response_json['object']['response']['response_json']
# print("Restaurant:\n",response_json,'\n')
with open('Full-output.txt', 'w') as outfile:
    json.dump(response_json, outfile)

@dataclass
class RestaurantInfo:
    name: ""
    tax_rate: float
    contactTracing: False
r1 = RestaurantInfo(response_json['restaurant']['name'], response_json['restaurant_availability']['sales_tax'], False)
print("Info: ", r1)

url = "https://api.staging.orderup.ai/merchant"

payload = "{{\n    \"name\": \"{0}\",\n    \"taxrate\": \"{1}\",\n    \"menuOnly\": \"1\",\n    \"contactTracing\": \"{2}\"\n}}".format(r1.name, r1.tax_rate, r1.contactTracing)
headers= {}
print(payload)
response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))
