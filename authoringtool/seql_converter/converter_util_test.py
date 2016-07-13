'''
Created on Jul 2, 2016

@author: ad
'''
import unittest
import converter_util as cu 

class TestConverterUtil(unittest.TestCase):

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

    def test_getSt26ElementNames(self):
#         self.assertEqual(x, (cu.ELEMENT_NAME_ST26))
        self.assertIn('ST26SequenceListing', cu.TAG_LENGTH_ST26.keys())
        self.assertIn('ApplicantFileReference', cu.TAG_LENGTH_ST26.keys())
        self.assertIn('INSDQualifier_value', cu.TAG_LENGTH_ST26.keys())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()