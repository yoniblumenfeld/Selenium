from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time,string,random

def generate_password():
    alphabet = list(string.ascii_letters)
    digits = [str(i) for i in xrange(10)]
    generated_digits = [str(generate_index(0,len(digits))) for i in xrange(3)]
    generated_letters = [alphabet[generate_index(0,len(alphabet)-1)] for i in xrange(random.randint(6,10))]
    return "".join(generated_digits+generated_letters)

def generate_index(min_idx,max_idx):
    return random.randint(min_idx,max_idx)

class RegisterWalla():
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
        generated_pwd = generate_password()
        pwd_elmt.send_keys(generated_pwd)

    def test_main(self):
        driver = self.driver
        driver.get("https://friends.walla.co.il/#/register")
        username_element = WebDriverWait(driver,10).until(
            EC.presence_of_element_located((By.ID,'username'))
        )
        self.fill_right_user_name(driver,username_element,'yonib12')
        password_element = driver.find_element_by_id("pw")
        self.fill_right_user_password(driver, password_element)

        private_name = driver.find_element_by_id("privateName")
        last_name = driver.find_element_by_id("surname")

        select_phone_prefix = Select(driver.find_element_by_id("altPhonePrefix"))
        select_phone_prefix.select_by_value("0") #prefix 050
        phone_post_fix = driver.find_element_by_id("altPhonePostfix")

        birth_date_day = Select(driver.find_element_by_id('day'))
        birth_date_day.select_by_value('01')
        birth_date_month = Select(driver.find_element_by_id('month'))
        birth_date_month.select_by_value('10')
        birth_date_year = Select(driver.find_element_by_id('year'))
        birth_date_year.select_by_value('1998')



        time.sleep(60)







if __name__=="__main__":
    generate_password()
    RegisterWalla().test_main()