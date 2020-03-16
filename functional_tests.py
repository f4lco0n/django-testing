from selenium import webdriver
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
        self.fail('Zakonczenie testu')


if __name__=='__main__':
    unittest.main(warnings='ignore')






