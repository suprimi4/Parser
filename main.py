import undetected_chromedriver as uc
import time
import random
import os
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

class AvitoParse:
    def __init__(self, url: str, count_page=5, version_main=None):
        self.url = url
        self.count_page = count_page
        self.version_main = version_main
        self.driver = None
        self.page_number = 1

    def __setUp(self):
        self.driver = uc.Chrome(version_main=self.version_main)

    def __getUrl(self):
        self.driver.get(self.url)
        self.__simulateHumanScrolling()
        self.__simulateMouseMovement()

    def __simulateHumanScrolling(self):
        scroll_down = "window.scrollTo(0, document.body.scrollHeight/3);"
        scroll_up = "window.scrollTo(0, -document.body.scrollHeight/4);"
        self.driver.execute_script(scroll_down)
        time.sleep(random.uniform(1, 2))
        self.driver.execute_script(scroll_up)
        time.sleep(random.uniform(1, 2))

    def __simulateMouseMovement(self):
        # Перемещение мыши на случайное смещение в пределах видимой части окна
        action = ActionChains(self.driver)
        move_x = random.randint(100, 500)  # Случайное смещение по горизонтали
        move_y = random.randint(100, 500)  # Случайное смещение по вертикали
        action.move_by_offset(move_x, move_y).perform()
        time.sleep(random.uniform(0.5, 1.5))  # Пауза после перемещения

    def __pg(self):
        while self.driver.find_element(By.CSS_SELECTOR,
                                       "[data-marker='pagination-button/nextPage']") and self.count_page > 0:
            self.__simulateHumanScrolling()
            self.__simulateMouseMovement()
            self.__parsePage()
            time.sleep(random.uniform(15, 20))  # Pause before clicking next
            self.driver.find_element(By.CSS_SELECTOR, "[data-marker*='pagination-button/next']").click()

            self.count_page -= 1

    def __saveToHTML(self, html, filepath):
        with open(filepath, 'w', encoding='utf-8') as html_file:
            html_file.write(html)
            print(f"HTML-код страницы успешно сохранен в файл {filepath}")

    def __createFolder(self, folder):
        if not os.path.exists(folder):
            os.makedirs(folder)

    def __parsePage(self):
        html = self.driver.page_source
        folder_name = time.strftime("%Y%m%d")
        folder_path = os.path.join("source", folder_name)
        self.__createFolder(folder_path)
        filename = f"{time.strftime('%H%M%S')}_{self.page_number}.html"
        filepath = os.path.join(folder_path, filename)
        self.__saveToHTML(html, filepath)
        self.page_number += 1

    def parse(self):
        self.__setUp()
        self.__getUrl()
        self.__pg()

if __name__ == "__main__":
    avito_parser = AvitoParse(
        url='https://www.avito.ru/voronezh/kvartiry/prodam-ASgBAgICAUSSA8YQ?context=H4sIAAAAAAAA_0q0MrSqLrYyNLNSKk5NLErOcMsvyg3PTElPLVGyrgUEAAD__xf8iH4tAAAA',
        count_page=2,
        version_main=114,
    )
    avito_parser.parse()
