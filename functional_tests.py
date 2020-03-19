from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)

    def tearDown(self):
        self.browser.quit()


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

        #find table by id and get rows
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')

        #compare text from inputbox to updated table
        self.assertTrue(
            any(row.text == '1: Kupić pióra' for row in rows))

        self.fail('Zakonczenie testu')

if __name__=='__main__':
    unittest.main(warnings='ignore')






