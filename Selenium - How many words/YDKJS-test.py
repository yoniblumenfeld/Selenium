from selenium import webdriver
import selenium.common.exceptions as SE
import time,re

import page
import unittest


class WordSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.get("https://github.com/getify/You-Dont-Know-JS")

    def iterate_whole_series(self,main_page,book_page,content_page,word="then"):
        main_page_url = self.driver.current_url
        books_href_list = [main_page.get_specific_book_link_element(book_name)\
                           for book_name in main_page.books_names_to_index_dict.keys()]
        print books_href_list
        books_href_list = [book.get_attribute("href") for book in books_href_list]
        series_counter = 0
        for book_href in books_href_list:
            self.driver.get(book_href)
            series_counter += self.iterate_whole_book(word,book_page,content_page)
            self.driver.get(main_page_url)
        return series_counter

    def iterate_whole_book(self,word,book_page,content_page):
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
        book_page = page.BookPage(self.driver)
        content_page = page.ContentPage(self.driver)
        print "The following word: {word} appears {appearence_count} times in the whole series!".format(
            word="then",
            appearence_count=self.iterate_whole_series(main_page,
                                                       book_page,
                                                       content_page,
                                                       "then")
        )

        #print "The chosen word appears {appearence_count} times in the whole book!".format(appearence_count=self.iterate_whole_book("then",book_page,content_page))

    def tearDown(self):
        time.sleep(5)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()