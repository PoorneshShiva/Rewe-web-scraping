import undetected_chromedriver
from bs4 import BeautifulSoup
import pandas as pd
import requests
import random
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By

# user_agents_list = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Avast/111.0.20716.147','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36 Edg/112.0.1722.34','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.62','Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/111.0']
#
#
#
#
# USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'
# # user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
# headers = {'Accept': 'text/html, image/avif, image/webp, image/apng, image/svg+xml,/;q=0.8',
# 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US, en;q=0.9','Connection': 'keep-alive',
# 'Upgrade-Insecure-Requests': '1',
# 'Sec-Fetch-Dest': 'document',
# 'Sec-Fetch-Mode': 'navigate',
# 'Sec-Fetch-User': '1',
# 'Sec-Fetch-Site': 'none',
#            'User-Agent':USER_AGENT
# }
# response = requests.get('https://shop.rewe.de/c/osterwelt/?source=homepage-category',headers=headers)
# print(response.status_code)
# soup = BeautifulSoup(response.content,'html.parser')
# print(soup.find_all('a', class_='home-page-category-tile'))
from product import GetProductDetails
import time
first_time = True
uc = Chrome()
uc.get('https://shop.rewe.de/')


if first_time:
    time.sleep(30)
    page = uc.page_source
    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find_all('a',class_='home-page-category-tile')
    for index, each in enumerate(data):
        print(data[index]['href'],'link')
        uc.get("https://shop.rewe.de" + data[index]['href'])
        soup2 = BeautifulSoup(uc.page_source,'html.parser')
        products = soup2.find_all('div',{"class":'search-service-product Product_product__maAwA'})
        for product_index, product in enumerate(products):
            uc.get('https://shop.rewe.de' + product.a['href'])

            time.sleep(5)
            product = GetProductDetails(uc.page_source)
            raw_data = product.store_to_csv()
            print(raw_data)
    # print(uc.page_source)


    # a = uc.find_elements(By.TAG_NAME,'a')


    # print(uc.find_elements(By.XPATH, '/html/body/div[3]/div/a[1]'))
    # uc.page_source
else:
    time.sleep(5)
