import time
import os
from bs4 import BeautifulSoup
from datetime import datetime
from selenium.webdriver.common.by import By
import requests
from selenium import webdriver
# import chromedriver_autoinstaller
import undetected_chromedriver as uc
import csv
from product import GetProductDetails

product = []
product_details = {}

# chromedriver_autoinstaller.install()
driver = uc.Chrome(executable_path="chromedriver.exe")

# with open(f'Meat & Fish/index1.html', encoding='utf-8') as f:
#     html = f.read()
#     soup = BeautifulSoup(html, 'html.parser')
#     element = soup.find_all('div', class_='search-service-productDetailsWrapper')[1]

current_path = os.getcwd()


all_dir = os.listdir(current_path)
first_time = True
for each in all_dir:
    if '.' not in each and '_' not in each and each != 'CSV':
        category = current_path + f'\{each}'
        files = os.listdir(category)
        # print(f"{each}/index1.html")

        # print(files)
        for file in files:
            print(f'{each}/{file}')

            with open(f'{each}/{file}', encoding='utf-8') as f:
                html = f.read()
            soup = BeautifulSoup(html, 'html.parser')

            element = soup.find_all('div', class_='search-service-productDetailsWrapper')
            # item_url = (element[0].find('a',class_="search-service-productDetailsLink Product_productDetailsLink__hXXfb")['href'])
            # base_url = f'https://shop.rewe.de{item_url}'
            # print(base_url)


            for e in element:
                try:
                    product_name = (e.a.find('div', class_='LinesEllipsis')).text
                except:
                    product_name = ''

                try:
                    product_price = (e.a.find('div',
                                              class_='search-service-productPrice ProductPriceDisplay_productPrice__pqWxK').text)
                except:
                    product_price = ''

                try:
                    product_quantity = (e.a.find('div',
                                                 class_='ProductGrammage_productGrammage__fMOJr search-service-productGrammage').text)
                except:
                    product_quantity = ''
                product_details = {
                    'name': product_name,
                    'price': product_price,
                    'quantity': product_quantity,
                }
                try:
                    item_url = (
                        e.find('a', class_="search-service-productDetailsLink Product_productDetailsLink__hXXfb")[
                            'href'])


                except:
                    item_url = ''

                base_url = f'https://shop.rewe.de{item_url}'

                try:
                    img_url = (e.div.find('div',
                                          class_='search-service-rsProductsMedia ProductMedia_rsProductsMedia__TgDb_').img[
                        'src'])

                except:
                    img_url = ''

                driver.get(base_url)
                if first_time:
                    time.sleep(30)
                    first_time = False
                else:
                    time.sleep(5)
                data = driver.page_source


                product_module = GetProductDetails(data)
                has_labels = product_module.has_labels
                row_data = product_module.store_to_csv()

                # try:
                #     brand = soup2.find('span', class_='art-Truncate__Children').text
                # except:
                #     brand = ''
                # print(brand)

                with open(f'CSV/{each}.csv', 'a', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    if file == "index1.html":

                        writer.writerow(['product_id', 'product_name', 'price', 'quantity', 'brand', 'image_url',
                                         'product_url', 'category', 'sub_category', 'product_type', 'location', 'offer',
                                         'offer_duration', 'date', 'country_of_origin',
                                         'information', 'instructions', 'contact_name', 'contact_address',
                                         'ingredients', 'features', 'energy_with_kj', 'energy_with_kcal',
                                         'fat', 'fat_including_saturated_fatty_acids', 'carbohydrates',
                                         'carbohydrates_thereof_sugar', 'protein', 'salt'])
                        print(row_data)
                        writer.writerow(row_data)
                        is_first_row = False

                    else:

                        # print([product_name, product_price, product_quantity, base_url,date])
                        print(row_data)
                        writer.writerow(row_data)
                    product.append(product_details)

print(len(product))

# with open ('fruits&vegetables_rewa.csv', 'a', newline='',encoding='utf-8') as file:
#     writer = csv.writer(file)
#
#     if is_first_row:
#         writer.writerow(['name','price','quantity'])
#         is_first_row = False
#     else:
#         print([product_name,product_price,product_quantity])
#         writer.writerow([product_name,product_price,product_quantity])
# product.append(product_details)
#
#         with open(f'CSV/{each}.csv', 'a', encoding='utf-8') as file:
#             writer = csv.writer(file)
#
#             if is_first_row:
#                 writer.writerow(['name', 'price', 'quantity', 'product_url','img_url', 'date'])
#                 is_first_row = False
#             else:
#                 date = datetime.now()
#                 # print([product_name, product_price, product_quantity, base_url,date])
#                 writer.writerow([product_name, product_price, product_quantity, base_url,img_url, date])
#             product.append(product_details)
# print(files)
# item_url = (element.find_all('a',class_='search-service-productDetailsLink Product_productDetailsLink__hXXfb')['href'])
# base_url = f'https://shop.rewe.de{item_url}'
# print(base_url)
# response2 = requests.get(base_url)
# soup2 = BeautifulSoup(response2.content,'html.parser')
# print(response2.status_code)

# print(base_url)
# product_name = (element.a.find('div', class_='LinesEllipsis')).text
# product_price = (element.a.find('div', class_='search-service-productPrice ProductPriceDisplay_productPrice__pqWxK')).text
# print(product_price,product_name)
# response = requests.get('https://shop.rewe.de'+element.a['href'])
# print(response.status_code)
# soup2 = BeautifulSoup(response.content, 'html.parser')
# print(soup2.find_all('div', class_='pdpr-TabCordionItem__Content'))

#
#     driver.get('https://shop.rewe.de'+element.a['href'])
#     time.sleep(5)
#     driver.find_elements(By.CLASS_NAME,'pdpr-TabCordionItem__Content')
# websites_link = {
#     'Bread,cereals & Spreads':'https://shop.rewe.de/c/brot-cerealien-aufstriche/?source=homepage-category/?objectsPerPage=80',
#     'Cooking&Baking':'https://shop.rewe.de/c/kochen-backen/?source=homepage-category/?objectsPerPage=80',
#     'Oils& sauces & spices':'https://shop.rewe.de/c/oele-sossen-gewuerze/?source=homepage-category/?objectsPerPage=80',
#     'Ready meals & canned food':'https://shop.rewe.de/c/fertiggerichte-konserven/?source=homepage-category/?objectsPerPage=80',
#     'Sweet & Salty':'https://shop.rewe.de/c/suesses-salziges/?icid=suess-salzig_shop-rewe-de_int_shop%20shop-rewe-de:c:suesses-salziges_nn_nn_nn_nn_&source=homepage-category/?objectsPerPage=80',
#     'Coffee, tea & cocoa':'https://shop.rewe.de/c/kaffee-tee-kakao/?source=homepage-category/?objectsPerPage=80',
#     'Beverages & Luxury Foods':'https://shop.rewe.de/c/getraenke-genussmittel/?source=homepage-category/?objectsPerPage=80',
#     'Drugstore & Cosmetics':'https://shop.rewe.de/c/drogerie-kosmetik/?source=homepage-category/?objectsPerPage=80',
#
#     'Baby supplies':'https://shop.rewe.de/c/babybedarf/?source=homepage-category/?objectsPerPage=80',
#     'Pet supplies':'https://shop.rewe.de/c/tierbedarf//?objectsPerPage=80',
#     'Kitchen & Household':'https://shop.rewe.de/c/kueche-haushalt/?source=homepage-category/?objectsPerPage=80',
#     'Vegan diversity':'https://shop.rewe.de/c/vegane-vielfalt/?source=homepage-category/?objectsPerPage=80',
#
# }
