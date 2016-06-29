from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys 

class VisitorTest(LiveServerTestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)
    
    def tearDown(self):
        self.browser.quit()

    def register(self):
        
        self.browser.get('%s%s' %(self.live_server_url, '/accounts/register/')) 
             
        username = self.browser.find_element_by_id('id_username')
        email = self.browser.find_element_by_id('id_email')
        password1 = self.browser.find_element_by_id('id_password1')
        password2 = self.browser.find_element_by_id('id_password2')
               
        username.send_keys('user20')
        email.send_keys('user20@email.com')
        password1.send_keys('password20')
        password2.send_keys('password20')
# #         self.browser.find_element_by_xpath('//input[@value="Submit"]').click()
        self.browser.find_element_by_class_name("btn").click()
        
    def test_can_access_index_page_no_seqls(self):
        print 'Selenium: Running %s ...' % self._testMethodName
        
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/'))
        
        self.assertIn('st26proto - Index', self.browser.title) 
        
        headers_h2 = self.browser.find_elements_by_tag_name('h2')
        self.assertIn('WELCOME', [h.text for h in headers_h2])
        self.assertIn('SEQUENCE LISTING PORTOFOLIO', [h.text for h in headers_h2])
              
        no_seqls_par = self.browser.find_element_by_id('no_seqls_par')  
        self.assertEqual('No sequence listings are available.', no_seqls_par.text)
        self.assertEqual(0, len(self.browser.find_elements_by_tag_name('table')), 
                         'There should be no table if no seqls created.')
    
    def test_about_page(self):
        print 'Selenium: Running %s ...' % self._testMethodName
        
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/about'))   
        
        self.assertIn('st26proto - About', self.browser.title)

    def test_register(self):
        print 'Selenium: Running %s ...' % self._testMethodName
        
        self.register()
        self.browser.get('%s%s' % (self.live_server_url, '/sequencelistings/'))
        self.assertIn('st26proto - Index', self.browser.title)
        self.assertIn('user20', self.browser.find_element_by_class_name('page-header').text)

    def test_add_sequencelisting_functionality(self):
        print 'Selenium: Running %s ...' % self._testMethodName
        
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/')) 
        # unregistered visitors are not allowed to add seqls i.e. there is no link to add seql
        self.assertEqual(0, len(self.browser.find_elements_by_id('add_seql_link'))) 
        
        self.register()
        self.browser.get('%s%s' %(self.live_server_url, '/sequencelistings/add_sequencelisting')) 
        self.assertIn('Create a sequence listing', self.browser.find_element_by_tag_name('h2').text)


