from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

class ExerciseTwo():
    def __init__(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
    def mainTest(self):
        driver=self.driver
        driver = self.restart_to_main(driver)
        tests = [self.testBadPassword,self.testGoodCreds,self.testIncorrectPasswordShows]
        [self.test_status(test,driver) for test in tests]

        time.sleep(60)

    def restart_to_main(self,driver):
        driver.get("http://tvroom.github.io/selenium-exercises/ex2/")
        return driver

    def getFormElements(self,driver):
        return (driver.find_element_by_name("username"),driver.find_element_by_name("password"))

    def test_status(self,func,driver):
        print "{func_name} Succeed: {status}".format(func_name=func.func_name,status=func(driver))

    def testBadPassword(self,driver):
        driver = self.restart_to_main(driver)
        user_name_text_field,password_text_field = self.getFormElements(driver)
        user_name_text_field.send_keys("bob")
        password_text_field.send_keys("foobz")
        user_name_text_field.submit()
        return self.who_logged_in(driver) == "guest"

    def testGoodCreds(self,driver):
        driver = self.restart_to_main(driver)
        user_name_text_field,password_text_field = self.getFormElements(driver)
        user_name_text_field.send_keys("bob")
        password_text_field.send_keys("foobaz")
        user_name_text_field.submit()
        return self.who_logged_in(driver) != "guest"

    def testIncorrectPasswordShows(self,driver):
        driver = self.restart_to_main(driver)
        user_name_text_field,password_text_field = self.getFormElements(driver)
        user_name_text_field.send_keys("bob")
        password_text_field.send_keys("wrong")
        user_name_text_field.submit()
        return self.is_incorrect_pwd_shown(driver)

    def who_logged_in(self,driver):
        who_is_logged = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'user'))
        )
        return who_is_logged.text

    def is_incorrect_pwd_shown(self,driver):
        msg = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'error'))
        )
        return msg.text == "Incorrect Password"

if __name__ == "__main__":
    ex = ExerciseTwo().mainTest()