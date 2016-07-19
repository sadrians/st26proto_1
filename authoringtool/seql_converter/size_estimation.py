'''
Created on Jul 12, 2016

@author: ad
'''
import re 
import os 
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
        self.filePath = aFilePath
        self.seql_raw = RawSequenceListing(self.filePath)
        self.seql_clean = st25parser.seqlparser.SequenceListing(self.filePath)
        self.generalInformationRows = []
#         self.generalInformationRows.append(self.getRow_header())
        self.setRow_header()
        self.setRow_dtdVersion()
        self.setRow_fileName()
        self.setRow_softwareName()
        self.setRow_110()
        self.setRow_120()
        self.setRow_130()
        if self.seql_raw.applicationNumber and self.seql_raw.filingDate:
            self.setRow_ApplicationIdentification()
            self.setRow_IPOfficeCode()
            self.setRow_140()
            self.setRow_141()
        if self.seql_raw.priorities:
            self.setRow_prio()
        self.setRow_160()
        self.setRow_170()
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

    def setRow_header(self):
        self.generalInformationRows.append([0, 0, 
                cu.safeLength(self.seql_raw.seqlHeader),
                cu.safeLength(self.seql_clean.generalInformation.seqlHeader),
                cu.TAG_LENGTH_ST26['ST26SequenceListing'],
                cu.TAG_LENGTH_ST26['ST26SequenceListing'],
                'ST26SequenceListing', 
                'ST.25 seqlHeader discarded'])
    
    def setRow_dtdVersion(self):
        dtdVersionValue = 'd.d'
        self.generalInformationRows.append([0, 0, 
                0,
                len(dtdVersionValue),
                cu.TAG_LENGTH_ST26['dtdVersion'],
                len(dtdVersionValue) + cu.TAG_LENGTH_ST26['dtdVersion'],
                'dtdVersion', 
                'ST.26 specific element. Assumed format: d.d (for ex.: 1.3)'])
    
    def setRow_fileName(self):
#         file name without extension
        fileName = os.path.basename(self.filePath)[:-4]
        
        self.generalInformationRows.append([0, 0, 
                0,
                len(fileName),
                cu.TAG_LENGTH_ST26['fileName'],
                len(fileName) + cu.TAG_LENGTH_ST26['fileName'],
                'fileName', 
                'ST.25 file name used with extension xml'])
    
    def setRow_softwareName(self):
        lenSoftwareNameValue = 10
        self.generalInformationRows.append([0, 0, 
                0,
                lenSoftwareNameValue,
                cu.TAG_LENGTH_ST26['softwareName'],
                lenSoftwareNameValue + cu.TAG_LENGTH_ST26['softwareName'],
                'softwareName', 
                'ST.26 specific element. Assumed it has 10 chars'])
    

# softwareVersion
# productionDate
        
    def setRow_110(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(110, 0,
            self.seql_raw.applicant,
            self.seql_clean.generalInformation.applicant[0],
            'ApplicantName', '-'))
    
    def setRow_120(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(120, 0,
            self.seql_raw.title,
            self.seql_clean.generalInformation.title,
            'InventionTitle', '-'))
        
    def setRow_130(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(130, 0,
            self.seql_raw.reference,
            self.seql_clean.generalInformation.reference,
            'ApplicantFileReference', '-'))
#     TODO: include in calculation IPOffice element!
 
    def setRow_ApplicationIdentification(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['ApplicationIdentification'],
                cu.TAG_LENGTH_ST26['ApplicationIdentification'],
                'ApplicationIdentification', 
                '-']
        
        self.generalInformationRows.append(r)
         
    def setRow_IPOfficeCode(self):
        r = [0, 0, 
                0,
                0,
                cu.TAG_LENGTH_ST26['IPOfficeCode'],
                cu.TAG_LENGTH_ST26['IPOfficeCode'],
                'IPOfficeCode', 
                'Corresponding to 140. Empty for the purpose of this study']
        
        self.generalInformationRows.append(r)
        
    def setRow_140(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(140, 0, 
            self.seql_raw.applicationNumber,
            self.seql_clean.generalInformation.applicationNumber,
            'ApplicationNumberText', '-'))
     
    def setRow_141(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(141, 0, 
            self.seql_raw.filingDate,
            self.seql_clean.generalInformation.filingDate,
            'FilingDate', '-'))
        
#     TODO add code for prio
    
    def setRow_prio(self):
        
        res = ['prio', 0, cu.safeLength(self.seql_raw.priorities)]
        
        priority_clean = self.seql_clean.generalInformation.priority
        pr_length = 0
        if priority_clean:
            pr = priority_clean[0]
            pr_applNr = pr[0]
            pr_filingDate = pr[1]
            
            pr_length = cu.safeLength(pr_applNr) + cu.safeLength(pr_filingDate)
        
        res.append(pr_length)
        res.append(cu.TAG_LENGTH_ST26['EarliestPriorityApplicationIdentification'] + 
                cu.TAG_LENGTH_ST26['IPOfficeCode'] + 
                cu.TAG_LENGTH_ST26['ApplicationNumberText'] + 
                cu.TAG_LENGTH_ST26['FilingDate'])
        res.append(pr_length + res[4])
        res.append('EarliestPriorityApplicationIdentification')
        res.append('only first ST.25 priority retained, if any')
        
        self.generalInformationRows.append(res)
    
    def setRow_160(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(160, 0, 
            self.seql_raw.quantity,
            self.seql_clean.generalInformation.quantity,
            'SequenceTotalQuantity', '-'))
    
    def setRow_170(self):
        self.generalInformationRows.append(self._getSt25St26Lengths(170, 0, 
            self.seql_raw.software,
            self.seql_clean.generalInformation.software,
            '-', 'information discarded in ST.26'))

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
            
            moltypeValue = 'AA' if parsedSequence.molType == 'PRT' else parsedSequence.molType 

            currentRow212 = [212, currentSeqId, cu.safeLength(seq.molType), 
                            cu.safeLength(parsedSequence.molType), 
                            cu.TAG_LENGTH_ST26['INSDSeq_moltype'], 
                            cu.safeLength(moltypeValue) + cu.TAG_LENGTH_ST26['INSDSeq_moltype'],
                            'INSDSeq_moltype', 
                            'PRT replaced by AA for protein sequences' if moltypeValue == 'AA' else '-']
            
            res.append(currentRow212)
                        
#             create ST.26 feature source
            currentRow_INSDFeature = [0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature'], 
                            cu.TAG_LENGTH_ST26['INSDFeature'],
                            'INSDFeature', 
                            'ST.26 mandatory feature source']
            res.append(currentRow_INSDFeature)
            
            currentRow_INSDFeature_key = [0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_key'], 
                            len('source') + cu.TAG_LENGTH_ST26['INSDFeature_key'],
                            'INSDFeature_key', 
                            'ST.26 mandatory feature source']
            
            res.append(currentRow_INSDFeature_key)
            
            sourceLocation = '1..%s' % parsedSequence.length
            currentRow_INSDFeature_location = [0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_location'], 
                            len(sourceLocation) + cu.TAG_LENGTH_ST26['INSDFeature_location'],
                            'INSDFeature_location', 
                            'ST.26 mandatory feature source']
            
            res.append(currentRow_INSDFeature_location)
            
            def append_INSDFeature_quals(msg):
                res.append([0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDFeature_quals'], 
                            cu.TAG_LENGTH_ST26['INSDFeature_quals'],
                            'INSDFeature_quals', 
                            msg])
            
#             add first the parent element INSDFeature_quals
            append_INSDFeature_quals('ST.26 mandatory feature source')
            
            def createQualifier(name, msg):
                currentRow_INSDQualifier = [0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDQualifier'], 
                            cu.TAG_LENGTH_ST26['INSDQualifier'],
                            'INSDQualifier', 
                            msg]
            
                res.append(currentRow_INSDQualifier)
                
                currentRow_INSDQualifier_name = [0, currentSeqId, 0, 0, 
                            cu.TAG_LENGTH_ST26['INSDQualifier_name'], 
                            len(name) + cu.TAG_LENGTH_ST26['INSDQualifier_name'],
                            'INSDQualifier_name', 
                            msg]
            
                res.append(currentRow_INSDQualifier_name)
            
            def createQualifierValue(tag_st25, element_st25, value_st25, msg):
                
                currentRow_INSDQualifier_value = [tag_st25, 
                    currentSeqId, cu.safeLength(element_st25), 
                    cu.safeLength(value_st25), 
                    cu.TAG_LENGTH_ST26['INSDQualifier_value'], 
                    cu.safeLength(value_st25) + cu.TAG_LENGTH_ST26['INSDQualifier_value'],
                    'INSDQualifier_value', 
                    msg]
            
                res.append(currentRow_INSDQualifier_value)
            
#             qualifier organism
            createQualifier('organism', 'ST.26 mandatory qualifier organism')
            createQualifierValue(213, seq.organism, 
                            parsedSequence.organism, 
                            'ST.26 mandatory qualifier organism')

#             qualifier mol_type
            mol_typeValue = 'protein' if parsedSequence.molType == 'PRT' else 'genomic DNA'
            createQualifier('mol_type', 'ST.26 mandatory qualifier mol_type') 
#             createQualifierValue(0, 0, mol_typeValue, 'ST.26 mandatory qualifier mol_type')
            res.append([0, currentSeqId, 0, 0,  
                    cu.TAG_LENGTH_ST26['INSDQualifier_value'], 
                    cu.safeLength(mol_typeValue) + cu.TAG_LENGTH_ST26['INSDQualifier_value'],
                    'INSDQualifier_value', 
                    'ST.26 mandatory qualifier mol_type'])
            
            


#             end create ST.26 feature source
        
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
                
                
#                 add element INSDFeature_quals
                append_INSDFeature_quals('-')
                
                createQualifier('note', '-')
                
                createQualifierValue(223, feat.description, 
                                parsedFeature.description, 
                                '-')
                
                
#                 currentRow223 = self._getSt25St26Lengths(223, currentSeqId, 
#                             feat.description, parsedFeature.description, 
#                             'INSDQualifier_value', '-')
#                 res.append(currentRow223)
                
        
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
    
    def writeSizes(self, outFilePath):
        with open(outFilePath, 'wb') as csvfile:
            wr = csv.writer(csvfile, delimiter=',')
            wr.writerow(['element_st25', 'seqIdNo', 
                         'element_st25_length', 
                         'value_length', 
                         'tag_st26_length', 
                         'element_st26_length', 
                         'element_st26', 
                         'comment'])
            
            for genInfoRow in self.generalInformationRows:
                wr.writerow(genInfoRow)
            for seqRow in self.sequenceRows:
                wr.writerow(seqRow)
        

