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
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json", "inputs": { "restaurant_id": "290029", "auth_token": response_json["session_handle"]["access_token"] } })
    # 1684504 - Wendys
    # 2124365 - Chipotle

response_json = r.json()
response_json = response_json['object']['response']['response_json']

   
print('\n\nmenu_category_list')

# parallel lists
list_of_json = []
merchantId_list = [] 

for r in response_json['restaurant']['menu_category_list']:
    #print(r)
    
    #print(r['menu_item_list']['choice_category_list'],'\n\n\n\n\n')
    for k in r['menu_item_list']:
        #print(k['choice_category_list'],'\n\n\n\n\n')
        modifiers = k['choice_category_list']
        cur = { "_links": {
                        'category': [
                                {
                    	    		"href": "/merchant/9/category/" + k['menu_category_id']
                    	    	}
                                ],
                        'menu': [
                                {
                    	    		"href": "/merchant/9/menu/13" # need to change
                    	    	}
                                ],
                        'modifierGroup': [
                                {"href": "/merchant/9/modifier-group/1" + m['name']} for m in modifiers
                                ]
                },
    
                "name": k['name'],
                "price": k['price']['amount'],
                "description": k['description']
                }
        list_of_json.append(cur)
        merchantId_list.append(k['restaurant_id'])
    

run = False
if run:
    for i in range(len(list_of_json)):
        r = requests.post(
            'https://api.orderup.ai/merchant/:'+ merchantId_list[i] +'/item',
            json = list_of_json[i]
            )

print_en = True
if print_en:
    for j in list_of_json:
        print(j,'\n\n')
    

