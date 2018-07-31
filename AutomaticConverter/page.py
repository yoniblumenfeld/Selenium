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

class MainPage(BasePage):
    def get_video_url_placeholder(self):
        return WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.ID,"texturl"))
        )
    def get_start_element(self):
        return WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.ID,"convert1"))
        )

    def submit_url(self,url):
        place_holder = self.get_video_url_placeholder()
        place_holder.clear()
        place_holder.send_keys(url)
        self.get_start_element().click()

    def get_format_choose_div(self):
        return WebDriverWait(driver=self.driver,timeout=10).until(
            EC.presence_of_element_located((By.ID,"select_main"))
        )

    def choose_format(self,format):
        self.get_format_choose_div().click()
        format_element = WebDriverWait(driver=self.driver,timeout=10).until(
            EC.visibility_of_element_located((By.XPATH,"//a[@class='video-format' and @data-value='{format}']".format(format=format)))
        )
        format_element.click()

    def wait_for_convert_to_complete(self):
        while not str(self.driver.current_url).__contains__("success"):
            time.sleep(0.3)


class ConvertedPage(BasePage):
    def click_download_btn(self):
        download_btn = self.driver.find_element_by_id("downloadq")
        download_btn.click()

    pass