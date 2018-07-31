from selenium import webdriver
import selenium.common.exceptions as SE
import time,re

import page
import unittest

class Converter(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('chromedriver.exe')
        self.urls = ["https://www.ssl.com/why-you-need-ssl-for-your-website/",
                     "https://blog.hubspot.com/marketing/what-is-ssl",
                     "https://www.youtube.com/watch?v=ERp8420ucGs",
                     "https://www.youtube.com/watch?v=SJJmoDZ3il8",
                     "https://www.youtube.com/watch?v=i-rtxrEz_E8",
                     "https://www.youtube.com/watch?v=AQDCe585Lnc",
                     "http://info.ssl.com/article.aspx?id=10241",
                     "https://www.youtube.com/watch?v=3QnD2c4Xovk"
                     ]
    def test_main(self):
        main_page = page.MainPage(self.driver)
        converted_page = page.ConvertedPage(self.driver)
        for url in self.urls:
            self.driver.get("https://www.onlinevideoconverter.com/video-converter")
            main_page.choose_format("mp4")
            main_page.submit_url(url)
            main_page.wait_for_convert_to_complete()
            converted_page.click_download_btn()
            time.sleep(1)

    def tearDown(self):
        time.sleep(10)
        self.driver.close()

if __name__ == "__main__":
    unittest.main()