import time
from selenium.webdriver.common.by import By
import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BasePage(object):
    def __init__(self,driver):
        self.driver = driver
    def get_search_bar(self):
        return WebDriverWait(driver=self.driver,timeout=10).until(
            EC.visibility_of_element_located((By.NAME,"q"))
        )

    def commit_search(self,value,search_bar_element=None):
        if search_bar_element == None:
            search_bar_element = self.get_search_bar()
        search_bar_element.clear()
        search_bar_element.send_keys(value)
        search_bar_element.submit()

class MainPage(BasePage):
    pass

class SearchResultsPage(BasePage):
    def click_filter_button_by_visible_text(self,visible_text):
        users_link_element = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.XPATH,"//a[contains(@class,'menu-item') and contains(text(),'{visible_text}')]".format(visible_text=visible_text)))
        )
        users_link_element.click()

    def filter_results_by_user_name(self):
        self.click_filter_button_by_visible_text("Users")

    def navigate_to_user_page(self,user_name):
        users_link_elements = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@data-hydro-click,'search_result.click')]"))
        )
        for element in users_link_elements:
            if element.text == user_name:
                element.click()
                break

class UserProfilePage(BasePage):
    def get_all_repositories_elements(self):
        repo_elements_list = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_all_elements_located((By.XPATH,"//span[@title and @class='repo js-repo']/parent::a"))
        )
        return repo_elements_list
        #for repository in repo_elements_list:
        #    print repository.get_attribute("href")
        #    print repository.text

    
