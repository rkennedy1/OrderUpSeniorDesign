import requests
import json
import sys

def create_data(restaurant_id):
    try:
        r = requests.post(
            'https://stevesie.com/cloud/api/v1/endpoints/92e9a78f-8e40-46c1-bc5c-f3b37ecb33de/executions',
            headers={
                'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
            },
            json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json" })

        response_json = r.json()
        response_json = response_json['object']['response']['response_json']

        r = requests.post(
            'https://stevesie.com/cloud/api/v1/endpoints/e35c15d5-0ff5-4d8d-bc16-7da5f22ff866/executions',
            headers={
                'Token': 'b90ea26c-cd3e-4a26-be92-5f235d4b1dbc',
            },
            json={ "proxy": { "type": "shared", "location": "nyc" }, "format": "json", "inputs": { "restaurant_id": restaurant_id, "auth_token": response_json["session_handle"]["access_token"] } })
            # 1684504 - Yardbird
            # 2124365 - Chipotle
            # 290029 - Thai Thai

        response_json = r.json()
        return response_json['object']['response']['response_json']
    except:
        print("Stevesie API has returned an error\nPlease try again in a few seconds\n")


class Requests:
    def __init__(self,response_json):

        self.response_json = response_json
        self.restaurant = response_json['restaurant']
        self.restaurant_availability = response_json['restaurant_availability']
        self.restaurant_categories = response_json['restaurant']['menu_category_list']

        self.modifier_list = []
        self.exist_list = []
        self.item_with_modifiers = []
        self.categoryIds = []

        self.itemID_to_modifiersID = {}

    def create_marchent(self):

        self.r = requests.post(
            'https://api.staging.orderup.ai/merchant',
            headers={
                'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
            },
            #features={
             #     "orderEta": False
             #},
            json={
                "name": self.restaurant['name']+"_Testing",
                "menuOnly": 1,
                "contactTracing": self.restaurant_availability['contact_free_required'],
                "headerImg": self.restaurant['logo'],
                "paySettings": {
                    "stripeAccount": "Null",
                    "flatFee": True,
                    "feeAmount": self.restaurant_availability['delivery_fee']['amount'],
                    "taxRate": self.restaurant_availability['sales_tax'],
                    "testMode": False,
                    "countryCode": "CA",
                    "currency": "usd"
                }, "features": {
                    "orderEta": False
                }
            }
        )



    def set_modifiers_lists(self):

        for i in self.response_json['restaurant']['menu_category_list']:
            for j in i['menu_item_list']:
                temp_list = []
                temp_list3 = []
                temp_list.append(j['id'])
                temp_list.append(j['name'])
                for k in j['choice_category_list']:
                    temp_list1 = []
                    temp_list3.append(k['id'])
                    if((k['id'] in self.exist_list) == False):
                        self.exist_list.append(k['id'])
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
                        self.modifier_list.append(temp_list1)
                if(len(temp_list3) > 0):
                    temp_list.append(temp_list3)
                    self.item_with_modifiers.append(temp_list)



    def create_menu(self):

        location = self.r.headers['Location']
        #location = '/merchant/29'

        r = requests.post(
            'https://api.staging.orderup.ai{}/menu'.format(location),
            headers={
                'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
            },
            json={
                "name": self.restaurant['cuisines'][0],
                "startTime": self.restaurant_availability['available_hours'][0]['time_ranges'][0].split('-')[0],
                "endTime": self.restaurant_availability['available_hours'][0]['time_ranges'][-1].split('-')[-1]
            }
        )
        print(r.headers['Location'])
        self.menuId = r.headers['Location'].split("/")[-1]
        print(self.menuId)
        self.location = r.headers['Location']
        self.merchantId = self.location.split("/")[2]


    def create_category(self):

        # CREATE CATEGORY
        for i in self.restaurant_categories:
            r = requests.post(
                "https://api.staging.orderup.ai/merchant/" + self.merchantId + "/category",
                headers={
                    'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
                },
                json={
                    "_links": {
                        "menu": [
                        {
                            "href": self.location
                        },
                        ]
                    },
                    "name": i["name"],
                    "position": 100,
                    "description": "Only the best will do"
                }
            )
            print(r.headers["Location"])
            self.categoryIds.append(r.headers["Location"].split("/")[4]) # this puts all category ids into a list
            #categoryId = r.headers["Location"].split("/")[4] # this gets the last category id, will be used to test updating a category

        print(self.categoryIds)




    def create_modifiers(self):
        url = "https://api.staging.orderup.ai/merchant/{}/modifier-group".format(self.merchantId)

        for i in self.modifier_list:
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
            modifier_url = "https://api.staging.orderup.ai/merchant/{}/modifier-group/{}/modifier".format(self.merchantId, modifier_group_id)
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


        self.itemID_to_modifiersID = {}
        print('pass')

        # setting map items id to modifier group
        for i in self.item_with_modifiers:
            self.itemID_to_modifiersID[i[0]] = []
            for j in i[2]:
                for k in self.modifier_list:
                    if (j == k[0]):
                        self.itemID_to_modifiersID[i[0]].append(k[-1])
                        break



    def create_items(self):
        catregoty_idx = 0
        for menu in self.response_json['restaurant']['menu_category_list']:
            print(menu['name'])
            #print(r['menu_item_list'],'\n')
            for item in menu['menu_item_list']:
                name = item['name']
                id = item['id']
                if name[0].isdigit() or name[1].isdigit(): # removing numbers before
                    name = ' '.join(name.split()[1:])
                #print(name + '(' +id + '):')
                #print(item)

                bill = self.itemID_to_modifiersID[str(id)] if str(id) in self.itemID_to_modifiersID else []
                ryan = [self.menuId] # menus
                category = [{"href": "/merchant/" + str(self.merchantId) + '/category/' + str(self.categoryIds[catregoty_idx])}]
                menu = [{"href": "/merchant/" + str(self.merchantId) +'/menu/'+str(m)} for m in ryan]
                modifierGroup = [{"href": "/merchant/" + str(self.merchantId) +'/modifier-group/'+str(m)} for m in bill]
                item_json = {

                        "_links":{
                                "category" : category,
                                "menu": menu,
                                "modifier-group":modifierGroup
                                },
                        "name":name,
                        "price":item['price']['amount'],
                        "description": item['description']
                        }
                #print(item_json)
                #print('\n\n')
                r = requests.post(
                    "https://api.staging.orderup.ai/merchant/" + self.merchantId + "/item",
                    headers={
                        'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
                    },
                    json = item_json
                )
                print(r.headers["Location"], ": ", name)

            catregoty_idx += 1
#-------------------------------------------------------------------
# 1684504 - Yardbird
# 290029 - Thai Thai

if __name__ == "__main__":
    if (len(sys.argv) > 1):
        menu_id = sys.argv[1]
    else:
        menu_id = 290029
    f = create_data(menu_id)
    r = Requests(f)
    r.create_marchent()
    r.set_modifiers_lists()
    r.create_menu()
    r.create_category()
    r.create_modifiers()
    r.create_items()
