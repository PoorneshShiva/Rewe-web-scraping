from bs4 import BeautifulSoup
from undetected_chromedriver import Chrome
from selenium.webdriver.common.by import By
from product import GetProductDetails
import time
import os
import csv

first_time = True
uc = Chrome()
uc.get('https://shop.rewe.de/')

time.sleep(20)
page = uc.page_source
soup = BeautifulSoup(page, 'html.parser')
data = soup.find_all('a', class_='home-page-category-tile')

for index, each in enumerate(data):
    category = (data[index]['href'].split('/')[2])
    uc.get("https://shop.rewe.de" + data[index]['href'])
    soup2 = BeautifulSoup(uc.page_source, 'html.parser')
    products = soup2.find_all('div', {"class": 'search-service-product Product_product__maAwA'})
    for product_index, product in enumerate(products):
        uc.get('https://shop.rewe.de' + product.a['href'])
        time.sleep(5)
        product = GetProductDetails(uc.page_source)
        row_data = product.store_to_csv()
        if not os.path.exists('CSV'):
            os.makedirs('CSV')

        else:
            pass


        with open(f'CSV/{category}.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            if first_time:
                writer.writerow(['product_id', 'product_name', 'price', 'quantity', 'brand', 'image_url',
                                 'product_url', 'category', 'sub_category', 'product_type', 'location', 'offer',
                                 'offer_duration', 'date', 'country_of_origin',
                                 'information', 'instructions', 'contact_name', 'contact_address',
                                 'ingredients', 'features', 'energy_with_kj', 'energy_with_kcal',
                                 'fat', 'fat_including_saturated_fatty_acids', 'carbohydrates',
                                 'carbohydrates_thereof_sugar', 'protein', 'salt'])
                print(row_data)
                writer.writerow(row_data)
                first_time = False
            else:
                print(row_data)
                writer.writerow(row_data)
