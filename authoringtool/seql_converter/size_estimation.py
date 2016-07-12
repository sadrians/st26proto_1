'''
Created on Jul 12, 2016

@author: ad
'''
import os 
import re 
import pprint

from st25parser.seqlparser import SequenceListing  

fp = os.path.join('st25parser', 'testData', 'file1.txt')

def estimate(afp):
    sl = SequenceListing(fp)
    gi = sl.generalInformation 
    
    print gi.applicant
    applicantValueLength = len(gi.applicant[0]) if gi.applicant else 0
    print applicantValueLength

GENERAL_INFORMATION_REGEX = r"""(?P<seqlHeader>[^<]+)(?P<applicant><110>[^<]+)
                (?P<title><120>[^<]+)
                (?P<reference><130>[^<]+)?
                (?P<applicationNumber><140>[^<]+)?
                (?P<filingDate><141>[^<]+)?
                (?P<priorities>(?P<priorityNumber><150>[^<]+)
                (?P<priorityDate><151>[^<]+))*
                (?P<quantity><160>[^<]+)
                (?P<software><170>[^<]+)
                """
 
GENERAL_INFORMATION_PATTERN = re.compile(GENERAL_INFORMATION_REGEX, re.DOTALL | re.VERBOSE)

SEQUENCE_REGEX = r"""
                (?P<seqIdNo><210>[^<]+)
                (?P<length><211>[^<]+)
                (?P<molType><212>[^<]+)
                (?P<organism><213>[^<]+)
                (?P<features><220>.*?)?
                (?P<residues><400>.*)
"""

SEQUENCE_PATTERN = re.compile(SEQUENCE_REGEX, re.DOTALL | re.VERBOSE)

FEATURE_REGEX = r"""
                (?P<featureHeader><220>[^<]+)
                (?P<key><221>[^<]+)?
                (?P<location><222>[^<]+)?
                (?P<description><223>[^<]+)?
"""
FEATURE_PATTERN = re.compile(FEATURE_REGEX, re.DOTALL | re.VERBOSE)

class SequenceListing(object):
    def __init__(self, aFilePath):
        blocks = []
        self.sequences = []
        
        with open(aFilePath, 'r') as f:
            blocks = f.read().split('<210>')
        
    #     pprint.pprint(blocks)    
        m = GENERAL_INFORMATION_PATTERN.match(blocks[0])
          
        if m:
            print 'General information match found.'
            self.seqlHeader = m.group('seqlHeader')
            self.applicant = m.group('applicant')
            self.title = m.group('title')
            self.reference = m.group('reference')
            self.applicationNumber = m.group('applicationNumber')
            self.filingDate = m.group('filingDate')
            self.priorities = m.group('priorities')
            self.quantity = m.group('quantity')
            self.software = m.group('software')
            
        for s in blocks[1:]:
#             print '='*50
            reconstructedString = '<210>%s' %s
            self.sequences.append(Sequence(reconstructedString))
            
    #         print reconstructedString
class Sequence(object):
    def __init__(self, aStr):
        sm = SEQUENCE_PATTERN.match(aStr)
        if sm:
#             print 'Sequence match found.'
            self.seqIdNo = sm.group('seqIdNo')
            self.length = sm.group('length')
            self.molType = sm.group('molType')
            self.organism = sm.group('organism')
            self.features = []
            featuresString = sm.group('features')
            if featuresString:
                reconstructedFeatureString = '<220>%s' % sm.group('features')
                featureMatchers = FEATURE_PATTERN.finditer(reconstructedFeatureString)
                
                for fm in featureMatchers:
                    self.features.append(Feature(fm))

            self.residues = sm.group('residues')

class Feature(object):
    def __init__(self, fm):
        self.featureHeader = fm.group('featureHeader')
        self.key = fm.group('key')
        self.location = fm.group('location')
        self.description = fm.group('description')
 
def getElementSize(aFilePath):
    blocks = []
    
    with open(aFilePath, 'r') as f:
        blocks = f.read().split('<210>')
    
#     pprint.pprint(blocks)    
    m = GENERAL_INFORMATION_PATTERN.match(blocks[0])
      
    if m:
        print 'General information match found.'
        print m.group('seqlHeader')
        print m.group('applicant')
        print m.group('title')
        print m.group('reference')
        print m.group('applicationNumber')
        print m.group('filingDate')
        print m.group('priorities')
        print m.group('quantity')
        print m.group('software')
        
    for s in blocks[1:]:
        print '='*50
        reconstructedString = '<210>%s' %s
#         print reconstructedString
        sm = SEQUENCE_PATTERN.match(reconstructedString)
        if sm:
            print 'Sequence match found.'
            print sm.group('seqIdNo')
            print sm.group('length')
            print sm.group('molType')
            print sm.group('organism')
            featuresString = sm.group('features')
            if featuresString:
                reconstructedFeatureString = '<220>%s' % sm.group('features')
                featureMatchers = FEATURE_PATTERN.finditer(reconstructedFeatureString)
                
                for fm in featureMatchers:
                    print '\t%s' %('&'*50)
                    print fm.group('featureHeader')
                    print fm.group('key')
                    print fm.group('location')
                    print fm.group('description')
#               print sm.group('features')
            print sm.group('residues')


f5 = os.path.join('st25parser', 'testData', 'file5.txt') 
# getElementSize(f5)









# with open(fp, 'r') as f:        
# #         for line in f:
# #             if '<110>' in line:
# #                 print line
# #                 print len(line)
# #                 print len(line.strip())
# #             if 'ACID' in line:
# #                     print line
# #                     print len(line)
# #                     print len(line.strip())
#         for line in [next(f) for i in xrange(10)]:
#             print line
#             print 'length of line is: ', len(line)  
#             i += 1   
# estimate(fp)