'''
Created on Jul 2, 2016

@author: ad
'''
import unittest
import os 
from converter import St25To26Converter 

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

class Test_St25To26Converter(unittest.TestCase):


    def setUp(self):
        pass


    def tearDown(self):
        pass

    @withMethodName
    def test_init(self):
        fp = os.path.join('test', 'testdata', 'WO2013041670.txt')
        sc = St25To26Converter(fp)
        
        self.assertEqual('WO2013041670', sc.fileName)


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()