# coding:utf-8
import webbrowser
import requests
import json
import random
import pygeohash as pgh
import re

# 经度纬度，精确到小数点后五位
longitude = 123.37814
latitude = 41.79008
geohash = pgh.encode(latitude, longitude, precision=11)
# 通过offset参数来调整之前刷出了多少
# limit参数为返回商家数量，最多30
url = 'https://mainsite-restapi.ele.me/shopping/restaurants?extras[]=activities&geohash={0}&latitude={1}&limit=30&longitude={2}&offset=0&terminal=web'.format(geohash, latitude, longitude)
header = {
    'Host': 'mainsite-restapi.ele.me',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Referer': 'https://www.ele.me/place/{0}'.format(geohash),
    'origin': 'https://www.ele.me',
    'DNT': '1',
    'Connection': 'keep-alive'
}
request = requests.get(url, headers=header)
json_shop = request.text
data = json.loads(json_shop)
print(json_shop)
all_shop = []
# 把所有Json值储存到list里
for shop in data:
    print(shop)
    shop_inf = {}
    shop_inf['id'] = shop['id']
    if 'average_cost' in shop:
        shop_inf['average_cost'] = re.findall(r'(\w*[0-9]+)\w*', shop['average_cost'])[0]
    else:
        shop_inf['average_cost'] = 0
    shop_inf['distance'] = shop['distance']
    shop_inf['phone'] = shop['phone']
    shop_inf['float_delivery_fee'] = shop['float_delivery_fee']
    all_shop.append(shop_inf)

ran = random.choice(all_shop)
# 从所有商家中选出一家
print(ran)
price_ran = {
    '1-20': [],
    '21-50': [],
    '51-100': [],
    '100+': []
}
for i in all_shop:
    if 0 < int(i['average_cost']) <= 20:
        price_ran['1-20'].append(i)
    if 20 < int(i['average_cost']) <= 50:
        price_ran['21-50'].append(i)
    if 50 < int(i['average_cost']) <= 100:
        price_ran['51-100'].append(i)
    if 100 < int(i['average_cost']):
        price_ran['100+'].append(i)
# 随机选择一家平均消费1元~20元之间的饭店
ran = random.choice(price_ran['1-20'])
ran_url = 'https://www.ele.me/shop/' + str(ran['id'])
# 打开随机选出的店家网页
webbrowser.open(ran_url)






