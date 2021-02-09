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
    json={
        "name": restaurant['name']+"_Testing",
        "menuOnly": 1,
        "contactTracing": restaurant_availability['contact_free_required'],
        "headerImg": restaurant['logo'],
        "paySettings": {
            "stripeAccount": "acct_1HSTyMHluWM5pjM5",
            "flatFee": True,
            "feeAmount": restaurant_availability['delivery_fee']['amount'],
            "taxRate": restaurant_availability['sales_tax'],
            "testMode": False,
            "countryCode": "CA",
            "currency": "usd"
        }
    }
)

print(r.headers['Location'])
location = r.headers['Location']

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
location = r.headers['Location']
merchantId = location.split("/")[2]
# categoryIds = []
categoryId = 0

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
    # categoryIds.append(r.headers["Location"].split("/")[4]) # this puts all category ids into a list
    categoryId = r.headers["Location"].split("/")[4] # this gets the last category id, will be used to test updating a category

#UPDATE CATEGORY
r = requests.post(
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
print(r.headers)

