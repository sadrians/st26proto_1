from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

class VisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()
        
    def test_can_access_index_page(self):
        print 'Running selenium test_can_access_index_page ...'
        
        current_url = '%s%s' %(self.live_server_url, '/sequencelistings/')
        print 'current_url', current_url
#         self.browser.get('http://localhost:8000/sequencelistings')
        self.browser.get(current_url)
        
        self.assertIn('st26proto - Index', self.browser.title) 
        
        headers_h2 = self.browser.find_elements_by_tag_name('h2')
        self.assertIn('WELCOME', [h.text for h in headers_h2])
        self.assertIn('SEQUENCE LISTING PORTOFOLIO', [h.text for h in headers_h2])
