import time
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()


    def check_for_row_in_list_table(self,row_text):
        time.sleep(5)
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        self.assertIn(row_text,[row.text for row in rows])

    def test_can_start_list_and_retrieve_it_later(self):
        """#start point of app"""
        self.browser.get(self.live_server_url)
        self.assertIn('Listy',self.browser.title)
        # header_text = self.browser.find_element_by_tag_name('h1').text
        # self.assertIn('Listy',header_text)

        #find element by given id and test his attribute
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'),'Wpisz rzeczy do zrobienia')

        #hardcode given text
        inputbox.send_keys('Kupić pióra')
        inputbox.send_keys(Keys.ENTER)
        user1_list_url = self.browser.current_url
        # self.assertRegex(user1_list_url,'/lists/.+')
        self.check_for_row_in_list_table('1: Kupić pióra')

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Uzyc pior')
        inputbox.send_keys(Keys.ENTER)

        self.check_for_row_in_list_table('2: Uzyc pior')
        self.check_for_row_in_list_table('1: Kupić pióra')

        #new user visits website

        self.browser.quit()
        self.browser = webdriver.Firefox()

        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pióra',page_text)
        self.assertNotIn('uzyc pior',page_text)

        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('Kupić mleko')
        inputbox.send_keys(Keys.ENTER)

        #unique url for second user
        user2_list_url = self.browser.current_url
        # self.assertRegex(user2_list_url,'/lists/.+')
        self.assertNotEqual(user2_list_url,user1_list_url)

        #check if there is something after user1
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Kupić pióra',page_text)
        self.assertIn('Kupić mleko',page_text)


    def test_layout_and_styling(self):

        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'],
            512,
            delta=5
        )




