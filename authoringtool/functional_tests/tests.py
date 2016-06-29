from selenium import webdriver
import unittest

class VisitorTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
        
    def test_can_access_index_page(self):
        print 'Running selenium test_can_access_index_page ...'
        self.browser.get('http://localhost:8000/sequencelistings')
        self.assertIn('st26proto - Index', self.browser.title) 

if __name__ == '__main__':
    unittest.main()