'''
Created on Jul 12, 2016

@author: ad
'''
import unittest
import os 
from django.conf import settings 
from size_estimation import RawSequenceListing

class Test(unittest.TestCase):
    def setUp(self):
        self.f5 = os.path.join(settings.BASE_DIR, 'seql_converter', 
                            'st25parser', 'testData', 'file5.txt')
        self.sl5 = RawSequenceListing(self.f5)

    def testRawSequenceListing(self):
        reference_exp = """<130>  BIOA-006/01WO\r\n\r\n"""
        self.assertEqual(reference_exp, self.sl5.reference)
        self.assertEqual(None, self.sl5.applicationNumber)
        self.assertEqual(None, self.sl5.filingDate)
        
        priorities_exp = '<150>  US 61/677,959\r\n<151>  2012-07-31\r\n\r\n'
        self.assertEqual(priorities_exp, self.sl5.priorities)
        
        self.assertEqual(40, len(self.sl5.sequences))
        
        organism1_exp = '<213>  Homo sapiens\r\n\r\n'
        self.assertEqual(organism1_exp, self.sl5.sequences[0].organism)
        
        organism40_exp = '<213>  Chloroflexus aurantiacus\r\n\r\n'
        self.assertEqual(organism40_exp, self.sl5.sequences[39].organism)
        
        self.assertFalse(self.sl5.sequences[0].features)
        
        features4 = self.sl5.sequences[3].features
        
        self.assertEqual(6, len(features4))
        
        self.assertEqual('<220>\r\n', features4[0].featureHeader)
        self.assertEqual(None, features4[0].key)
        self.assertEqual(None, features4[0].location)
        self.assertEqual('<223>  Sulfatase motif\r\n\r\n\r\n', features4[0].description)
        
        self.assertEqual('<220>\r\n', features4[5].featureHeader)
        self.assertEqual('<221>  MISC_FEATURE\r\n', features4[5].key)
        self.assertEqual('<222>  (5)..(5)\r\n', features4[5].location)
        self.assertEqual('<223>  Xaa = Any amino acid\r\n\r\n', features4[5].description)
        
         
        residues40_exp = '<400>  40\r\n\r\nMet Ser Gly Thr Gly Arg Leu Ala Gly Lys Ile Ala Leu Ile Thr Gly \r\n1               5                   10                  15      \r\n\r\n\r\nGly Ala Gly Asn Ile Gly Ser Glu Leu Thr Arg Arg Phe \r\n            20                  25         \r\n'
        
        self.assertEqual(residues40_exp, self.sl5.sequences[39].residues)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()