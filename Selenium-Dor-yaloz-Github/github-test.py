from selenium import webdriver
import time,re
import page
import unittest

class DorGitTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    #def test_repositories_opens(self):
    #    main_page = page.MainPage(self.driver)
    #    pass

    def test_dors_repository_index(self):
        """
        tests whether each of dor's repositories,
        is found on the same index, when the repository name
        is searched on github
        """
        USER_NAME = "doryalo"
        self.driver.get("https://github.com/")
        main_page = page.MainPage(self.driver)
        main_page.commit_search(USER_NAME)
        search_result_page = page.SearchResultsPage(self.driver)
        search_result_page.filter_results_by_user_name()
        search_result_page.navigate_to_user_page(USER_NAME)
        user_page = page.UserProfilePage(self.driver)
        user_page.get_all_repositories_elements()
        user_page.commit_search()
    def tearDown(self):
        print "ended, sleeping for 10 seconds"
        time.sleep(60)
        self.driver.close()

if __name__ == "__main__":
        unittest.main()