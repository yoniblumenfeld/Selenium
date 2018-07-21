import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import helper_funcs

class BasePage(object):
    def __init__(self,driver):
        self.driver = driver #change to driver

    def get_search_bar(self):
        search_bar_element =  WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//input[@name='q']"))
        )
        return search_bar_element

    def commit_seacrh(self,value):
        search_bar_element = self.get_search_bar()
        search_bar_element.send_keys(value)
        search_bar_element.submit()

class MainPage(BasePage):
    pass

class SearchResultsPage(BasePage):

    def get_search_results_table_element(self):
        results_table_element = WebDriverWait(driver=self.driver,timeout=6).until(
            EC.presence_of_element_located((By.XPATH,"//table[@id='searchResult']//tbody"))
        )
        return results_table_element

    def count_search_results(self):
        results_table_element = self.get_search_results_table_element()
        results_elements_list = results_table_element.find_elements_by_tag_name("tr")
        print "Counted results: {res}".format(res=len(results_elements_list))
        return len(results_elements_list)

    def get_search_results_text_element(self):
        text_element = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//h2/span[contains(text(),'results')]/.."))
        )
        return text_element

    def analayze_search_results_text_element(self):
        text_element = self.get_search_results_text_element()
        numbers_from_string_list = helper_funcs.get_numbers_from_string(text_element.text)
        print "Numbers found on search results text element: {nums_list}".format(nums_list=numbers_from_string_list)
        return {"AMOUNT_OF_FOUND_RESULTS_BY_TEXT":int(numbers_from_string_list[1])-int(numbers_from_string_list[0]),
                "AMOUNT_OF_TOTAL_RESULTS":int(numbers_from_string_list[2])}

    def is_page_text_results_match_page_counted_results(self):
        return self.count_search_results() == self.analayze_search_results_text_element()["AMOUNT_OF_FOUND_RESULTS_BY_TEXT"]

    def get_next_page_element(self,current_page):
        next_page_xpath = "//*[@id='content']/div[3]/a[contains(@href,'search') and text()='{next_page}']".format(next_page=current_page+1)
        try:
            next_page_element = WebDriverWait(driver=self.driver,timeout=10).until(
                EC.presence_of_element_located((By.XPATH,next_page_xpath))
            )
            print next_page_element.text
        except Exception as exc:
            print exc.message
            print "Probably reached final page!"
            return -1
        return next_page_element

    def count_total_results_on_all_results_pages(self):
        TOTAL_SEARCH_RESULTS_FOUND_ON_TEXT = int(self.analayze_search_results_text_element()['AMOUNT_OF_TOTAL_RESULTS'])
        TOTAL_SEARCH_RESULTS = 0
        page_counter = 1
        next_page_element = self.get_next_page_element(page_counter)
        current_window_handle = self.driver.current_window_handle
        while next_page_element != -1:
            print "page number: ",page_counter

            self.driver.switch_to.window(current_window_handle)
            TOTAL_SEARCH_RESULTS += self.count_search_results()
            next_page_element = self.get_next_page_element(page_counter)
            print "Total search results: ",TOTAL_SEARCH_RESULTS
            if next_page_element == -1:
                break
            next_page_element.click()
            current_window_handle = self.driver.current_window_handle
            page_counter += 1




        print "do they match: ",TOTAL_SEARCH_RESULTS == TOTAL_SEARCH_RESULTS_FOUND_ON_TEXT
