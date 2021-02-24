import requests
import json

f = open("Output1.txt", "r")
response_json = json.load(f)
restaurant = response_json['restaurant']
restaurant_availability = response_json['restaurant_availability']
restaurant_categories = response_json['restaurant']['menu_category_list']

r = requests.post(
    'https://api.staging.orderup.ai/merchant',
    headers={
        'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
    },
    #features={
     #     "orderEta": False
     #},
    json={
        "name": restaurant['name']+"_Testing",
        "menuOnly": 1,
        "contactTracing": restaurant_availability['contact_free_required'],
        "headerImg": restaurant['logo'],
        "paySettings": {
            "stripeAccount": "Null",
            "flatFee": True,
            "feeAmount": restaurant_availability['delivery_fee']['amount'],
            "taxRate": restaurant_availability['sales_tax'],
            "testMode": False,
            "countryCode": "CA",
            "currency": "usd"
        }, "features": {
            "orderEta": False
        }
    }
)

#--------------------------------------------------------------------

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
                temp_list1.append(k['min_choice_options'])
                # temp_list1.append(k['max_choice_options'])
                if('max_choice_options' in k):
                    temp_list1.append(k['max_choice_options'])
                else:
                    temp_list1.append(-1)
                if(temp_list1[2] == 0):
                    temp_list1.append(False)
                else:
                    temp_list1.append(True)
                item_counter = 0
                for l in k['choice_option_list']:
                    temp_list2 = []
                    # temp_list2.append(l['id'])
                    temp_list2.append(l['description'])
                    temp_list2.append(l['price']['amount'])
                    temp_list1.append(temp_list2)
                    item_counter += 1
                if temp_list1[3] == -1:
                    temp_list1[3] = item_counter
                modifier_list.append(temp_list1)
        if(len(temp_list3) > 0):
            temp_list.append(temp_list3)
            item_with_modifiers.append(temp_list)

#--------------------------------------------------------------------


print(r.headers['Location'])
location = r.headers['Location']
#location = '/merchant/29'

r = requests.post(
    'https://api.staging.orderup.ai{}/menu'.format(location),
    headers={
        'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
    },
    json={
        "name": restaurant['cuisines'][0],
        "startTime": restaurant_availability['available_hours'][0]['time_ranges'][0].split('-')[0],
        "endTime": restaurant_availability['available_hours'][0]['time_ranges'][-1].split('-')[-1]
    }
)
print(r.headers['Location'])
menuId = r.headers['Location'].split("/")[-1]
#print(menuId)
location = r.headers['Location']
merchantId = location.split("/")[2]
categoryIds = []
#categoryId = 0

categoryName_to_ID = {}
# CREATE CATEGORY
for i in restaurant_categories:
    r = requests.post(
        "https://api.staging.orderup.ai/merchant/" + merchantId + "/category",
        headers={
            'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
        },
        json={
            "_links": {
                "menu": [
                {
                    "href": location
                },
                ]
            },
            "name": i["name"],
            "position": 100,
            "description": "Only the best will do"
        }
    )
    print(r.headers["Location"])
    categoryIds.append(r.headers["Location"].split("/")[4]) # this puts all category ids into a list
    #categoryId = r.headers["Location"].split("/")[4] # this gets the last category id, will be used to test updating a category

#print(categoryIds)
print()
#UPDATE CATEGORY
'''r = requests.post(
        "https://api.orderup.ai/merchant/" + merchantId + "/category/" + categoryId,
        headers={
            'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
        },
        json={
            "_links": {
                "menu": [
                {
                    "href": location
                },
                ]
            },
            "name": "Test",
            "position": 100,
            "description": "updated category"
        }
    )
'''
#-------------------------------------------------------------------
url = "https://api.staging.orderup.ai/merchant/{}/modifier-group".format(merchantId)
#print(modifier_list)
for i in modifier_list:
    r = requests.post(
        url,
        json={
            "name": i[1],
            "description": "None",
            "required": i[4],
            "minRange": i[2],
            "maxRange": i[3]
        }
    )
    modifier_group_id = r.headers['Location']
    modifier_group_id = modifier_group_id[modifier_group_id.rfind('/') + 1:]
    modifier_url = "https://api.staging.orderup.ai/merchant/{}/modifier-group/{}/modifier".format(merchantId, modifier_group_id)
    for j in i[5:]:
        r = requests.post(
        modifier_url,
        json={
            "name": j[0],
            "price": j[1]
            }
        )
        modifier_item_id = r.headers['Location']
        modifier_item_id = modifier_item_id[modifier_item_id.rfind('/') + 1:]
        j.append(modifier_item_id)
        print("Modifier item id: " + modifier_item_id)
    i.append(modifier_group_id)
    print("Modifier group id: " + modifier_group_id + "\n")


itemID_to_modifiersID = {}
print('pass')


for i in item_with_modifiers:
    temp_list_4 = []
    #temp_list_4.append()
    itemID_to_modifiersID[i[0]] = []
    for j in i[2]:
        for k in modifier_list:
            if (j == k[0]):
                itemID_to_modifiersID[i[0]].append(k[-1])
                break

#print(itemID_to_modifiersID)


#-------------------------------------------------------------------
# creating items
catregoty_idx = 0
for menu in response_json['restaurant']['menu_category_list']:
    print(menu['name'])
    #print(r['menu_item_list'],'\n')
    for item in menu['menu_item_list']:
        name = item['name']
        id = item['id']

        if name[0].isdigit() or name[1].isdigit(): # removing numbers before
            name = ' '.join(name.split()[1:])

        #print(name + '(' +id + '):')
        #print(item)


        bill = itemID_to_modifiersID[str(id)] if str(id) in itemID_to_modifiersID else []
        ryan = [menuId] # menus
        category = [{"href": "/merchant/" + str(merchantId) + '/category/' + str(categoryIds[catregoty_idx])}]
        menu = [{"href": "/merchant/" + str(merchantId) +'/menu/'+str(m)} for m in ryan]
        modifierGroup = [{"href": "/merchant/" + str(merchantId) +'/modifier-group/'+str(m)} for m in bill]

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
        #print(item_json)
        #print('\n\n')

        r = requests.post(
            "https://api.staging.orderup.ai/merchant/" + merchantId + "/item",
            headers={
                'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
            },
            json = item_json
        )
        print(r.headers["Location"],": {}".format(name))

    catregoty_idx += 1
#-------------------------------------------------------------------

#print(itemID_to_modifiersID)
#print(r.headers)
