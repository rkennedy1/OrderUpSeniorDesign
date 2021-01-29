
import requests

r = requests.post(
    'https://api.staging.orderup.ai/merchant',
    headers={
        'Authorization': 'Bearer hMLsrTVzDwDgea3D0Ghl0Rh51ytlDmUYNK8Fj1MD3GQ',
    },
    json={
        "name": "Pukka",
        "menuOnly": 1,
        "contactTracing": True,
        "headerImg": "url.to.img",
        "paySettings": {
            "stripeAccount": "acct_1HSTyMHluWM5pjM5",
            "flatFee": True,
            "feeAmount": 53,
            "taxRate": 13.00,
            "countryCode": "CA",
            "currency": "usd"
        }
    }
)

response_json = r.json()
print(response_json)
