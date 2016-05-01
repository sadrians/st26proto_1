#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from models import SequenceListing, Title, Sequence, Feature, Qualifier
from forms import QualifierForm
import views

from django.utils import timezone
import util 

import inspect 
import os
import logging

from selenium import webdriver 

logger = logging.getLogger(__name__)
logger.info('TEST start.')

TEST_DATA_DIR_PATH = os.path.join(util.PROJECT_DIRECTORY, 
                                       'sequencelistings', 'testData')



def getName():
    return inspect.stack()[1][3]
 
class SequenceListingFixture(object):
    def create_sequencelisting_instance(self):
        sl = SequenceListing.objects.create(
            fileName = 'test_xmlsql',
            dtdVersion = '1',
            softwareName = 'prototype',
            softwareVersion = '0.1',
            productionDate = timezone.now().date(),
              
            applicantFileReference = '123',
       
            IPOfficeCode = 'EP',
            applicationNumberText = '2015123456',
            filingDate = timezone.now().date(),
           
            earliestPriorityIPOfficeCode = 'US',
            earliestPriorityApplicationNumberText = '998877',
            earliestPriorityFilingDate = timezone.now().date(),
           
            applicantName = 'John Smith',
            applicantNameLanguageCode = 'EN',
            applicantNameLatin = 'same',
           
            inventorName = 'Mary Dupont',
            inventorNameLanguageCode = 'FR',
            inventorNameLatin = 'Mary Dupont',        
            )
        self.create_title_instance(sl)
         
        return sl 
  
    def create_title_instance(self, sl):
        return Title.objects.create(
                    sequenceListing = sl,
                    inventionTitle = 'Invention 1',
                    inventionTitleLanguageCode = 'EN')
      
    def create_sequence_instance(self, sl):
        return Sequence.objects.create(
                    sequenceListing = sl,
                    moltype = 'DNA',
                    residues = 'catcatcatcatcatcat')
      
    def create_feature_instance(self, s):
        return Feature.objects.create(sequence=s, 
                                      featureKey='source', 
                                      location='1..%s' % s.length)
      
    def create_organism_qualifier_instance(self, sourceFeature):
        return Qualifier.objects.create(feature=sourceFeature, 
                                      qualifierName='organism', 
                                      qualifierValue='Homo sapiens')
       
    def create_mol_type_qualifier_instance(self, sourceFeature):
        return Qualifier.objects.create(feature=sourceFeature, 
                                      qualifierName='mol_type', 
                                      qualifierValue='genomic DNA')
 
class NoSequenceListingViewTest(TestCase):
    def test_index_view_with_no_sequencelistings(self):
        """
        If no sequence listings exist, an appropriate message should be displayed.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sequence listings are available.")
        self.assertQuerysetEqual(response.context['sequencelistings'], [])
             
class SequenceListingViewTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(SequenceListingViewTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
           
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
       
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
                     
    def test_index_view_with_one_sequencelisting(self):
        """
        The sequence listings index, displays one sequence listing.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_xmlsql")
        self.assertContains(response, "Invention 1")
        self.assertQuerysetEqual(response.context['sequencelistings'], 
                                 ['<SequenceListing: Sequence listing test_xmlsql>'])
           
    def test_detail_view(self):
        """
        The details of the sequence listing are correctly displayed.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_xmlsql")
        self.assertContains(response, "2015123456")
        self.assertEqual(response.context['sequencelisting'], self.sequenceListing)
#         there are no sequences created yet:
        self.assertFalse(response.context['sequencelisting'].sequence_set.all())
#         now a sequence is created
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        self.assertTrue(response.context['sequencelisting'].sequence_set.all())
        self.sequenceListingFixture.create_feature_instance(s1)
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.pk]))
#         print response
        self.assertContains(response, "location")
        self.assertContains(response, "Generate XML")
#         if the user is logged in: TODO: see what is this?
#         self.assertContains(response, "Add new sequence")
              
    def test_add_seq_view(self):
        """
        The form add_seq is correctly displayed.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:add_seq', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Molecule type")
        self.assertContains(response, "Residues")
              
    def test_add_feature_view(self):
        """
        The form add_feature is correctly displayed.
        """
        print 'Running %s ...' % getName()
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        response = self.client.get(reverse('sequencelistings:add_feature', args=[1, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feature key")
         
    def test_createSequence(self):
        """
        The sequence listing detail page, displays the generated sequences.
        """
        print 'Running %s ...' % getName()
            
        self.assertEqual(0, self.sequenceListing.sequenceTotalQuantity)
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
            
        self.assertEqual(1, self.sequenceListing.sequenceTotalQuantity)
        self.assertEqual(1, s1.sequenceIdNo)
        self.assertEqual('catcatcatcatcatcat', s1.residues)
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
              
        s2 = Sequence.objects.create(
            sequenceListing = self.sequenceListing,
            moltype = 'RNA',
            residues = 'caucaucaucaucaucaucc')
              
        self.assertEqual(2, self.sequenceListing.sequenceTotalQuantity)
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
        self.assertContains(response, "20")
        self.assertContains(response, "RNA")
      
    def test_getOrganism(self):
        """
        Test that the Sequence object returns correctly the organism value.
        """
        print 'Running %s ...' % getName()
            
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
             
        self.assertEqual(None, s1.getOrganism())
             
        f1 = self.sequenceListingFixture.create_feature_instance(s1)
             
        self.assertEqual(None, s1.getOrganism())
             
        self.sequenceListingFixture.create_organism_qualifier_instance(f1)
             
        self.assertEqual('Homo sapiens', s1.getOrganism())
             
        s2 = Sequence.objects.create(
                sequenceListing = self.sequenceListing,
                moltype = 'AA',
                residues = 'MRTAVTAD')
        self.assertEqual(None, s2.getOrganism())
             
        f2 = Feature.objects.create(sequence=s2, 
                                  featureKey='SOURCE', 
                                  location='1..%s' % s2.length)
        self.assertEqual(None, s2.getOrganism())
     
        Qualifier.objects.create(feature=f2, 
                                  qualifierName='ORGANISM', 
                                  qualifierValue='Mus musculus')
        self.assertEqual('Mus musculus', s2.getOrganism())
     
               
        s3 = Sequence.objects.create(
            sequenceListing = self.sequenceListing,
            moltype = 'RNA',
            residues = 'caucaucaucaucaucau')
        f3 = Feature.objects.create(sequence=s3, 
                                  featureKey='source', 
                                  location='1..%s' % s3.length)
             
        Qualifier.objects.create(feature=f3, 
                                  qualifierName='organism', 
                                  qualifierValue='Drosophila')
        self.assertEqual('Drosophila', s3.getOrganism())
      
    def test_createFeature(self):
        """
        The sequence listing detail page, displays the generated feature.
        """
        print 'Running %s ...' % getName()
            
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
              
        f1 = Feature.objects.create(sequence=s1, 
                                    featureKey='source', 
                                    location='1..4')
        self.assertEqual('source', f1.featureKey)
        self.assertEqual('1..4', f1.location)
             
        f = s1.feature_set.all()
        self.assertEqual(1, len(f), 'Expected 1 feature.')
        self.assertEqual('source', f[0].featureKey)
             
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "source")
        self.assertContains(response, "1..4")
          
    def test_createQualifier(self):
        """
        The sequence listing detail page, displays the generated qualifier.
        """
        print 'Running %s ...' % getName()
            
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f1 = self.sequenceListingFixture.create_feature_instance(s1)
      
        q1 = Qualifier.objects.create(feature=f1, 
                                      qualifierName='organism', 
                                      qualifierValue='Homo sapiens')
              
        self.assertEqual('organism', q1.qualifierName)
        self.assertEqual('Homo sapiens', q1.qualifierValue)
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "organism")
        self.assertContains(response, "Homo sapiens")
       
    def test_xmloutput_view(self):
        """
        The generated xml file (xmloutput) is correctly displayed.
        """
        print 'Running %s ...' % getName()
           
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        response = self.client.get(reverse('sequencelistings:xmloutput', args=[self.sequenceListing.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '%s.xml' % self.sequenceListing.fileName)

class ViewsTest(TestCase):
    '''
    Tests for view.py module.
    '''
    @classmethod
    def setUpClass(cls):
        cls.sequenceListingFixture = SequenceListingFixture()
          
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
      
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
 
#     test that a valid seql xml file is generated
    def test_generateXml(self):
        print 'Running %s ...' % getName()
                                   
        f1 = os.path.join(TEST_DATA_DIR_PATH, 'file1.xml')
        f2 = os.path.join(TEST_DATA_DIR_PATH, 'test1.xml')
           
#         self.assertTrue(util.validateDocumentWithSchema1(f, s))
        self.assertFalse(util.validateDocumentWithSchema(f1, util.XML_SCHEMA_PATH))
        self.assertTrue(util.validateDocumentWithSchema(f2, util.XML_SCHEMA_PATH))
#         self.assertTrue(not util.validateDocumentWithSchema(f3, s))
#          
#         self.assertTrue(util.validateDocumentWithDtd(f, d))
        self.assertTrue(util.validateDocumentWithDtd(f1, util.XML_DTD_PATH))
        self.assertTrue(util.validateDocumentWithDtd(f2, util.XML_DTD_PATH))
#         self.assertTrue(not util.validateDocumentWithDtd(f3, d))
    
#     def test_generate_Xml(self):
#         print 'Running %s ...' % getName()
#          
#         s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
#         f1 = self.sequenceListingFixture.create_feature_instance(s1)
#      
#         q1 = self.sequenceListingFixture.create_organism_qualifier_instance(f1)
#         q2 = self.sequenceListingFixture.create_mol_type_qualifier_instance(f1)
#              
#         fileName = views.helper_generateXml(self.sequenceListing)
#        
#         f =  os.path.join(self.dirPath, fileName[1])
# #         TODO: run this only after methods from util are properly tested   
#         self.assertTrue(util.validateDocumentWithSchema(f, self.dtdPath))
#         
#         t2 = Title.objects.create(sequenceListing = sl, 
#                                   inventionTitle = 'efgタンパク質のためのマウスabcd-1遺伝子',
#                                   inventionTitleLanguageCode = 'JA')
#         
#         fileName = views.helper_generateXml(sl)
#      
#         s = 'static/sequencelistings/st26.xsd'
#         f =  'static/%s' % fileName
#            
#         self.assertTrue(util.validateDocumentWithSchema(f, s))


class XmlTest(TestCase):          
      
    @classmethod
    def setUpClass(cls):
        super(XmlTest, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
           
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
       
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
  
    def test_validateXmlDocument(self):
        print 'Running %s ...' % getName()
                                    
        f1 = os.path.join(TEST_DATA_DIR_PATH, 'file1.xml')
        f2 = os.path.join(TEST_DATA_DIR_PATH, 'test1.xml')
            
#         self.assertTrue(util.validateDocumentWithSchema1(f, s))
        self.assertFalse(util.validateDocumentWithSchema(f1, util.XML_SCHEMA_PATH))
        self.assertTrue(util.validateDocumentWithSchema(f2, util.XML_SCHEMA_PATH))
#         self.assertTrue(not util.validateDocumentWithSchema(f3, s))
#          
#         self.assertTrue(util.validateDocumentWithDtd(f, d))
        self.assertTrue(util.validateDocumentWithDtd(f1, util.XML_DTD_PATH))
        self.assertTrue(util.validateDocumentWithDtd(f2, util.XML_DTD_PATH))
#         self.assertTrue(not util.validateDocumentWithDtd(f3, d))
     
#     def test_generate_Xml(self):
#         print 'Running %s ...' % getName()
#          
#         s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
#         f1 = self.sequenceListingFixture.create_feature_instance(s1)
#      
#         q1 = self.sequenceListingFixture.create_organism_qualifier_instance(f1)
#         q2 = self.sequenceListingFixture.create_mol_type_qualifier_instance(f1)
#              
#         fileName = views.helper_generateXml(self.sequenceListing)
#        
#         f =  os.path.join(self.dirPath, fileName[1])
# #         TODO: run this only after methods from util are properly tested   
#         self.assertTrue(util.validateDocumentWithSchema(f, self.dtdPath))
#         
#         t2 = Title.objects.create(sequenceListing = sl, 
#                                   inventionTitle = 'efgタンパク質のためのマウスabcd-1遺伝子',
#                                   inventionTitleLanguageCode = 'JA')
#         
#         fileName = views.helper_generateXml(sl)
#      
#         s = 'static/sequencelistings/st26.xsd'
#         f =  'static/%s' % fileName
#            
#         self.assertTrue(util.validateDocumentWithSchema(f, s))
 
class UtilTests(TestCase):
    def test_rangeFromString(self):
        """
        Test that range is correctly returned.
        """
        print 'Running %s ...' % getName()
          
        s1 = 'ra(1,11,2)'
        s2 = 'r(1,11,2)'
#         print util.rangeFromString(s2)
        self.assertEqual([1,3,5,7,9], util.rangeFromString(s1))
        self.assertEqual(None, util.rangeFromString(s2))
          
    def test_expandFormula(self):
        """
        Test that a formula of type MARRST(ATWQ)2..9TFSRA is correctly expanded.
        """
        print 'Running %s ...' % getName()
          
        self.assertEqual('abc', util.expandFormula('abc'))
        self.assertEqual('abcddd', util.expandFormula('abc(d)3'))
        self.assertEqual('abcdededede', util.expandFormula('abc(de)4'))
        self.assertEqual('abcdedededefg', util.expandFormula('abc(de)4fg'))
        self.assertEqual('abcdededededede', util.expandFormula('abc(de)2..6'))
        self.assertEqual('abcdedededededefg', util.expandFormula('abc(de)2..6fg'))
        self.assertEqual('ab(c', util.expandFormula('ab(c'))
        self.assertEqual('a(b9c', util.expandFormula('a(b9c'))
 
    def test_validateDocumentWithSchema(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the schema.
        """
        print 'Running %s ...' % getName()
                  
#         valid seql contains the first 2 seqs from f2 - goes via if branch
        f3 = os.path.join(TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithSchema(f3, util.XML_SCHEMA_PATH))
 
#         ApplicantNamex instead of ApplicantName - goes to except branch
        f4 = os.path.join(TEST_DATA_DIR_PATH, 'test4.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f4, util.XML_SCHEMA_PATH))
 
#         SOURCxE instead of SOURCE - goes to else branch 
        f5 = os.path.join(TEST_DATA_DIR_PATH, 'test5.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f5, util.XML_SCHEMA_PATH))
 
 
#         supplementary test with seql with more sequences
#         valid seql 20 sequences
        f2 = os.path.join(TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithSchema(f2, util.XML_SCHEMA_PATH))
     
class FormsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(FormsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
           
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
           
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
       
    def test_qualifierForm(self):
        """
        Test the qualifier form.
        """
        print 'Running %s ...' % getName()
           
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f1 = self.sequenceListingFixture.create_feature_instance(s1)
              
        qf1 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'note',
                                  'qualifierValue':'test for value'})
            
        self.assertTrue(qf1.is_valid())
        self.assertEqual('note', qf1.cleaned_data['qualifierName'])  
           
        qf2 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'xxx',
                                  'qualifierValue':'test for xxx value'})
            
        self.assertTrue(qf2.is_valid())
   
class HomeTestCase(StaticLiveServerTestCase):
       
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.selenium.maximize_window()
        self._screenshot_number=1
        super(HomeTestCase, self).setUp() 
           
    def tearDown(self):
        self.selenium.quit()
        super(HomeTestCase, self).tearDown()
           
    def get(self, relative_url):
        self.selenium.get('%s%s' % (self.live_server_url, relative_url))
        self.screenshot()
    
    def screenshot(self):
        print 'Running %s ...' % getName() 
        if hasattr(self, 'sauce_user_name'):
            # Sauce Labs is taking screenshots for us
            return
        name = '%s_%d.png' % (self._testMethodName, self._screenshot_number)
        path = os.path.join(util.SCREENSHOT_DIR, name)
        self.selenium.get_screenshot_as_file(path)
        self._screenshot_number += 1   
           
    def test_check_pages(self):
        print 'Running %s ...' % self._testMethodName
        self.get('/sequencelistings/')
        self.assertIn('st26proto - Index', self.selenium.title)
            
        self.get('/sequencelistings/about')
        self.assertIn('st26proto - About', self.selenium.title)
           
    def test_register(self):
        print 'Running %s ...' % self._testMethodName
           
        self.get('/accounts/register/')
        username = self.selenium.find_element_by_id('id_username')
        email = self.selenium.find_element_by_id('id_email')
        password1 = self.selenium.find_element_by_id('id_password1')
        password2 = self.selenium.find_element_by_id('id_password2')
           
        username.send_keys('user20')
        email.send_keys('user20@email.com')
        password1.send_keys('password20')
        password2.send_keys('password20')
        self.screenshot()
#         self.selenium.find_element_by_xpath('//input[@value="Submit"]').click()
        self.selenium.find_element_by_class_name("btn").click()
        self.get('/sequencelistings/')
        self.assertIn('st26proto - Index', self.selenium.title)
           
        self.assertIn('user20', self.selenium.find_element_by_class_name('page-header').text)
