# -*- coding: utf-8 -*-
"""
Created on Fri Feb  5 11:27:02 2021

@author: matan
"""

s = """{'uuid': 'bx_BgHtJEeaLmBnMIaxRfg', 'id': '15046831', 'restaurant_id': 290029, 'menu_category_name': 'Appetizers', 'menu_category_id': '1081396', 'name': '3. Crispy Wrapped Shrimp', 'description': 'Crispy shrimp wrapped in rice paper. Served with Sriracha cream sauce.', 'price': {'amount': 695, 'currency': 'USD'}, 'delivery_price': {'amount': 695, 'currency': 'USD'}, 'pickup_price': {'amount': 695, 'currency': 'USD'}, 'tax': 8.25, 'tax_rate': {'name': 'RestaurantTax', 'rate': 8.25, 'included_in_item_price': False}, 'miscellaneous_taxes': [], 'minimum_cart_total': {'amount': 0, 'currency': 'USD'}, 'combinable_with_coupons': True, 'sequence': 3, 'minimum_price_variation': {'amount': 695, 'currency': 'USD'}, 'delivery_minimum_price_variation': {'amount': 695, 'currency': 'USD'}, 'pickup_minimum_price_variation': {'amount': 695, 'currency': 'USD'}, 'maximum_price_variation': {'amount': 695, 'currency': 'USD'}, 'delivery_maximum_price_variation': {'amount': 695, 'currency': 'USD'}, 'pickup_maximum_price_variation': {'amount': 695, 'currency': 'USD'}, 'available': True, 'choice_category_list': [], 'tag_list': [], 'media_image': {'base_url': 'https://media-cdn.grubhub.com/image/upload/', 'public_id': 'mkoykz3knmjni72ngttk', 'format': 'jpg', 'tag': 'food'}, 'dishes': ['seafood', 'shrimp'], 'allowable_order_types': ['standard', 'group'], 'menu_item_features': [], 'in_store_only': False, 'gh_pos_only': False, 'routing_tags': [], 'item_coupon': False, 'popular': False, 'deleted': False}"""

s = s.replace("'",'"')
s = s.replace('False','"FALSE"')
s = s.replace('True','"TRUE"')
print('\n',s)

