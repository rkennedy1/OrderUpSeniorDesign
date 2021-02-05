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

with open('output1.txt', 'w') as outfile:
    json.dump(response_json, outfile)
   

exist_list = set()

print('\n\nitems:\n')
for menu in response_json['restaurant']['menu_category_list']:
    print(menu['name'])
    #print(r['menu_item_list'],'\n')
    for item in menu['menu_item_list']:
        name = item['name']
        print(name +':')
        #print(item)
        
        #cahgne for the real one according to Kirby/Ryan
        merchant = str(item['restaurant_id'])
        category = str(item['menu_category_id'])
        
        cur_json = '{"_links":{"category":[' # what is the category?!
        cur_json += '], "menu":[{'
        cur_json += '"href": "/merchant/' + merchant + '/category/' + category + '"}]' 
        
        #change according to Bill
        modi_group = str(item['choice_category_list'])
        
        cur_json += ', "modifierGroup":[{'
        if modi_group: cur_json += '"href": "/merchant/'+ merchant +'/modifier-group/'+modi_group+'"'
        cur_json += '}]},' # end links
    
        cur_json += '"name": "'+name+'",'
        cur_json += '"price": '+str(item['price']['amount'])+','
        cur_json += '"description": "'+item['description']+'"'

        cur_json +='}'
        
        print(cur_json)
        print('\n\n')

