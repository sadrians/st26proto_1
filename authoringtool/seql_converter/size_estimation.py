'''
Created on Jul 12, 2016

@author: ad
'''
import os 
import re 
import csv
import pprint
import converter_util as cu 

from django.conf import settings 

import st25parser.seqlparser
from seql_converter.st25parser import seqlparser

# fp = os.path.join('st25parser', 'testData', 'file1.txt')

# pprint.pprint(cu.TAG_LENGTH_ST26)

# def estimate(afp):
#     sl = SequenceListing(fp)
#     gi = sl.generalInformation 
#     
#     print gi.applicant
#     applicantValueLength = len(gi.applicant[0]) if gi.applicant else 0
#     print applicantValueLength

GENERAL_INFORMATION_REGEX = r"""(?P<seqlHeader>[^<]+)
                (?P<applicant><110>[^<]+)
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

def safeLength(aStr):
    if aStr is not None:
        return len(aStr)
    else:
        return 0

def writeSizes(inFile, outFile):
    sl = SequenceListing(inFile)
    slp = st25parser.seqlparser.SequenceListing(inFile)
    
    def getSt25St26Lengths(element_st25, 
                           element_st25_length, 
                           value_st25_length, 
                           element_st26, comment):
        
        return [element_st25, 
                safeLength(element_st25_length), 
                safeLength(value_st25_length),
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26],
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26] + safeLength(value_st25_length),
                element_st26, 
                comment
                ]
        
    
    with open(outFile, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(['element_st25', 'element_st25_length', 'value_st25_length', 
                     'tag_st26_length', 'element_st26_length', 'element_st26', 
                     'comment'])
        
#         currentValueLength = 0
#         currentTag = 'ST26SequenceListing'
#         currentTuple = getSt26Lengths(currentValueLength, currentTag)
#         
#         wr.writerow(['-', 0, currentValueLength, currentTuple[0], currentTuple[1], currentTag])
#                 
        wr.writerow(getSt25St26Lengths(110, 
                                       sl.applicant, 
                                       slp.generalInformation.applicant[0], 
                                       'ApplicantName', '-'))
        wr.writerow(getSt25St26Lengths(120, 
                                       sl.title, 
                                       slp.generalInformation.title, 
                                       'InventionTitle', '-'))
        wr.writerow(getSt25St26Lengths(130, 
                                       sl.reference, 
                                       slp.generalInformation.reference, 
                                       'ApplicantFileReference', '-'))
        wr.writerow(getSt25St26Lengths(140, 
                                       sl.applicationNumber, 
                                       slp.generalInformation.applicationNumber, 
                                       'IPOfficeCode', '-'))
        wr.writerow(getSt25St26Lengths(141, 
                                       sl.filingDate, 
                                       slp.generalInformation.filingDate, 
                                       'FilingDate', '-'))
        
        priority_st25 = slp.generalInformation.priority
        priority_st25_length = sum([len(a[0]) + len(a[1]) for a in priority_st25])
        priorityNumber_length = 0
        priorityDate_length = 0
        if priority_st25:
            priorityNumber_length = safeLength(priority_st25[0][0])
            priorityDate_length = safeLength(priority_st25[0][1])
        
#         wr.writerow(getSt25St26Lengths('prio', 
#                                         priority_st25_length, 
#                                         priorityNumber_length + priorityDate_length, 
#                                         'EarliestPriorityApplicationIdentification'))
#         wr.writerow(getSt25St26Lengths(151, 
#                                        sl., 
#                                        slp.generalInformation., 
#                                        ''))
        
        wr.writerow(getSt25St26Lengths(160, 
                                       sl.quantity, 
                                       slp.generalInformation.quantity, 
                                       'SequenceTotalQuantity', '-'))
        wr.writerow(getSt25St26Lengths(170, 
                                       sl.software, 
                                       slp.generalInformation.software, 
                                       '-', 'Discarded in ST.26'))
        
        parsedSequences = []
        for s in slp.generateSequence():
            parsedSequences.append(s)
                
        for seq in sl.sequences:
            currentIndex = sl.sequences.index(seq)
            parsedSequence = parsedSequences[currentIndex]
            wr.writerow(getSt25St26Lengths(210, 
                seq.seqIdNo, 
                parsedSequences[currentIndex].seqIdNo, 
                'sequenceIDNumber', 
                'SEQ ID NO: %s' % parsedSequence.seqIdNo))
            wr.writerow(getSt25St26Lengths(211, 
                seq.length, 
                parsedSequence.length, 
                'INSDSeq_length', '-'))
            wr.writerow(getSt25St26Lengths(212, 
                seq.molType, 
                parsedSequence.molType, 
                'INSDSeq_moltype', '-'))
            wr.writerow(getSt25St26Lengths(213, 
                seq.organism, 
                parsedSequence.organism, 
                'INSDQualifier_value', '-'))
            
            parsedFeatures = parsedSequence.features
            for feat in seq.features:
                currentFeatureIndex = seq.features.index(feat)
                wr.writerow(getSt25St26Lengths(220, 
                    feat.featureHeader, 
                    parsedFeatures[currentFeatureIndex].featureHeader, 
                    'INSDFeature', 
                    '-'))
                wr.writerow(getSt25St26Lengths(221, 
                    feat.key, 
                    parsedFeatures[currentFeatureIndex].key, 
                    'INSDFeature_key', 
                    '-'))
                wr.writerow(getSt25St26Lengths(222, 
                    feat.location, 
                    parsedFeatures[currentFeatureIndex].location, 
                    'INSDFeature_location', 
                    '-'))
                wr.writerow(getSt25St26Lengths(223, 
                    feat.description, 
                    parsedFeatures[currentFeatureIndex].description, 
                    'INSDQualifier_value', 
                    '-'))
            if parsedSequence.molType == 'PRT':
                parsedResidues = parsedSequence.residues_prt
                wr.writerow([400, 
                            safeLength(seq.residues), 
                            safeLength(parsedResidues),
                            cu.TAG_LENGTH_ST26['INSDSeq_sequence'],
                            (cu.TAG_LENGTH_ST26['INSDSeq_sequence'] + 
                            len(cu.oneLetterCode(parsedResidues))),
                            'INSDSeq_sequence', '3-to-1 letter code' 
                            ])
            else:
                parsedResidues = parsedSequence.residues_nuc
            
#             print 'seq id no', parsedSequence.seqIdNo 
#             print parsedResidues
            
                wr.writerow(getSt25St26Lengths(400, 
                    seq.residues, 
                    parsedResidues, 
                    'INSDSeq_sequence', '-'))    
            
            
        
f5 = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 'testData', 'file5.txt') 
outf = 'combined_lengths.csv'

writeSizes(f5, outf)
print 'Done'
 
# def getElementSize(aFilePath):
#     blocks = []
#     
#     with open(aFilePath, 'r') as f:
#         blocks = f.read().split('<210>')
#     
# #     pprint.pprint(blocks)    
#     m = GENERAL_INFORMATION_PATTERN.match(blocks[0])
#       
#     if m:
#         print 'General information match found.'
#         print m.group('seqlHeader')
#         print m.group('applicant')
#         print m.group('title')
#         print m.group('reference')
#         print m.group('applicationNumber')
#         print m.group('filingDate')
#         print m.group('priorities')
#         print m.group('quantity')
#         print m.group('software')
#         
#     for s in blocks[1:]:
#         print '='*50
#         reconstructedString = '<210>%s' %s
# #         print reconstructedString
#         sm = SEQUENCE_PATTERN.match(reconstructedString)
#         if sm:
#             print 'Sequence match found.'
#             print sm.group('seqIdNo')
#             print sm.group('length')
#             print sm.group('molType')
#             print sm.group('organism')
#             featuresString = sm.group('features')
#             if featuresString:
#                 reconstructedFeatureString = '<220>%s' % sm.group('features')
#                 featureMatchers = FEATURE_PATTERN.finditer(reconstructedFeatureString)
#                 
#                 for fm in featureMatchers:
#                     print '\t%s' %('&'*50)
#                     print fm.group('featureHeader')
#                     print fm.group('key')
#                     print fm.group('location')
#                     print fm.group('description')
# #               print sm.group('features')
#             print sm.group('residues')



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