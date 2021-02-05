import requests
import json


f = open("Output1.txt", "r")
response_json = json.load(f)
restaurant_availability = response_json['restaurant_availability']
restaurant = response_json['restaurant']

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

location = r.headers['Location']
print(r.headers['Location'])

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
