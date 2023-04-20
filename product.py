from bs4 import BeautifulSoup
from datetime import datetime


class GetProductDetails:
    def __init__(self, page_source):
        self.offer = None
        self.offer_duration = None
        self.date = None
        self.features = None
        self.has_labels = False
        self.product_id = None
        self.image_url = None
        self.quantity = None
        self.product_url = None
        self.price = None
        self.brand = None
        self.product_name = None
        self.labels = None
        self.instructions = None
        self.ingredients = None
        self.country_of_origin = None
        self.contact_address = None
        self.contact_name = None
        self.offer_duration = None
        self.response = page_source
        self.category = None
        self.sub_category = None
        self.product_type = None
        self.soup = BeautifulSoup(self.response, 'html.parser')
        self.label_texts = []
        self.energy_with_kj = None
        self.energy_with_kcal = None
        self.information = None
        self.fat_including_saturated_fatty_acids = None
        self.carbohydrates = None
        self.fat = None
        self.salt = None
        self.protein = None
        self.location = None
        self.carbohydrates_thereof_sugar = None
        self.get_category()
        self.get_tab_labels()
        self.get_product_info()

    def get_category(self):
        breadcrumbs = self.soup.find_all('a', class_='lr-breadcrumbs__link')
        for index, each in breadcrumbs:
            if index == 0:
                self.category = each.text
            elif index == 1:
                self.sub_category = each.text
            elif index == 2:
                self.product_type = each.text

        # self.item = self.soup.find_all('a', class_='lr-breadcrumbs__link')[2].text

    def store_to_csv(self):

        return [self.product_id, self.product_name, self.price, self.quantity, self.brand, self.image_url,
                self.product_url, self.category, self.sub_category, self.product_type, self.location, self.offer,
                self.offer_duration, self.date, self.country_of_origin,
                self.information, self.instructions, self.contact_name, self.contact_address,
                self.ingredients, self.features, self.energy_with_kj, self.energy_with_kcal,
                self.fat, self.fat_including_saturated_fatty_acids, self.carbohydrates,
                self.carbohydrates_thereof_sugar, self.protein, self.salt]

    def get_tab_labels(self):
        try:
            self.labels = self.soup.find_all('label', class_='pdpr-TabCordionItem__Label')
        except:
            self.labels = ''
            self.has_labels = False
        else:
            self.has_labels = True
            for index, each in enumerate(self.labels):
                self.label_texts.append(each.text)
            self.get_tab_values()
            return self.label_texts

    def get_product_info(self):
        self.product_name = self.soup.find('h1', class_='pdpr-Title')
        if self.product_name:

            self.product_name = self.soup.find('h1', class_='pdpr-Title').text
        else:
            self.product_name = None

        self.brand = self.soup.find('span', class_='art-Truncate__Children')
        if self.brand:

            self.brand = self.soup.find('span', class_='art-Truncate__Children').text
        else:
            self.brand = None

        self.price = self.soup.find('div', class_='pdpr-Price pdpr-Price--Details')
        if self.price:

            self.price = self.soup.find('div', class_='pdpr-Price pdpr-Price--Details').text
        else:
            self.price = None

        self.quantity = self.soup.find('div', class_='rs-qa-price-base pdsr-Grammage')
        if self.quantity:

            self.quantity = self.soup.find('div', class_='rs-qa-price-base pdsr-Grammage').text
        else:
            self.quantity = None

        self.image_url = self.soup.find('div', class_='pdsr-ResponsiveImage')
        if self.image_url:

            self.image_url = self.soup.find('div', class_='pdsr-ResponsiveImage').picture.find('img')['src']
        else:
            self.image_url = None

        self.product_url = self.soup.find('link', {'rel': 'canonical'})
        if self.product_url:

            self.product_url = self.soup.find('link', {'rel': 'canonical'})['href']
        else:
            self.product_url = None

        self.product_id = self.soup.find('div', class_='pdpr-ArticleNumber')
        if self.product_id:

            self.product_id = self.soup.find('div', class_='pdpr-ArticleNumber').text.split(' ')[1]
        else:
            self.product_id = None

        self.location = self.soup.find('span',
                                       class_='gbmc-header-link__text gbmc-customer-zipcode-qa rs-qa-customer-zip')
        if self.location:
            self.location = self.soup.find('span',
                                           class_='gbmc-header-link__text gbmc-customer-zipcode-qa rs-qa-customer-zip').text
        else:
            self.location = None

        self.offer_duration = self.soup.find('div', class_='pdpr-Price__DiscountValidTo')

        if self.offer_duration:
            self.offer = True
            self.offer_duration = self.offer_duration.text
        else:
            self.offer = False
            self.offer_duration = None

        self.date = datetime.now()

    def get_tab_values(self):
        table_keys = []
        table_values = []
        if 'Zutaten & Allergene' in self.label_texts:
            index_of_label = (self.label_texts.index('Zutaten & Allergene'))
            for each in self.soup.find_all('div', class_='pdpr-TabCordionItem__Content')[index_of_label].children:
                tab_contents = each.find_all('div', class_='pdpr-Attribute')
                for tab_content in tab_contents:
                    # print(tab_content.h3.text)
                    if tab_content.h3.text == "Zutaten: ":
                        self.ingredients = tab_content.text.replace('Zutaten: ', '')
                    elif tab_content.h3.text == "Allergenhinweise: ":
                        self.information = tab_content.text.replace('Allergenhinweise: ', '')
        if 'Hinweise' in self.label_texts:
            index_of_label = (self.label_texts.index('Hinweise'))
            for each in self.soup.find_all('div', class_='pdpr-TabCordionItem__Content')[index_of_label].children:
                tab_contents = each.find_all('div', class_='pdpr-Attribute')
                for tab_content in tab_contents:
                    # print(tab_content.h3.text)

                    self.instructions = tab_content.text

                    # print(each.find_all('div', class_= 'pdpr-Attribute')[1].text)
        item_details = []
        if 'Artikeldetails' in self.label_texts:
            index_of_label = (self.label_texts.index('Artikeldetails'))
            for each in self.soup.find_all('div', class_='pdpr-TabCordionItem__Content')[index_of_label].children:
                tab_contents = each.find_all('div', class_='pdpr-Attribute')
                for tab_content in tab_contents:
                    # print(tab_content.h3.text)
                    if 'Ursprungsland:' in tab_content.text:
                        self.country_of_origin = tab_content.text.replace('Ursprungsland:', '')

                    elif 'Eigenschaften' in tab_content.text:
                        self.features = tab_content.text.replace('Eigenschaften:', '')

        if 'Kontakt' in self.label_texts:
            index_of_label = (self.label_texts.index('Kontakt'))
            for each in self.soup.find_all('div', class_='pdpr-TabCordionItem__Content')[index_of_label].children:
                tab_contents = each.find_all('div', class_='pdpr-Attribute')
                for tab_content in tab_contents:
                    # print(tab_content.h3.text)
                    if 'Kontaktname:' in tab_content.text:
                        self.contact_name = tab_content.text.replace('Kontaktname:', '')
                    elif 'Kontaktadresse' in tab_content.text:
                        self.contact_address = tab_content.text.replace('Kontaktadresse:', '')

        if 'Nährwerte' in self.label_texts:
            index_of_label = (self.label_texts.index('Nährwerte'))

            for each in self.soup.find_all('div', class_='pdpr-TabCordionItem__Content')[index_of_label].children:
                try:
                    table_keys = each('tr', class_='pdsr-Table--Row')[index_of_label].find_all_next('td')
                except:
                    pass
                else:
                    if len(table_keys) > 1:
                        table_keys = each('tr', class_='pdsr-Table--Row')[index_of_label].find_all_next('td')[::2]

                        table_values = each('tr', class_='pdsr-Table--Row')[index_of_label].find_all_next('td')[1::2]

                        for table_index, table_key in enumerate(table_keys):
                            if table_key.text == 'Energie' and table_index == 0:
                                self.energy_with_kj = table_values[table_index].text

                            elif table_key.text == 'Energie' and table_index == 1:
                                self.energy_with_kcal = table_values[table_index].text

                            elif table_key.text == "Fett":
                                self.fat = table_values[table_index].text

                            elif table_key.text == "Fett, davon gesättigte Fettsäuren":
                                self.fat_including_saturated_fatty_acids = table_values[table_index].text

                            elif table_key.text == "Kohlenhydrate":
                                self.carbohydrates = table_values[table_index].text

                            elif table_key.text == "Kohlenhydrate, davon Zucker":
                                self.carbohydrates_thereof_sugar = table_values[table_index].text

                            elif table_key.text == "Salz":
                                self.salt = table_values[table_index].text

                            elif table_key.text == "Eiweiß":
                                self.protein = table_values[table_index].text

# print(soup.find_all('div',class_='pdpr-AttributeGroup')[0].find_all_next(class_='pdpr-Attribute'))
# Item number
# print(soup.find('div',class_='pdpr-ArticleNumber').text.split(' ')[1])
# print(soup.find('div',class_='pdpr-Attribute').text.split(':')[1])
# print(''.join(soup.find_all('div',class_='pdpr-Attribute')[1].text.split(':')[1:]))
#
#
# print(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[::2])
# print(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[1::2])

# print(len(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[::2]))
# print(len(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[1::2]))


#  Even will be Name
# print(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[0].text)
# Odd one will be Value
# print(soup.find_all('tr',class_='pdsr-Table--Row')[1].find_all_next('td')[1].text)
# print(soup.find('div',class_='lr-breadcrumbs').a.text)


# print(soup.find_all('div',class_='pdpr-AttributeGroup')[0].find_all_next(class_='pdpr-Attribute'))
