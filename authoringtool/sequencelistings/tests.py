#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.test import TestCase, LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.core.urlresolvers import reverse
from models import SequenceListing, Title, Sequence, Feature, Qualifier
from forms import QualifierForm
 
from django.utils import timezone
import util 
# import views
# 
import inspect 
import os

from selenium import webdriver 

def getName():
    return inspect.stack()[1][3]

def create_sequencelisting_instance():
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
    create_title_instance(sl)
    
    return sl 
 
def create_title_instance(sl):
    return Title.objects.create(
                sequenceListing = sl,
                inventionTitle = 'Invention 1',
                inventionTitleLanguageCode = 'EN')
 
def create_sequence_instance(sl):
    return Sequence.objects.create(
                sequenceListing = sl,
#                 length = '29',
                moltype = 'DNA',
                residues = 'catcatcatcatcatcat')
 
def create_feature_instance(s):
    return Feature.objects.create(sequence=s, 
                                  featureKey='source', 
                                  location='1..%s' % s.length)
 
def create_organism_qualifier_instance(sourceFeature):
    return Qualifier.objects.create(feature=sourceFeature, 
                                  qualifierName='organism', 
                                  qualifierValue='Homo sapiens')
  
def create_mol_type_qualifier_instance(sourceFeature):
    return Qualifier.objects.create(feature=sourceFeature, 
                                  qualifierName='mol_type', 
                                  qualifierValue='genomic DNA')
 
class SequenceListingViewTests(TestCase):
    
    def test_index_view_with_no_sequencelistings(self):
        """
        If no sequence listings exist, an appropriate message should be displayed.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sequence listings are available.")
        self.assertQuerysetEqual(response.context['sequencelistings'], [])
         
    def test_index_view_with_one_sequencelisting(self):
        """
        The sequence listings index, displays one sequence listing.
        """
        print 'Running %s ...' % getName()
        sl = create_sequencelisting_instance()
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
        sl1 = create_sequencelisting_instance()
        response = self.client.get(reverse('sequencelistings:detail', args=[sl1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test_xmlsql")
        self.assertContains(response, "2015123456")
        self.assertEqual(response.context['sequencelisting'], sl1)
#         there are no sequences created yet:
        self.assertFalse(response.context['sequencelisting'].sequence_set.all())
#         now a sequence is created
        s1 = create_sequence_instance(sl1)
        self.assertTrue(response.context['sequencelisting'].sequence_set.all())
        create_feature_instance(s1)
        response = self.client.get(reverse('sequencelistings:detail', args=[sl1.pk]))
#         print response
        self.assertContains(response, "location")
        self.assertContains(response, "Generate XML")
#         if the user is logged in:
#         self.assertContains(response, "Add new sequence")
          
    def test_add_seq_view(self):
        """
        The form add_seq is correctly displayed.
        """
        print 'Running %s ...' % getName()
        sl = create_sequencelisting_instance()
        response = self.client.get(reverse('sequencelistings:add_seq', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Molecule type")
        self.assertContains(response, "Residues")
          
    def test_add_feature_view(self):
        """
        The form add_feature is correctly displayed.
        """
        print 'Running %s ...' % getName()
        
        sl = create_sequencelisting_instance()
        create_sequence_instance(sl)
        response = self.client.get(reverse('sequencelistings:add_feature', args=[1, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feature key")
     
    def test_createSequence(self):
        """
        The sequence listing detail page, displays the generated sequences.
        """
        print 'Running %s ...' % getName()
        
        sl = create_sequencelisting_instance()
        self.assertEqual(0, sl.sequenceTotalQuantity)
        s1 = create_sequence_instance(sl)
        
#         print s1.inspectSequence()
  
        self.assertEqual(1, sl.sequenceTotalQuantity)
        self.assertEqual(1, s1.sequenceIdNo)
        self.assertEqual('catcatcatcatcatcat', s1.residues)
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
          
        s2 = Sequence.objects.create(
            sequenceListing = sl,
            moltype = 'RNA',
            residues = 'caucaucaucaucaucaucc')
          
        self.assertEqual(2, sl.sequenceTotalQuantity)
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
        self.assertContains(response, "20")
        self.assertContains(response, "RNA")
  
    def test_getOrganism(self):
        """
        xxxxTest that the Sequence object returns correctly the organism value.
        """
        print 'Running %s ...' % getName()
        
        sl = create_sequencelisting_instance()
        s1 = create_sequence_instance(sl)
         
        self.assertEqual(None, s1.getOrganism())
         
        f1 = create_feature_instance(s1)
         
        self.assertEqual(None, s1.getOrganism())
         
        create_organism_qualifier_instance(f1)
         
        self.assertEqual('Homo sapiens', s1.getOrganism())
         
        s2 = Sequence.objects.create(
                sequenceListing = sl,
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
            sequenceListing = sl,
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
        xxxxThe sequence listing detail page, displays the generated feature.
        """
        print 'Running %s ...' % getName()
        
        sl = create_sequencelisting_instance()
        s1 = create_sequence_instance(sl)
          
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
        
        sl = create_sequencelisting_instance()
        s1 = create_sequence_instance(sl)
        f1 = create_feature_instance(s1)
  
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
        sl = create_sequencelisting_instance()
        create_sequence_instance(sl)
        response = self.client.get(reverse('sequencelistings:xmloutput', args=[sl.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '%s.xml' % sl.fileName)
           
#     def test_validateXmlDocument(self):
#         s = 'static/sequencelistings/st26.xsd'
#         d ='static/sequencelistings/ST26SequenceListing_V1_0.dtd'
#          
#         f = 'static/sequencelistings/example.xml'
#         f1 = 'static/sequencelistings/example1.xml'
#         f2 = 'static/sequencelistings/example2.xml'
#         f3 = 'static/sequencelistings/example3.xml'
#          
#         self.assertTrue(util.validateDocumentWithSchema(f, s))
#         self.assertTrue(util.validateDocumentWithSchema(f1, s))
#         self.assertTrue(util.validateDocumentWithSchema(f2, s))
#         self.assertTrue(not util.validateDocumentWithSchema(f3, s))
#          
#         self.assertTrue(util.validateDocumentWithDtd(f, d))
#         self.assertTrue(util.validateDocumentWithDtd(f1, d))
#         self.assertTrue(util.validateDocumentWithDtd(f2, d))
#         self.assertTrue(not util.validateDocumentWithDtd(f3, d))
#      
#     def test_generate_Xml(self):
#         sl = create_sequencelisting_instance()
#         create_title_instance(sl)
#         s1 = create_sequence_instance(sl)
#         f1 = create_feature_instance(s1)
#    
#         q1 = create_organism_qualifier_instance(f1)
#         q2 = create_mol_type_qualifier_instance(f1)
#            
#         fileName = views.helper_generateXml(sl)
#      
#         s = 'static/sequencelistings/st26.xsd'
#         f =  'static/%s' % fileName
#            
#         self.assertTrue(util.validateDocumentWithSchema(f, s))
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
#         

class UtilTests(TestCase):
    def test_rangeFromString(self):
        """
        Test that range is correctly returned.
        """
        s1 = 'ra(1,11,2)'
        s2 = 'r(1,11,2)'
#         print util.rangeFromString(s2)
        self.assertEqual([1,3,5,7,9], util.rangeFromString(s1))
        self.assertEqual(None, util.rangeFromString(s2))
        
    def test_expandFormula(self):
        """
        Test that a formula of type MARRST(ATWQ)2..9TFSRA is correctly expanded.
        """
        self.assertEqual('abc', util.expandFormula('abc'))
        self.assertEqual('abcddd', util.expandFormula('abc(d)3'))
        self.assertEqual('abcdededede', util.expandFormula('abc(de)4'))
        self.assertEqual('abcdedededefg', util.expandFormula('abc(de)4fg'))
        self.assertEqual('abcdededededede', util.expandFormula('abc(de)2..6'))
        self.assertEqual('abcdedededededefg', util.expandFormula('abc(de)2..6fg'))
        self.assertEqual('ab(c', util.expandFormula('ab(c'))
        self.assertEqual('a(b9c', util.expandFormula('a(b9c'))

class FormsTests(TestCase):
         
    def test_qualifierForm(self):
        """
        Test the qualifier form.
        """
        sl = create_sequencelisting_instance()
        s1 = create_sequence_instance(sl)
        f1 = create_feature_instance(s1)
  
#         q1 = Qualifier.objects.create(feature=f1, 
#                                       qualifierName='organism', 
#                                       qualifierValue='Homo sapiens')
         
        qf1 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'note',
                                  'qualifierValue':'test for value'})
         
        self.assertTrue(qf1.is_valid())
        self.assertEqual('note', qf1.cleaned_data['qualifierName'])      

SCREENSHOT_DIR = os.path.join(util.PROJECT_DIRECTORY, 'sequencelistings', 'static', 'screenshots')
# class HomeTestCase(LiveServerTestCase):
class HomeTestCase(StaticLiveServerTestCase):
#     def __init__(self):
#         self._screenshot_number=1
    
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
        if hasattr(self, 'sauce_user_name'):
            # Sauce Labs is taking screenshots for us
            return
        name = '%s_%d.png' % (self._testMethodName, self._screenshot_number)
        path = os.path.join(SCREENSHOT_DIR, name)
#         path = 'selenium_screenshot.png'
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
    
