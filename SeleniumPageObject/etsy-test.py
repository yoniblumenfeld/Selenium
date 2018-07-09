from selenium import webdriver
import time
import etsy_page_object as page
import unittest

class Etsy(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://www.etsy.com/")

    def test_main(self):
        print "hi"
        main_page = page.MainPage(self.driver)
        main_page.search_value("shoes")
        search_results_page = page.SearchResultsPage(self.driver)
        search_results_page.add_vintage_item_type_filter()
        all_vintage_shoes = search_results_page.get_all_items_containing_value_in_description(value="vintage")
        for shoes in all_vintage_shoes:
            print shoes.get_attribute("href")

    def tearDown(self):
        self.driver.close()

if __name__=="__main__":
    unittest.main()