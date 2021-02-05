import requests
import json



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
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json", "inputs": { "restaurant_id": "290029", "auth_token": response_json["session_handle"]["access_token"] } })
    # 1684504 - Wendys
    # 2124365 - Chipotle
    # 290029 - Thai Thai

response_json = r.json()
response_json = response_json['object']['response']['response_json']


# modifier_list: modifier id + item + price
# item_with_modifiers: item + available modifiers' groupID
modifier_list = []
exist_list = []
item_with_modifiers = []

for i in response_json['restaurant']['menu_category_list']:
    for j in i['menu_item_list']:
        temp_list = []
        temp_list3 = []
        temp_list.append(j['id'])
        temp_list.append(j['name'])
        for k in j['choice_category_list']:
            temp_list1 = []
            temp_list3.append(k['id'])
            if((k['id'] in exist_list) == False):
                exist_list.append(k['id'])
                temp_list1.append(k['id'])
                temp_list1.append(k['name'])
                for l in k['choice_option_list']:
                    temp_list2 = []
                    temp_list2.append(l['id'])
                    temp_list2.append(l['description'])
                    temp_list2.append(l['price']['amount'])
                    temp_list1.append(temp_list2)
                modifier_list.append(temp_list1)
        if(len(temp_list3) > 0):
            temp_list.append(temp_list3)
            item_with_modifiers.append(temp_list)

print('modifier_list')
for i in modifier_list:
    print(i)      
    
print('item list')
for i in item_with_modifiers:
    print(i)