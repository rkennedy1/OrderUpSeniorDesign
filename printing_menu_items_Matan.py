import requests
import json


'''
This will print the menues and its items as a list
I am using the id 1453199, which is the one Chris sent us
'''

r = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/92e9a78f-8e40-46c1-bc5c-f3b37ecb33de/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json" })

response_json = r.json()
response_json = response_json['object']['response']['response_json']
#print("Auth:\n",response_json,'\n')

r = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/e35c15d5-0ff5-4d8d-bc16-7da5f22ff866/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json", "inputs": { "restaurant_id": "1453199", "auth_token": response_json["session_handle"]["access_token"] } })
    # 1684504 - Wendys
    # 2124365 - Chipotle

response_json = r.json()
response_json = response_json['object']['response']['response_json']
#print("Restau'rant:\n",respon'se_json,'\n')

with open('output1.txt', 'w') as outfile:
    json.dump(response_json, outfile)

'''for r in response_json:
    print('\n\n',r)
    for r2 in response_json[r]:
        print('   ',r2)'''
   
print('\n\nmenu_category_list')
for r in response_json['restaurant']['menu_category_list']:
    print(r['name'])
    #print(r['menu_item_list'],'\n')
    for k in r['menu_item_list']:
        print('   ',k['name'])
    print('\n')
    

'''print('\n\nmenu_item_features')
for r in response_json['restaurant']['menu_item_features']:
    print(r)'''


'''rr = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/dcd6049c-6354-49b9-abed-041939db3094/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json" ,"inputs": { "restaurant_id": "1453199", "auth_token": response_json["session_handle"]["access_token"] } })


response_json = r.json()
print(response_json['object']['response'])'''
'''for r in response_json['object']['response']['response_json']:
    print(r)'''
    
    

