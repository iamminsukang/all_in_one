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
url = 'https://www.coupang.com/'


# 카테고리 scaraping 함수
def ctgr_scrap(url, headers):
    # 최초 db collection 초기화
    db.coupang_ctgr.drop()

    # 최초 Request
    data = requests.get(url=url,
                        headers=headers)
    soup = BeautifulSoup(data.text, 'html.parser')

    #### list elements 추출
    menu_list = soup.select('#gnbAnalytics > ul.menu.shopping-menu-list > li')
    ctgr_list = {
        'ctgr1_nm': [],
        'ctgr1_no': [],
        'ctgr2_nm': [],
        'ctgr2_no': [],
        'ctgr3_nm': [],
        'ctgr3_no': [],
        'ctgr4_nm': [],
        'ctgr4_no': [],
        'ctgr5_nm': [],
        'ctgr5_no': []
    }

    #### Lv 1~5 카테고리 정보 Scraping
    for i in range(len(menu_list)):

        ctgr1_nm = menu_list[i].select_one('a:nth-child(1)').text
        ctgr1_no = menu_list[i].select_one('a:nth-child(1)')['href'].split('/')[-1]

        if not (re.match(r'\d+', ctgr1_no)):
            ctgr1_no = None

        ctgr2_list = menu_list[i].select('li.second-depth-list')

        for j in range(len(ctgr2_list)):

            ctgr2_nm = ctgr2_list[j].select_one('a:nth-child(1)').text
            ctgr2_no = ctgr2_list[j].select_one('a:nth-child(1)')['href'].split('/')[-1]
            url_ctgr2 = 'https://www.coupang.com/np/categories/%s' % (ctgr2_no)

            res_ctgr2 = requests.get(url=url_ctgr2,
                                     headers=headers)
            soup_ctgr2 = BeautifulSoup(res_ctgr2.text, 'html.parser')
            ctgr3_list = soup_ctgr2.select('#searchCategoryComponent > ul > li')

            sleep(uniform(0, 1))

            for k in range(0, len(ctgr3_list)):
                ctgr3_nm = ctgr3_list[k].select_one('label').text
                ctgr3_no = ctgr3_list[k]['data-linkcode']
                ctgr4_comp_id = ctgr3_list[k]['data-component-id']
                try:
                    ctgr4_a = ctgr3_list[k].a
                except TypeError as e:
                    pass

                if ctgr4_a is None:
                    ctgr4_nm = None
                    ctgr4_no = None
                    ctgr5_nm = None
                    ctgr5_no = None

                    db.coupang_ctgr.insert_one({
                        'ctgr1_nm': ctgr1_nm,
                        'ctgr1_no': ctgr1_no,
                        'ctgr2_nm': ctgr2_nm,
                        'ctgr2_no': ctgr2_no,
                        'ctgr3_nm': ctgr3_nm,
                        'ctgr3_no': ctgr3_no,
                        'ctgr4_nm': ctgr4_nm,
                        'ctgr4_no': ctgr4_no,
                        'ctgr5_nm': ctgr5_nm,
                        'ctgr5_no': ctgr5_no,
                    })
                    print(ctgr1_nm, ctgr2_nm, ctgr3_nm, ctgr4_nm, ctgr5_nm)
                elif ctgr4_a is not None:
                    url_ctgr5 = 'http://www.coupang.com/np/search/getFirstSubCategory'
                    params_ctgr5 = {
                        'channel': '',
                        'component': ctgr4_comp_id,
                        'campaignId': '',
                        'priceRange': '',
                        'filterType': '',
                        'minPrice': '',
                        'maxPrice': '',
                        'sorter': '',
                        'listSize': 60,
                        'page': 1,
                        'filter': '',
                        'brand': '',
                        'offerCondition': '',
                        'rating': 0,
                        'isPriceRange': 'false',
                        'isEmptyByRocket': '',
                        'filterMode': 'PLP',
                        'fromComponent': 'N',
                        'filterKey': '',
                        'selectedPlpKeepFilter': ''
                    }
                    res_ctgr5 = requests.get(url=url_ctgr5,
                                             headers=headers,
                                             params=params_ctgr5)
                    soup_ctgr4 = BeautifulSoup(res_ctgr5.text, 'html.parser')
                    ctgr5_selector = 'ul#category%s.search-option-items-child > li.search-option-item' % (ctgr4_comp_id)
                    ctgr4_list = soup_ctgr4.select(ctgr5_selector)

                    sleep(uniform(0, 1))

                    for l in range(0, len(ctgr4_list)):
                        ctgr4_nm = ctgr4_list[l].select_one('label').text
                        ctgr4_no = ctgr4_list[l]['data-linkcode']
                        ctgr5_comp_id = ctgr4_list[l]['data-component-id']
                        try:
                            ctgr5_a = ctgr4_list[l].a
                        except TypeError as a:
                            pass

                        if ctgr5_a is None:
                            ctgr5_nm = None
                            ctgr5_no = None

                            db.coupang_ctgr.insert_one({
                                'ctgr1_nm': ctgr1_nm,
                                'ctgr1_no': ctgr1_no,
                                'ctgr2_nm': ctgr2_nm,
                                'ctgr2_no': ctgr2_no,
                                'ctgr3_nm': ctgr3_nm,
                                'ctgr3_no': ctgr3_no,
                                'ctgr4_nm': ctgr4_nm,
                                'ctgr4_no': ctgr4_no,
                                'ctgr5_nm': ctgr5_nm,
                                'ctgr5_no': ctgr5_no,
                            })
                            print(ctgr1_nm, ctgr2_nm, ctgr3_nm, ctgr4_nm, ctgr5_nm)
                        elif ctgr5_a is not None:
                            url_ctgr5 = 'http://www.coupang.com/np/search/getFirstSubCategory'
                            params_ctgr5 = {
                                'channel': '',
                                'component': ctgr5_comp_id,
                                'campaignId': '',
                                'priceRange': '',
                                'filterType': '',
                                'minPrice': '',
                                'maxPrice': '',
                                'sorter': '',
                                'listSize': 60,
                                'page': 1,
                                'filter': '',
                                'brand': '',
                                'offerCondition': '',
                                'rating': 0,
                                'isPriceRange': 'false',
                                'isEmptyByRocket': '',
                                'filterMode': 'PLP',
                                'fromComponent': 'N',
                                'filterKey': '',
                                'selectedPlpKeepFilter': ''
                            }
                            res_ctgr5 = requests.get(url=url_ctgr5,
                                                     headers=headers,
                                                     params=params_ctgr5)
                            soup_ctgr4 = BeautifulSoup(res_ctgr5.text, 'html.parser')
                            ctgr5_selector = 'ul#category%s.search-option-items-child > li.search-option-item' % (
                                ctgr5_comp_id)
                            ctgr5_list = soup_ctgr4.select(ctgr5_selector)

                            sleep(randint(0, 1))

                            for n in range(0, len(ctgr5_list)):
                                ctgr5_nm = ctgr5_list[n].select_one('label').text
                                ctgr5_no = ctgr5_list[n]['data-linkcode']

                                db.coupang_ctgr.insert_one({
                                    'ctgr1_nm': ctgr1_nm,
                                    'ctgr1_no': ctgr1_no,
                                    'ctgr2_nm': ctgr2_nm,
                                    'ctgr2_no': ctgr2_no,
                                    'ctgr3_nm': ctgr3_nm,
                                    'ctgr3_no': ctgr3_no,
                                    'ctgr4_nm': ctgr4_nm,
                                    'ctgr4_no': ctgr4_no,
                                    'ctgr5_nm': ctgr5_nm,
                                    'ctgr5_no': ctgr5_no,
                                })
                                print(ctgr1_nm, ctgr2_nm, ctgr3_nm, ctgr4_nm, ctgr5_nm)
    return ctgr_list

ctgr_scrap(url, headers)
# print(len(data['ctgr3_no']))
# if __name__ == '__main__':
#     ctgr_scrap()
