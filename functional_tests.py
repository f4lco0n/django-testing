import time
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import unittest
from contextlib import contextmanager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import staleness_of

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()


    def wait_for_row_in_list_table(self,row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text,[row.text for row in rows])
            except (AssertionError,WebDriverException) as e:
                if time.time() - start_time > 5:
                    raise e
                time.sleep(0.1)

    def test_can_start_list_and_retrieve_it_later(self):
        """#start point of app"""
        self.browser.get('http://localhost:8000')
        self.assertIn('Listy',self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('Listy',header_text)

        #find element by given id and test his attribute
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Wpisz rzeczy do zrobienia')

        #hardcode given text
        inputbox.send_keys('Kupić pióra')
        inputbox.send_keys(Keys.ENTER)

        self.wait_for_row_in_list_table('1: Kupić pióra')


        self.fail('Zakonczenie testu')

if __name__=='__main__':
    unittest.main(warnings='ignore')






