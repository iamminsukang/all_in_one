from bs4 import BeautifulSoup
import requests
from random import randint, random, uniform
from time import sleep
import re
from pymongo import MongoClient

# MongoDB 클라이언트 연결
client = MongoClient('mongodb://localhost:27017/')
db = client.dbsparta

# Scraping Header 정보
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
}


def prd_scrap(ctgr_no):
    # db collection 초기화
    db.target_item.drop()

    url = 'https://www.coupang.com/np/categories/%s' % (ctgr_no)
    res = requests.get(url=url,
                       headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')

    prd_list = soup.select('ul#productList > li')
    for i in range(0, len(prd_list)):
        rank = i + 1
        product_id = prd_list[i].select_one('a')['data-product-id'].strip()
        item_id = prd_list[i].select_one('a')['data-item-id']
        vendoritem_id = prd_list[i].select_one('a')['data-vendor-item-id']
        item_nm = prd_list[i].select_one('a > dl > dd > div.name').text.strip()
        price = prd_list[i].select_one('div.price-area > div > div.price > em > strong').text.replace(',', '')
        dlv_dt = prd_list[i].select_one('div.delivery > span > em:nth-child(1)').text.strip() + ' ' + prd_list[i].select_one('div.delivery > span > em:nth-child(2)').text.strip()
        star = prd_list[i].select_one('div.other-info > div > span.star > em.rating').text
        review = re.findall(r'\d+', prd_list[i].select_one('div.other-info > div > span.rating-total-count').text)[0]
        img = prd_list[i].select_one('a > dl > dt > img')['src'].replace('230x230ex', '492x492ex')
        if prd_list[i].select_one('a')['data-is-rocket'] == 'true':
            rocket_yn = 1
        else:
            rocket_yn = 0

        db.target_item.insert_one({
            # 'depth': depth
            'ctgr_no': ctgr_no,
            'rank': int(rank),
            'product_id': product_id,
            'item_id': item_id,
            'vendoritem_id': vendoritem_id,
            'item_nm': item_nm,
            'price': int(price),
            'dlv_dt': dlv_dt,
            'star': float(star),
            'review': int(review),
            'img': img,
            'rocket_yn': rocket_yn
        })


# prd_scrap(114472)
