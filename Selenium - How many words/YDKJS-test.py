from selenium import webdriver
import selenium.common.exceptions as SE
import time,re

import page
import unittest


class WordSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://github.com/getify/You-Dont-Know-JS")


    def search_whole_book(self,word,book_page,content_page):
        all_chapters_and_appendix = [element.get_attribute("href") for element in
                                     book_page.get_chapters_or_appendix_link_elements()]
        counter = 0
        for ch_or_ap in all_chapters_and_appendix:
            book_page.move_to_chapter_or_appendix(ch_or_ap)
            counter += content_page.count_string_in_content(word)
            self.driver.back()
        return counter

    def test_main(self):
        main_page = page.MainPage(self.driver)
        main_page.get_specific_book_link_element("async & performance").click()
        book_page = page.BookPage(self.driver)
        content_page = page.ContentPage(self.driver)
        print "The chosen word appears {appearence_count} times in the whole book!".format(appearence_count=self.search_whole_book("then",book_page,content_page))


    def tearDown(self):
        time.sleep(5)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()