'''
Created on Jul 12, 2016

@author: ad
'''
import re 
import csv
import pprint
import converter_util as cu 

import st25parser.seqlparser

GENERAL_INFORMATION_REGEX = r"""(?P<seqlHeader>[^<]+)?
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

class RawSequenceListing(object):
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
            self.sequences.append(RawSequence(reconstructedString))
             
class RawSequence(object):
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
                    self.features.append(RawFeature(fm))

            self.residues = sm.group('residues')

class RawFeature(object):
    def __init__(self, fm):
        self.featureHeader = fm.group('featureHeader')
        self.key = fm.group('key')
        self.location = fm.group('location')
        self.description = fm.group('description')


class ElementSizeCalculator(object):
    def __init__(self, aFilePath):
        self.seql_raw = RawSequenceListing(aFilePath)
        self.seql_clean = st25parser.seqlparser.SequenceListing(aFilePath)
        
        self.sequenceRows = self.setSequenceRows()
     
    def _getSt25St26Lengths(self,
                        element_st25_tag, 
                        seqIdNo,
                        element_st25, 
                        value_st25, 
                        element_st26, comment):
        
        return [element_st25_tag, 
                seqIdNo,
                cu.safeLength(element_st25), 
                cu.safeLength(value_st25),
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26],
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26] + 
                                    cu.safeLength(value_st25),
                element_st26, 
                comment
                ]    
    
    def getRow_110(self):
        return self._getSt25St26Lengths(110, 0,
            self.seql_raw.applicant,
            self.seql_clean.generalInformation.applicant[0],
            'ApplicantName', '-')
    
    def getRow_120(self):
        return self._getSt25St26Lengths(120, 0,
            self.seql_raw.title,
            self.seql_clean.generalInformation.title,
            'InventionTitle', '-')
        
    def getRow_130(self):
        return self._getSt25St26Lengths(130, 0,
            self.seql_raw.reference,
            self.seql_clean.generalInformation.reference,
            'ApplicantFileReference', '-')
#     TODO: include in calculation IPOffice element!
    def getRow_140(self):
        return self._getSt25St26Lengths(140, 0, 
            self.seql_raw.applicationNumber,
            self.seql_clean.generalInformation.applicationNumber,
            'ApplicationNumberText', '-')
     
    def getRow_141(self):
        return self._getSt25St26Lengths(141, 0, 
            self.seql_raw.filingDate,
            self.seql_clean.generalInformation.filingDate,
            'FilingDate', '-')
        
#     TODO add code for prio

    def getRow_160(self):
        return self._getSt25St26Lengths(160, 0, 
            self.seql_raw.quantity,
            self.seql_clean.generalInformation.quantity,
            'SequenceTotalQuantity', '-')
    
    def getRow_170(self):
        return self._getSt25St26Lengths(170, 0, 
            self.seql_raw.software,
            self.seql_clean.generalInformation.software,
            '-', 'information discarded in ST.26')

    def setSequenceRows(self):
        res = []
        
        parsedSequences = []
        for s in self.seql_clean.generateSequence():
            parsedSequences.append(s)
                
        for seq in self.seql_raw.sequences:
            currentIndex = self.seql_raw.sequences.index(seq)
            parsedSequence = parsedSequences[currentIndex]
            currentSeqId = parsedSequence.seqIdNo
            currentRow210 = self._getSt25St26Lengths(210, currentSeqId, 
                            seq.seqIdNo, parsedSequence.seqIdNo, 'sequenceIDNumber', '-')

            res.append(currentRow210)
            
            currentRow211 = self._getSt25St26Lengths(211, currentSeqId, 
                            seq.length, parsedSequence.length, 'INSDSeq_length', '-')
            res.append(currentRow211)
            
            currentRow212 = self._getSt25St26Lengths(212, currentSeqId, 
                            seq.molType, parsedSequence.molType, 'INSDSeq_moltype', '-')
            res.append(currentRow212)
            
            currentRow213 = self._getSt25St26Lengths(213, currentSeqId, 
                            seq.organism, parsedSequence.organism, 'INSDQualifier_value', '-')
            res.append(currentRow213)
        
            parsedFeatures = parsedSequence.features
            for feat in seq.features:
                currentFeatureIndex = seq.features.index(feat)
                parsedFeature = parsedFeatures[currentFeatureIndex]
                
                currentRow220 = self._getSt25St26Lengths(220, currentSeqId, 
                            feat.featureHeader, parsedFeature.featureHeader, 
                            'INSDFeature', '-')
                res.append(currentRow220)
                
                currentRow221 = self._getSt25St26Lengths(221, currentSeqId, 
                            feat.key, parsedFeature.key, 
                            'INSDFeature_key', '-')
                res.append(currentRow221)
                
                currentRow222 = self._getSt25St26Lengths(222, currentSeqId, 
                            feat.location, parsedFeature.location, 
                            'INSDFeature_location', '-')
                res.append(currentRow222)
                
                currentRow223 = self._getSt25St26Lengths(223, currentSeqId, 
                            feat.description, parsedFeature.description, 
                            'INSDQualifier_value', '-')
                res.append(currentRow223)
                
        
            if parsedSequence.molType == 'PRT':
                parsedResidues = parsedSequence.residues_prt
                currentRow400 = [400, currentSeqId, 
                            cu.safeLength(seq.residues), 
                            cu.safeLength(parsedResidues),
                            cu.TAG_LENGTH_ST26['INSDSeq_sequence'],
                            (cu.TAG_LENGTH_ST26['INSDSeq_sequence'] + 
                            len(cu.oneLetterCode(parsedResidues))),
                            'INSDSeq_sequence', '3-to-1 letter code']
                
            else:
                parsedResidues = parsedSequence.residues_nuc
                currentRow400 = self._getSt25St26Lengths(400, currentSeqId, 
                                seq.residues, parsedResidues, 
                                'INSDSeq_sequence', '-')
            res.append(currentRow400)
        
        return res 

def writeSizes(inFile, outFile):
    sl = RawSequenceListing(inFile)
    slp = st25parser.seqlparser.SequenceListing(inFile)
    
    def getSt25St26Lengths(element_st25, 
                           element_st25_length, 
                           value_st25_length, 
                           element_st26, comment):
        
        return [element_st25, 
                cu.safeLength(element_st25_length), 
                cu.safeLength(value_st25_length),
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26],
                0 if element_st26 == '-' else cu.TAG_LENGTH_ST26[element_st26] + cu.safeLength(value_st25_length),
                element_st26, 
                comment
                ]
        
    
    with open(outFile, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(['element_st25', 'element_st25_length', 'value_st25_length', 
                     'tag_st26_length', 'element_st26_length', 'element_st26', 
                     'comment'])
                         
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

# TODO: calculate and write to csv priorities sizes        
        priority_st25 = slp.generalInformation.priority
        priority_st25_length = sum([len(a[0]) + len(a[1]) for a in priority_st25])
        priorityNumber_length = 0
        priorityDate_length = 0
        if priority_st25:
            priorityNumber_length = cu.safeLength(priority_st25[0][0])
            priorityDate_length = cu.safeLength(priority_st25[0][1])
        
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
                            cu.safeLength(seq.residues), 
                            cu.safeLength(parsedResidues),
                            cu.TAG_LENGTH_ST26['INSDSeq_sequence'],
                            (cu.TAG_LENGTH_ST26['INSDSeq_sequence'] + 
                            len(cu.oneLetterCode(parsedResidues))),
                            'INSDSeq_sequence', '3-to-1 letter code' 
                            ])
            else:
                parsedResidues = parsedSequence.residues_nuc
                wr.writerow(getSt25St26Lengths(400, 
                    seq.residues, 
                    parsedResidues, 
                    'INSDSeq_sequence', '-'))    
            
            
        

 
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