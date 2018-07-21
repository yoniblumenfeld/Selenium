from selenium import webdriver
import selenium.common.exceptions as SE
import time,re
import page
import unittest

class DorGitTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome("chromedriver.exe")

    #def test_repositories_opens(self):
    #    main_page = page.MainPage(self.driver)
    #    pass
    def analyze_all_repositories(self,repositories_list):
        results_dict={}
        for repo_txt,repo_href in repositories_list:
            try:
                self.search_result_page.commit_search(repo_txt)
                results_dict[repo_txt] = self.search_result_page.get_index_of_repository_in_results(repo_href)
            except SE.StaleElementReferenceException as err:
                print err.msg
        print results_dict

    def test_dors_repository_index(self):
        """
        tests whether each of dor's repositories,
        is found on the same index, when the repository name
        is searched on github
        """
        USER_NAME = "doryalo"
        self.driver.get("https://github.com/")
        self.main_page = page.MainPage(self.driver)
        self.main_page.commit_search(USER_NAME)
        self.search_result_page = page.SearchResultsPage(self.driver)
        self.search_result_page.filter_results_by_user_name()
        self.search_result_page.navigate_to_user_page(USER_NAME)
        self.user_page = page.UserProfilePage(self.driver)
        self.analyze_all_repositories(repositories_list=self.user_page.get_all_repositories_elements())


    def tearDown(self):
        print "ended tests"
        self.driver.close()

if __name__ == "__main__":
        unittest.main()