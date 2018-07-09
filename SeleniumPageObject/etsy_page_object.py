import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC



class BasePage(object):
    def __init__(self,driver):
        self.driver = driver

class MainPage(BasePage):
    url = "https://www.etsy.com/"
    def get_search_bar_element(self):
        search_input_element = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.ID,"search-query"))
        )
        return search_input_element

    def search_value(self,value,search_bar_element=None):
        if search_bar_element == None:
            search_bar_element = self.get_search_bar_element()
        search_bar_element.clear()
        search_bar_element.send_keys(value)
        search_bar_element.submit()


class SearchResultsPage(BasePage):
    def find_item_type_button(self,text):
        item_type_button_by_value = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//a[contains(@data-context,'item_type') and contains(text(),'{item_type}')]".format(item_type=text)))
        )
        return item_type_button_by_value

    def add_vintage_item_type_filter(self):
        vintage_item_button = self.find_item_type_button("Vintage")
        vintage_item_button.click()

    def get_all_items(self):
        all_items = WebDriverWait(driver=self.driver, timeout=7).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[@data-listing-id and @data-logging-key and @title]"))
        )
        return all_items

    def get_all_items_containing_value_in_description(self,all_items=None,value="vintage"):
        if all_items == None:
            all_items = self.get_all_items()
        return filter(lambda item: self.filter_value_in_item_description(value=value,item_element=item),all_items)

    def get_first_item(self):
        return self.get_all_items()[0]

    def compare_item_title_to_description(self,item):
        item_title = item.get_attribute("title")
        self.click_item(item)
        item_page = ItemPage(self.driver)
        description_element = item_page.get_description_element()
        return item_title in description_element.text

    def click_item(self,item):
        self.driver.get(item.get_attribute("href"))

    def filter_value_in_item_description(self,item_element,value=""):
        description_text_element = item_element.find_element_by_xpath(".//p[@class='text-gray text-truncate mb-xs-0 text-body']")
        if re.search(value, description_text_element.text, re.IGNORECASE) != None:
            return item_element


class ItemPage(BasePage):
    def get_description_element(self):
        return self.driver.find_element_by_id("description-text")