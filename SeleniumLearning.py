# *- encoding: utf-8 -*

from selenium import webdriver
import unittest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Yad2(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.i7_products_urls=[]

    def iterate_all_computers(self,driver):
        """
        functions that iterates all the products found on the yad2 search results.
        for each product, it runs the working_on_product function
        """
        elements = driver.find_elements_by_class_name("gallery_block_body")
        for element in elements:
            self.working_on_product(driver,element)
            time.sleep(5)

    def is_product__i7(self,string):
        try:
            print "found ",unicode(string).find("i7")
            return unicode(string).find("i7") > -1 or unicode(string).find("I7") > -1
        except Exception as err:
            print err


    def add_if_i7_product(self,element,url):
        if self.is_product__i7(element.text):
            self.i7_products_urls.append(url)
            print "{line_mark}Product Added {url}{line_mark}".format(url=url,line_mark="*"*10+"\n")

    def working_on_product(self,driver,product_element):
        """
        function that runs on each product that is opened on main yad2->computers page
        for each product in tries to open new tab (because trying to manipulate page-source fails, because data about product
        is loaded into an iframe on the main page
        """
        mainHandle = ""
        product_element.click()
        for handle in driver.window_handles:
            if mainHandle == "":
                mainHandle = handle
            else:
                driver.switch_to.window(handle)
                try:
                    driver.switch_to_frame(driver.find_element_by_id("hotPic_iframe"))
                    for index,element in enumerate(driver.find_elements_by_class_name("innerDetailsDataGrid")):
                        if index%2 != 0:
                            self.add_if_i7_product(element,driver.current_url)
                    print self.i7_products_urls
                except Exception as err:
                    print err
                    continue
                time.sleep(3)
        driver.switch_to.window(mainHandle)


    def test_search_in_yad2(self):
        """
        the main function, running on the main yad2 page and looking for computers using
        hebrew keyword מחשבים and the relevant category text
        """
        driver = self.driver
        driver.get("http://www.yad2.co.il/")
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "CatNSubCat"))
        )
        self.change_CatNSubCat_to_visibile(driver)
        select = Select(element)
        select.select_by_visible_text(u"מוצרי סלולר ודיגיטל")
        self.search_string(driver,u"מחשבים")
        self.iterate_all_computers(driver)



        time.sleep(60)

    def change_CatNSubCat_to_visibile(self,driver):
        """
        a function that changes the CatNSubCat select element to visible,
        in order to make it possible doing select-elements operation on it
        """
        js_change_attribute="""
        document.getElementsByName('CatNSubCat')[0].removeAttribute('style')
        """
        driver.execute_script(js_change_attribute)

    def search_string(self,driver,string):
        """
        a function that submits the search in the yad2 main page, of a given string
        """
        search_input = driver.find_element_by_name("q")
        search_input.send_keys(string)
        search_input.submit()

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()