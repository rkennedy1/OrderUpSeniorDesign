# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:09:26 2021

@author: matan
"""

import requests
import json

r = requests.post(
    'https://stevesie.com/cloud/api/v1/endpoints/92e9a78f-8e40-46c1-bc5c-f3b37ecb33de/executions',
    headers={
        'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
    },
    json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json" })

response_json = r.json()
#print(response_json)
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
#print(response_json)
response_json = response_json['object']['response']['response_json']
#print("Restau'rant:\n",respon'se_json,'\n')


print('\n\nitems:\n')
for menu in response_json['restaurant']['menu_category_list']:
    print(menu['name'])
    #print(r['menu_item_list'],'\n')
    for item in menu['menu_item_list']:
        name = item['name']
        id = item['id']
        
        if name[0].isdigit() or name[1].isdigit(): # removing numbers before
            name = ' '.join(name.split()[1:])
        
        print(name + '(' +id + '):')
        #print(item)
        

        merchant = 0
        kirby = [1] # category
        bill = [5] # itemID_to_modifiersID
        ryan = [6] # menus
        category = [{"href": "/merchant/" + str(merchant) + '/category/' + str(c)} for c in kirby] 
        menu = [{"href": "/merchant/" + str(merchant) +'/menu/'+str(m)} for m in ryan]
        modifierGroup = [{"href": "/merchant/" + str(merchant) +'/modifier-group/'+str(m)} for m in bill]
        
        item_json = {
                
                "_links":{
                        "category" : category,
                        "menu": menu,
                        "modifierGroup":modifierGroup
                        },
                "name":name,
                "price":item['price']['amount'],
                "description": item['description']
                
                }
        
        
        
        #print(cur_json)
        print(item_json)
        print('\n\n')

