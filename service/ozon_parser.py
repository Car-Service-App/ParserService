import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs4, Tag
import json

from schema.car_part import CarPart


class CarPartScraper:
    def __init__(self, search):
        self.search = search
        self.url = f"https://www.ozon.ru/category/avtozapchasti-8678/?category_was_predicted=true&deny_category_prediction=true&from_global=true&&text={self.search}"
        self.cookies = list()
        self.firefox_options = FirefoxOptions()
        self.firefox_options.add_argument("-headless")
        self.driver = webdriver.Firefox(options=self.firefox_options)
        self.driver.get(self.url)

    def page_open(self, url):
        for cookie in self.cookies:
            self.driver.add_cookie(cookie)
        self.driver.get(url)
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "ozonTagManagerApp"))
            )
        finally:
            return self.driver.page_source

    def options_dictionary(self, options_list: list) -> dict:
        options_dict = {}
        for option in options_list:
            options_dict[option.split(':')[0].strip()] = option.split(':')[1].strip()
        return options_dict

    def images_dict(self, good_id: int, mask: str, soup) -> dict:
        images_dictionary = []
        try:
            data = soup.select_one(f'div[data-state*="{mask}"]')['data-state']
            json_data = json.loads(data)
            for link in json_data['items'][good_id]['tileImage']['items']:
                images_dictionary.append(link['image']['link'])
            return images_dictionary
        except:
            return []

    def func_parse(self, items, soup) -> []:
        car_parts = []
        idx = 0
        for sibling in items:
            car_part = CarPart()
            if isinstance(sibling, Tag) and sibling.text:
                item = {}
                bonuses = False
                if t := sibling.div.next_sibling.next_sibling.select_one('div span > span b'):
                    item['bonuses'] = t.text
                    bonuses = True
                item_name = sibling.div.next_sibling.next_sibling.div.a.text
                car_part.name = item_name
                img = sibling.div.a.div.div.img['src']
                car_part.image_link = img
                item_images = self.images_dict(idx, img.split('/')[-1], soup)
                if link := sibling.div.next_sibling.next_sibling.div.a['href']:
                    item['link'] = link
                car_part.link = f"https://www.ozon.ru{item['link']}"
                n_child = 3 if bonuses else 2
                if options := sibling.div.next_sibling.next_sibling.select_one(f'div > span:nth-child({n_child}) span'):
                    options_str = str(options)
                idx += 1
                if price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.div:
                    price_text = price.text[:-1].replace(' ', '')
                    item['price'] = int(price_text.encode('ascii', 'ignore'))
                elif price := sibling.div.next_sibling.next_sibling.next_sibling.next_sibling.div.span.span:
                    price_text = price.text[:-1].replace(' ', '')
                    item['price'] = int(price_text.encode('ascii', 'ignore'))
                car_part.last_price = item['price']
                car_parts.append(car_part)
        return car_parts

    def run(self) -> []:
        for page in range(1, 2):
            source_text = self.page_open(f'{self.url}&page={page}')
            result = re.sub(r'<!.*?->', '', source_text)
            soup = bs4(result, 'html.parser')
            items_body = soup.find('div', id='paginatorContent')
            items = items_body.div.div
            car_parts = self.func_parse(items=items, soup=soup)
            self.driver.quit()
            return car_parts

if __name__ == '__main__':
    search = 'toyota+corolla+e180+свечи'
    scraper = CarPartScraper(search)
    scraper.run()
