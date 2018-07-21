from selenium import webdriver
import selenium.common.exceptions as SE
import time,re
import page
import unittest

class TpbTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://pirateproxy.mx/")

    def test_tpb_results(self):
        main_page = page.MainPage(self.driver)
        main_page.commit_seacrh("sims")
        search_results_page = page.SearchResultsPage(self.driver)
        #search_results_page.count_search_results()
        #search_results_page.get_search_results_text_element()
        #search_results_page.analayze_search_results_text_element()
        search_results_page.count_total_results_on_all_results_pages()



    def tearDown(self):
       #time.sleep(10)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()