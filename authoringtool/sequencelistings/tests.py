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
# import logging

# TODO: revive logging whenever necessary
# logger = logging.getLogger(__name__)
# logger.info('TEST start.')

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
        seq = Sequence.objects.create(
                    sequenceListing = sl,
                    moltype = 'DNA',
                    residues = 'catcatcatcatcatcat')

        views.feature_source_helper(seq, 'Homo sapiens')
        
        return seq 
 
class IndexViewNoSequenceListingTest(TestCase):
    def test_index_view_with_no_sequencelistings(self):
        """
        If no sequence listings exist, an appropriate message should be displayed 
        on index page.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No sequence listings are available.")
        self.assertContains(response, "sequencelistings/output/resources/style.css")
        self.assertQuerysetEqual(response.context['sequencelistings'], [])
              
class ViewsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ViewsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
            
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
                      
    def test_index_view_with_one_sequencelisting(self):
        """
        The index page displays one sequence listing.
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
        response = self.client.get(reverse('sequencelistings:detail', args=[self.sequenceListing.pk]))
#         print response
        self.assertContains(response, "location")
        self.assertContains(response, "Generate XML")
        self.assertContains(response, "source")
        self.assertContains(response, "organism")
        self.assertContains(response, "Homo sapiens")
         
#         if the user is logged in: TODO: see what is this?
#         self.assertContains(response, "Add new sequence")
               
    def test_detail_view_after_add_sequence(self):
        """
        The sequence listing detail page, displays the generated sequences.
        """
        print 'Running %s ...' % getName()
              
        self.assertEqual(0, self.sequenceListing.sequenceTotalQuantity)
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
              
        self.assertEqual(1, self.sequenceListing.sequenceTotalQuantity)
#         check however that the sequence has been correctly created
        self.assertEqual(1, s1.sequenceIdNo)
        self.assertEqual('catcatcatcatcatcat', s1.residues)
         
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "18")
        self.assertContains(response, "catcatcatcatcatcat")
#         create another sequence      
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
            
    def test_detail_view_after_add_feature(self):
        """
        The sequence listing detail page displays correctly the generated feature.
        """
        print 'Running %s ...' % getName()
              
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f = s1.feature_set.all()
        self.assertEqual(1, len(f), 'Expected 1 feature.')
          
#         create feature
        f2 = Feature.objects.create(sequence=s1, 
                                    featureKey='allele', 
                                    location='4')
        self.assertEqual('allele', f2.featureKey)
        self.assertEqual('4', f2.location)
               
        f = s1.feature_set.all()
        self.assertEqual(2, len(f), 'Expected 2 features.')
        self.assertEqual('source', f[0].featureKey)
               
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "source")
        self.assertContains(response, "1..18")
        self.assertContains(response, "allele")
        self.assertContains(response, "4")
      
    def test_detail_view_after_add_qualifier(self):
        """
        The sequence listing detail page displays correctly the generated qualifier.
        """
        print 'Running %s ...' % getName()
              
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
          
        f1 = Feature.objects.create(sequence=s1, 
                                    featureKey='modified_base', 
                                    location='7')
        q1 = Qualifier.objects.create(feature=f1, 
                                    qualifierName='note', 
                                    qualifierValue='test for note')
               
        self.assertEqual('note', q1.qualifierName)
        self.assertEqual('test for note', q1.qualifierValue)
         
        response = self.client.get(reverse('sequencelistings:detail', args=[1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "note")
        self.assertContains(response, "test for note")
 
#     TODO: status code is 302 instead of 200. why????
#     def test_add_sequencelisting_view(self):
#         """
#         The form add_sequencelisting is correctly displayed.
#         """
#         print 'Running %s ...' % getName()
#         response = self.client.get(reverse('sequencelistings:add_sequencelisting'))
#         print 'response:', response
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "Create a sequence listing")
#         self.assertContains(response, "File name:")
 
    def test_add_seq_view(self):
        """
        The form add_seq is correctly displayed.
        """
        print 'Running %s ...' % getName()
        response = self.client.get(reverse('sequencelistings:add_seq', args=[1]))
#         print 'response:', response
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
        self.assertContains(response, "Submit")
        
    def test_edit_feature_view(self):
        """
        The form edit_feature is correctly displayed.
        """
        print 'Running %s ...' % getName()
        s = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        f = Feature.objects.create(sequence=s, 
                                    featureKey='modified_base', 
                                    location='7')
        response = self.client.get(reverse('sequencelistings:edit_feature', args=[self.sequenceListing.id, s.id, f.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feature key")
        self.assertContains(response, "7")
        self.assertContains(response, "Update")
        
    def test_add_qualifier_view(self):
        """
        The form add_qualifier is correctly displayed.
        """
        print 'Running %s ...' % getName()
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        response = self.client.get(reverse('sequencelistings:add_qualifier', args=[1, 1, 1]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Feature: source at location 1..")
        self.assertContains(response, "Qualifier name:")
        self.assertContains(response, "Qualifier value:")
         
    def test_xmloutput_view(self):
        """
        The generated xml file (xmloutput) is correctly displayed.
        """
        print 'Running %s ...' % getName()
             
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        response = self.client.get(reverse('sequencelistings:xmloutput', args=[self.sequenceListing.pk, ]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '%s.xml' % self.sequenceListing.fileName)
         
    def test_about_view(self):
        """
        The about_view page is correctly displayed.
        """
        print 'Running %s ...' % getName()
             
        self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)
        response = self.client.get(reverse('sequencelistings:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
        self.assertContains(response, 'only for information purposes')
 
class ModelsTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super(ModelsTests, cls).setUpClass()
        cls.sequenceListingFixture = SequenceListingFixture()
            
    def setUp(self):
        self.sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
        
    def tearDown(self):
        TestCase.tearDown(self)
        self.sequenceListing.delete()
                      
    def test_getOrganism(self):
        """
        Test that the Sequence object returns correctly the organism value.
        """
        print 'Running %s ...' % getName()
              
        s1 = self.sequenceListingFixture.create_sequence_instance(self.sequenceListing)             
        self.assertEqual('Homo sapiens', s1.getOrganism())
                
        s2 = Sequence.objects.create(
                sequenceListing = self.sequenceListing,
                moltype = 'AA',
                residues = 'MRTAVTAD')
        self.assertEqual(None, s2.getOrganism())
         
        views.feature_source_helper(s2, 'Drosophila melanogaster')
        self.assertEqual('Drosophila melanogaster', s2.getOrganism())
                       
        s3 = Sequence.objects.create(
            sequenceListing = self.sequenceListing,
            moltype = 'RNA',
            residues = 'caucaucaucaucaucau')
         
        views.feature_source_helper(s3, 'Mus musculus')
        self.assertEqual('Mus musculus', s3.getOrganism())

class UtilTests(TestCase):
    def setUp(self):
        self.sequenceListingFixture = SequenceListingFixture()
       
    def tearDown(self):
        TestCase.tearDown(self)
    
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
  
    def test_helper_generateXml(self):
        print 'Running %s ...' % getName()
        
        sequenceListing = self.sequenceListingFixture.create_sequencelisting_instance()
        self.sequenceListingFixture.create_sequence_instance(sequenceListing)
#         TODO: generate some fancy sequences to check xml validation?
        util.helper_generateXml(sequenceListing)
        
        f =  os.path.join(util.OUTPUT_DIR, '%s.xml' % sequenceListing.fileName)

        self.assertTrue(util.validateDocumentWithSchema(f, util.XML_SCHEMA_PATH))
        self.assertTrue(util.validateDocumentWithDtd(f, util.XML_DTD_PATH))
        sequenceListing.delete()

    def test_validateDocumentWithSchema(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the schema.
        """
        print 'Running %s ...' % getName()
                   
#         valid seql contains the first 2 seqs from f2 - goes via if branch
        f3 = os.path.join(util.TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithSchema(f3, util.XML_SCHEMA_PATH))
  
#         ApplicantNamex instead of ApplicantName - goes to except branch
        f4 = os.path.join(util.TEST_DATA_DIR_PATH, 'test4.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f4, util.XML_SCHEMA_PATH))
  
#         SOURCxE instead of SOURCE - goes to else branch 
        f5 = os.path.join(util.TEST_DATA_DIR_PATH, 'test5.xml')        
        self.assertFalse(util.validateDocumentWithSchema(f5, util.XML_SCHEMA_PATH))
 
#         supplementary test with seql with more sequences
#         valid seql 20 sequences
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithSchema(f2, util.XML_SCHEMA_PATH))

#         SequenceTotalQuantity element is missing
# TODO: the error msg says that EarliestPriorityApplicationIdentification is expected: /Users/ad/pyton/projects/st26proto/authoringtool/sequencelistings/testData/test8.xml:42:0:ERROR:SCHEMASV:SCHEMAV_ELEMENT_CONTENT: Element 'SequenceData': This element is not expected. Expected is ( EarliestPriorityApplicationIdentification ).
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithSchema(f8, util.XML_SCHEMA_PATH))
      
    def test_validateDocumentWithDtd(self):
        """
        Test that xml sequence listing files are correctly validated 
        against the dtd.
        """
        print 'Running %s ...' % getName()
                   
#         valid seql contains the first 2 seqs from f2
        f3 = os.path.join(util.TEST_DATA_DIR_PATH, 'test3.xml')
        self.assertTrue(util.validateDocumentWithDtd(f3, util.XML_DTD_PATH))
        
#         SOURCxE instead of SOURCE. It passes the validation bc there is no
#         restriction defined in dtd on the value of an element
        f5 = os.path.join(util.TEST_DATA_DIR_PATH, 'test5.xml')        
        self.assertTrue(util.validateDocumentWithDtd(f5, util.XML_DTD_PATH))
        
#         supplementary test with seql with more sequences
#         valid seql 20 sequences
        f2 = os.path.join(util.TEST_DATA_DIR_PATH, 'test2.xml')
        self.assertTrue(util.validateDocumentWithDtd(f2, util.XML_DTD_PATH))
        
#         ApplicantNamey instead of ApplicantName - except branch
        f6 = os.path.join(util.TEST_DATA_DIR_PATH, 'test6.xml')
        self.assertFalse(util.validateDocumentWithDtd(f6, util.XML_DTD_PATH))

#         ApplicantsName open and closing tags instead of ApplicantName - else branch
        f7 = os.path.join(util.TEST_DATA_DIR_PATH, 'test7.xml')
        self.assertFalse(util.validateDocumentWithDtd(f7, util.XML_DTD_PATH))
        
#         SequenceTotalQuantity element is missing
        f8 = os.path.join(util.TEST_DATA_DIR_PATH, 'test8.xml')
        self.assertFalse(util.validateDocumentWithDtd(f8, util.XML_DTD_PATH))
        
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
  
        f1 = Feature.objects.create(sequence=s1, 
                                    featureKey='modified_base', 
                                    location='7')
        qf1 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'note',
                                  'qualifierValue':'test for value'})
              
        self.assertTrue(qf1.is_valid())
        self.assertEqual('note', qf1.cleaned_data['qualifierName'])  
             
        qf2 = QualifierForm(feature=f1, 
                            data={'qualifierName': 'xxx',
                                  'qualifierValue':'test for xxx value'})
              
        self.assertTrue(qf2.is_valid())
        