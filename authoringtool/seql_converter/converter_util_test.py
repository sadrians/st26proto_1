'''
Created on Jul 2, 2016

@author: ad
'''
import os 
import django
django.setup()

from django.conf import settings

import unittest
import converter_util as cu 

class TestConverterUtil(unittest.TestCase):
    def test_safeLength(self):
        self.assertEqual(0, cu.safeLength(None))
        self.assertEqual(3, cu.safeLength('abc'))
        self.assertEqual(20, cu.safeLength('<400>  40\r\n\r\nMet Ser'))

    def test_applicationNumberAsTuple(self):
        an1 = 'EP12345'
        an2 = '12345'
        an3 = 'PCT/GB2016/12345'
        an4 = 'us - 12345'
        an5 = 'US 61/678,367'
        an6 = 'EP 12005594.2'
        
        self.assertEqual(('EP', '12345'), cu.applicationNumberAsTuple(an1))
        self.assertEqual(('XX', '12345'), cu.applicationNumberAsTuple(an2))
        self.assertEqual(('PC', 'T/GB2016/12345'), cu.applicationNumberAsTuple(an3))
        self.assertEqual(('us', '- 12345'), cu.applicationNumberAsTuple(an4))
        self.assertEqual(('US', '61/678,367'), cu.applicationNumberAsTuple(an5))
        self.assertEqual(('EP', '12005594.2'), cu.applicationNumberAsTuple(an6))

    def test_setSt26ElementNames(self):
        self.assertIn('ST26SequenceListing', cu.TAG_LENGTH_ST26.keys())
        self.assertIn('ApplicantFileReference', cu.TAG_LENGTH_ST26.keys())
        self.assertIn('INSDQualifier_value', cu.TAG_LENGTH_ST26.keys())
        
        self.assertEqual(43, cu.TAG_LENGTH_ST26['ST26SequenceListing'])
        self.assertEqual(47, cu.TAG_LENGTH_ST26['INSDSeq_feature-table'])
        self.assertEqual(20, cu.TAG_LENGTH_ST26['sequenceIDNumber'])
        
    def test_getNumberOfCharsFromFile(self):
        f1004 = os.path.join(settings.BASE_DIR, 'seql_converter', 
                            'st25parser', 'testData', 'WO2012-001004-001.zip.txt')
#         cu.getNumberOfCharsFromFile(f1004)
        
        self.assertEqual(21983 + 670, cu.getNumberOfCharsFromFile(f1004))
        
    def test_getMarkupLength(self):
        s1 = '<abc>def</abc>'
        s2 = '<abc attr1="1" attr2="2">def</abc>'
        s3 = '<abc>def</abc><ghi attr="1">jkl</ghi>'
        
        
        
        self.assertEqual(11, cu.getMarkupLength(s1))
        self.assertEqual(31, cu.getMarkupLength(s2))
        self.assertEqual(31, cu.getMarkupLength(s3))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()