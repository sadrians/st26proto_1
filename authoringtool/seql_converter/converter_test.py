'''
Created on Jul 2, 2016

@author: ad
'''
from django.test import TestCase
import os 
from django.conf import settings 
from converter import St25To26Converter 
import sequencelistings.util as slsu

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

class Test_St25To26Converter(TestCase):
    @classmethod
    def getAbsPath(cls, aFileName):
        return os.path.join(settings.BASE_DIR, 'seql_converter', 
                            'st25parser', 'testData', aFileName)
 
    def setUp(self):
        self.f1 = self.getAbsPath('file1.txt')
        self.f33_1 = self.getAbsPath('file33_1.txt')
        self.f80 = self.getAbsPath('file80.txt')
         
        self.sc1 = St25To26Converter(self.f1)
        self.sc33_1 = St25To26Converter(self.f33_1)
        self.sc80 = St25To26Converter(self.f80) 
 
    def tearDown(self):
        pass
 
    @withMethodName
    def test_getSequenceListingSt26(self):
         
        self.assertEqual('file1', self.sc1.fileName)
         
        self.assertEqual('file1_converted', self.sc1.seql_st26.fileName)
        self.assertEqual('34246761601', self.sc1.seql_st26.applicantFileReference)
         
        self.assertEqual('XX', self.sc1.seql_st26.IPOfficeCode)
        self.assertEqual('61536464', self.sc1.seql_st26.applicationNumberText)
         
        self.assertEqual('XX', self.sc80.seql_st26.IPOfficeCode)
        self.assertEqual('Not yet assigned', self.sc80.seql_st26.applicationNumberText)
         
        self.assertEqual(2012, self.sc1.seql_st26.filingDate.year)
        self.assertEqual(9, self.sc1.seql_st26.filingDate.month)
        self.assertEqual(19, self.sc1.seql_st26.filingDate.day)
        
        self.assertEqual(1900, self.sc33_1.seql_st26.filingDate.year)
        self.assertEqual(1, self.sc33_1.seql_st26.filingDate.month)
        self.assertEqual(1, self.sc33_1.seql_st26.filingDate.day)
         
        self.assertEqual('XX', self.sc1.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61536558 - prio1', self.sc1.seql_st26.earliestPriorityApplicationNumberText)
         
        self.assertEqual('US', self.sc80.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61/678,367', self.sc80.seql_st26.earliestPriorityApplicationNumberText)
         
        self.assertEqual(2001, self.sc1.seql_st26.earliestPriorityFilingDate.year)
        self.assertEqual(1, self.sc1.seql_st26.earliestPriorityFilingDate.month)
        self.assertEqual(1, self.sc1.seql_st26.earliestPriorityFilingDate.day)
 
        self.assertEqual('OPX Biotechnologies, Inc.', self.sc1.seql_st26.applicantName)
        self.assertEqual('XX', self.sc1.seql_st26.applicantNameLanguageCode)
        self.assertEqual('OPX Biotechnologies, Inc.', self.sc1.seql_st26.applicantNameLatin)
 
        self.assertEqual(4, self.sc1.seql_st26.sequenceTotalQuantity)
         
    @withMethodName
    def test_setTitleSt26(self):
        t = self.sc1.seql_st26.title_set.all()[0]
        self.assertEqual('COMPOSITIONS AND METHODS REGARDING DIRECT NADH UTILIZATION TO PRODUCE 3-HYDROXYPROPIONIC ACID AND RELATED CHEMICALS AND PRODUCTS', 
                         t.inventionTitle)
        self.assertEqual('XX', t.inventionTitleLanguageCode)
         
    @withMethodName
    def test_setSequencesSt26(self):
 
        sequences = self.sc1.seql_st26.sequence_set.all()
        self.assertEqual(4, sequences.count())
         
        s2 = sequences.get(sequenceIdNo=2)
        s4 = sequences.get(sequenceIdNo=4)
         
        self.assertEqual('DNA', s2.moltype)
        self.assertEqual('AA', s4.moltype)
         
        self.assertEqual('ttgaccaagctggggaccccggtcccttgggaccagtggcagaggagtc', s2.residues)
         
        features_s2 = s2.feature_set.all()
         
        self.assertEqual("3'clip", features_s2[1].featureKey)
        self.assertEqual("1..30", features_s2[1].location)
         
    @withMethodName
    def test_generateXmlFile(self):
        od = os.path.join(settings.BASE_DIR, 'seql_converter', 'test', 'output')
         
        self.sc1.generateXmlFile(od)
        filePath1 = os.path.join(od, '%s.xml' % self.sc1.seql_st26.fileName)
         
        self.assertTrue(os.path.isfile(filePath1))
        self.assertTrue(slsu.validateDocumentWithDtd(filePath1, slsu.XML_DTD_PATH))

#         self.assertTrue(slsu.validateDocumentWithSchema(filePath1, slsu.XML_SCHEMA_PATH))
