'''
Created on Jul 2, 2016

@author: ad
'''
import unittest
import os 
from django.conf import settings 
from converter import St25To26Converter 

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

class Test_St25To26Converter(unittest.TestCase):
    @classmethod
    def getAbsPath(cls, aFileName):
        return os.path.join(settings.BASE_DIR, 'seql_converter', 
                            'st25parser', 'testData', aFileName)

    def setUp(self):
        self.f1 = self.getAbsPath('file1.txt')
        self.f80 = self.getAbsPath('file80.txt')

    def tearDown(self):
        pass

    @withMethodName
    def test_init(self):
        sc = St25To26Converter(self.f1)
        sc80 = St25To26Converter(self.f80)
        
        self.assertEqual('file1', sc.fileName)
        
        self.assertEqual('file1', sc.seql_st26.fileName)
        self.assertEqual('34246761601', sc.seql_st26.applicantFileReference)
        
        self.assertEqual('XX', sc.seql_st26.IPOfficeCode)
        self.assertEqual('61536464', sc.seql_st26.applicationNumberText)
        
        self.assertEqual('XX', sc80.seql_st26.IPOfficeCode)
        self.assertEqual('Not yet assigned', sc80.seql_st26.applicationNumberText)
        
        self.assertEqual(2012, sc.seql_st26.filingDate.year)
        self.assertEqual(9, sc.seql_st26.filingDate.month)
        self.assertEqual(19, sc.seql_st26.filingDate.day)
        
        self.assertEqual('XX', sc.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61536558 - prio1', sc.seql_st26.earliestPriorityApplicationNumberText)
        
        self.assertEqual('US', sc80.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61/678,367', sc80.seql_st26.earliestPriorityApplicationNumberText)
        
        self.assertEqual(2001, sc.seql_st26.earliestPriorityFilingDate.year)
        self.assertEqual(1, sc.seql_st26.earliestPriorityFilingDate.month)
        self.assertEqual(1, sc.seql_st26.earliestPriorityFilingDate.day)

        self.assertEqual('OPX Biotechnologies, Inc.', sc.seql_st26.applicantName)
        self.assertEqual('XX', sc.seql_st26.applicantNameLanguageCode)
        self.assertEqual('OPX Biotechnologies, Inc.', sc.seql_st26.applicantNameLatin)

        self.assertEqual('4', sc.seql_st26.sequenceTotalQuantity)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()