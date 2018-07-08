# *- encoding:utf-8 -*
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class Etsy:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.vintage_shoes_list = []

    def add_if_shoes_vintage(self,driver,shoes_element):
        """
        this function adds shoes' href's for shoes' that are considered vintage, judging by the product's description, to the vintage_shoes_list
        """
        description_text_element = shoes_element.find_element_by_xpath(".//p[@class='text-gray text-truncate mb-xs-0 text-body']")
        if re.search("vintage", description_text_element.text, re.IGNORECASE) != None:
            if not(shoes_element.get_attribute("href") in self.vintage_shoes_list):
                self.vintage_shoes_list.append(shoes_element.get_attribute("href"))


    def find_vintage_out_of_main_shoes(self,driver):
        """
        this function finds all the products founds on the shoes search operation.
        it calls the map function to run the add_if_shoes_vintage function on each product element.
        """
        all_shoes = WebDriverWait(driver=driver, timeout=7).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[@data-listing-id and @data-logging-key and @title]"))
        )
        map(lambda shoes: self.add_if_shoes_vintage(driver,shoes),all_shoes)

    def search_for_shoes(self,driver):
        """
        this method searches for shoes in the search-bar.
        it waits for the search bar element to be located and interacts with it.
        """

        search_input = WebDriverWait(driver=driver, timeout=10).until(
            EC.presence_of_element_located((By.ID, "search-query"))
        )  # waiting for search input element to be loaded
        search_input.send_keys("shoes")  # searches shoes
        search_input.submit()  # submits the search

    def sort_vintage_by_radio(self,driver):
        """
        checking the Vintage item-type checkbutton. thus, causing only vintage items to appear.
        """
        vintage_item_type_radio_btn = driver.find_element_by_xpath("//a[contains(@data-context,'item_type') and contains(text(),'Vintage')]")
        vintage_item_type_radio_btn.click()

    def test_flow(self):
        """
        this method contains the flow of the test, so the flow of
        the test is easier to understand
        """
        driver = self.driver
        driver.get("https://www.etsy.com/")
        self.search_for_shoes(driver)
        self.find_vintage_out_of_main_shoes(driver)
        print self.vintage_shoes_list #the shoes found without checking the Vintage item-type checkbox
        self.sort_vintage_by_radio(driver)
        self.find_vintage_out_of_main_shoes(driver)
        print self.vintage_shoes_list #the shoes found after checking the vintage item-type checkbox

        time.sleep(30)


    def run_test(self):
        """
        a method used to run the test, in a way that in the end of the test automated-chrome will be closed.
         and the chromedriver process will be closed.
         its job is basically doing cleanups.
        """
        try:
            self.test_flow()
        except Exception as err:
            print err
        finally:
            self.driver.close()
            self.driver.quit()


if __name__ == "__main__":
    etsy = Etsy()
    etsy.run_test()