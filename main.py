import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
import random
import csv


class AvitoParse:
    def __init__(self, url: str, items: list, count_page=5, version_main=None):
        self.url = url
        self.items = items
        self.count_page = count_page
        self.version_main = version_main
        self.driver = None

    def __setUp(self):
        self.driver = uc.Chrome(version_main=self.version_main)

    def __getUrl(self):
        self.driver.get(self.url)

    def __pg(self):
        while self.driver.find_element(By.CSS_SELECTOR,
                                       "[data-marker='pagination-button/nextPage']") and self.count_page > 0:
            self.__parsePage()
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker*='pagination-button/next']").click()
            self.count_page -= 1

    def __saveToCSV(self, data):
        with open('avito_data.csv', 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Name', 'Price', 'Description', 'Address', 'Seller', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            if csvfile.tell() == 0:
                writer.writeheader()
            writer.writerow(data)  # Просто записываем данные без проверки на дубликаты

    def __parsePage(self):
        items = self.driver.find_elements(By.CSS_SELECTOR, "[data-marker='item']")
        for i, data in enumerate(items):
            url = data.find_element(By.CSS_SELECTOR, "[data-marker='item-title']").get_attribute("href")
            name = data.find_element(By.CSS_SELECTOR, "[itemprop='name']").text
            price = data.find_element(By.CSS_SELECTOR, "[data-marker='item-price']").text
            # Проверяем наличие элемента с описанием
            try:
                description = data.find_element(By.CSS_SELECTOR, "[class*='item-description']").text
            except:
                description = "Нет описания"
            # Проверяем наличие элемента с адресом
            try:
                address = data.find_element(By.CSS_SELECTOR, "[data-marker='item-address']").text
            except:
                address = "Адрес не указан"
            # Проверяем наличие элемента с продавцом
            try:
                seller = data.find_element(By.CSS_SELECTOR, "[data-marker='seller-info/label']").text
            except:
                seller = "Нет информации о продавце"
            # Создаем словарь с данными для записи в CSV файл
            csv_data = {
                'Name': name,
                'Price': price,
                'Description': description,
                'Address': address,
                'Seller': seller,
                'URL': url
            }
            # Записываем данные в CSV файл
            self.__saveToCSV(csv_data)
            # Выводим данные в консоль
            print(name, price, description, address, seller, url)
            if (i + 1) % 5 == 0 and i != 0:
                print("Парсинг приостановлен. Подождите 10 секунд...")
                time.sleep(10)  # Задержка 10 секунд после каждых 5 объявлений
            else:
                print("Подождите 4 секунды перед парсингом следующего объявления...")
                time.sleep(random.uniform(3, 5))  # Рандомная задержка от 3 до 5 секунд

    def parse(self):
        self.__setUp()
        self.__getUrl()
        self.__pg()


if __name__ == "__main__":
    avito_parser = AvitoParse(
        url='https://www.avito.ru/voronezh/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_0q0MrSqLraysFJKK8rPDUhMT1WyLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA',
        count_page=1,
        version_main=114,
        items=["1-к. квартира"]
    )

    avito_parser.parse()
