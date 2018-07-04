# *- encoding:utf-8 -*
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time,string,random

def generate_password():
    """
    a function that generates password conssisting of letters and numbers
    """
    alphabet = list(string.ascii_letters)
    digits = [str(i) for i in xrange(10)]
    generated_digits = [str(generate_index(0,len(digits))) for i in xrange(3)]
    generated_letters = [alphabet[generate_index(0,len(alphabet)-1)] for i in xrange(random.randint(6,10))]
    return "".join(generated_digits+generated_letters)

def generate_index(min_idx,max_idx):
    return random.randint(min_idx,max_idx)

def generate_phone_number_post_fix():
    return "".join([str(generate_index(0,10)) for i in xrange(7)])

class RegisterWalla:
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    def fill_right_user_name(self,driver,username_elmt,uname):
        check_availability_button = driver.find_element_by_xpath("//button[@ng-click='checkIfAvailableUsername()']")
        username_elmt.send_keys(uname)
        check_availability_button.click()
        suggested_option = WebDriverWait(driver,10).until(
            EC.visibility_of_element_located((By.XPATH,"//button[@ng-click='chooseUsernameFromSuggestions(firstSuggestedUsername)']"))
        ).click()

    def fill_right_user_password(self,driver,pwd_elmt):
        pwd_elmt.send_keys(generate_password())

    def fill_user_name_and_password(self,driver):
        username_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, 'username'))
        )
        self.fill_right_user_name(driver, username_element, 'user12')
        password_element = driver.find_element_by_id("pw")
        self.fill_right_user_password(driver, password_element)

    def fill_private_and_last_name(self,driver):
        private_name,last_name = driver.find_element_by_id("privateName"),driver.find_element_by_id("surname")
        private_name.send_keys(u'סתם')
        last_name.send_keys(u'משתמש')

    def fill_date(self,driver):
        Select(driver.find_element_by_id('day')).select_by_value('01') #fill day 01
        Select(driver.find_element_by_id('month')).select_by_value('01') #fill month october (10)
        Select(driver.find_element_by_id('year')).select_by_value('1996') #fill year 1998


    def fill_phone(self,driver):
        select_phone_prefix,phone_post_fix = Select(driver.find_element_by_id("altPhonePrefix")),driver.find_element_by_id("altPhonePostfix")
        select_phone_prefix.select_by_value("0")  # prefix 050
        phone_post_fix.send_keys(generate_phone_number_post_fix())

    def fill_random_gender(self,driver):
        gender_elmts = driver.find_elements_by_name("gender")
        choice = random.randint(1,2)
        print choice
        for index,gender_element in enumerate(gender_elmts):
            if index+1==choice:
                gender_element.click()

    def click_gatcha(self,driver):
        gatpcha_element = driver.find_element_by_class_name("recaptcha-checkbox-checkmark")
        gatpcha_element.click()
    def test_main(self):
        driver = self.driver
        driver.get("https://friends.walla.co.il/#/register")
        self.fill_user_name_and_password(driver)
        self.fill_private_and_last_name(driver)
        self.fill_phone(driver)
        self.fill_date(driver)
        self.fill_random_gender(driver)
        self.click_gatcha(driver)
        time.sleep(60)







if __name__=="__main__":
    RegisterWalla().test_main()