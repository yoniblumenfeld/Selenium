from selenium import webdriver
import time
import etsy_page_object as page
import unittest

class Etsy(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    def test_vintage_shoes(self):
        self.driver.get("https://www.etsy.com/")
        main_page = page.MainPage(self.driver)
        main_page.search_value("shoes")
        search_results_page = page.SearchResultsPage(self.driver)
        search_results_page.add_vintage_item_type_filter()
        all_vintage_shoes = search_results_page.get_all_items_containing_value_in_description(value="vintage")
        try:
            assert len(all_vintage_shoes) > 0
            print "Vintage shoes found"
        except AssertionError:
            print "No vintage shoes found"

    def test_title_matches_description(self):
        self.driver.get("https://www.etsy.com/")
        main_page = page.MainPage(self.driver)
        main_page.search_value("shoes")
        search_results_page = page.SearchResultsPage(self.driver)
        first_item = search_results_page.get_first_item()
        try:
            assert search_results_page.compare_item_title_to_description(first_item)
            print "The title of the product is in its description"
        except AssertionError:
            print "The title of the product is not in its description"



    def tearDown(self):
        self.driver.close()

if __name__=="__main__":
    unittest.main()