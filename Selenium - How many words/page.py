import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver


class BasePage(object):
    def __init__(self,driver):
        self.driver = driver
        self.books_names_to_index_dict = {"async & performance":2,"es6 & beyond":3,
                            "scope & closures":4,"this & object prototypes":5,
                            "types & grammar":6,"up & going":7}
class MainPage(BasePage):
    def get_specific_book_link_element(self,book_name):
        return WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.XPATH,
                                            '//*[@id="js-repo-pjax-container"]/div[2]/div[1]/div[6]/table/tbody/tr[{book_name}]/td[@class="content"]'.format(book_name=self.books_names_to_index_dict[book_name])))
        )


class BookPage(BasePage):
    def get_chapters_or_appendix_link_elements(self):
        return WebDriverWait(self.driver,10).until(
            EC.presence_of_all_elements_located((By.XPATH,
                                                 "//*[@id='js-repo-pjax-container']/div[2]/div[1]/div[3]/table/tbody[2]/tr/td[@class='content']/span/a[contains(@title,'ch') or contains(@title,'ap')]"))
        )
    def print_all_relevant_elements(self):
        for element in self.get_chapters_or_appendix_link_elements():
            print element.get_attribute("href")

    def move_to_chapter_or_appendix(self,chapter_or_appendix):
        self.driver.get(chapter_or_appendix)


class ContentPage(BasePage):
    def get_content_element(self):
        return WebDriverWait(self.driver,10).until(
            EC.presence_of_element_located((By.CLASS_NAME,"file"))
        )

    def count_string_in_content(self,string_to_count):
        content_element = self.get_content_element()
        count = (content_element.text).count(string_to_count)
        print count
        return count
