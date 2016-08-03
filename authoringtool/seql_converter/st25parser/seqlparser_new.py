__author__ = 'ad'

import re
import os 
import chardet
import pprint 
import seqlutils as su

# pa = '<210>'
# 
# def tag(i):
#     return '<?%i>?' % i
# 
# generalInformationRegex = r"""(?P<header>[^<]*)
#                             <110>\s*(?P<applicant>[^<]*)
#                             ({tag120}\s*(?P<title>[^<]*))?
#                             ({tag130}\s*(?P<reference>[^<]*))?
#                             ({tag140}\s*(?P<applicationNumber>[^<]*))?
#                             ({tag141}\s*(?P<filingDate>[^<]*))?
#                             ({tag150}\s*(?P<priority>.*))*
#                             ({tag160}\s*(?P<quantity>[^<]*))
#                             ({tag170}\s*(?P<software>[^<]*))?
#                             """.format(tag120 = tag(120),
#                                        tag130 = tag(130),
#                                        tag140 = tag(140),
#                                        tag141 = tag(141),
#                                        tag150 = tag(150),
#                                        tag160 = tag(160),
#                                        tag170 = tag(170))
# 
# generalInformationPattern = re.compile(generalInformationRegex, re.DOTALL | re.VERBOSE)
# 
# # (<151>\s*(?P<priorityDate>[^<]*))*
# # priorityRegex = r"""(<150>\s*(?P<prNumber>[^<]*?)<151>\s*(?P<prDate>[^<]*))+"""
# # priorityPattern = re.compile(priorityRegex, re.MULTILINE)
# 
# sequenceRegex = r"""<210>\s*(?P<seqIdNo>[^<]*)
#                     (<211>\s*(?P<length>[^<]*))?
#                     (<212>\s*(?P<molType>[^<]*))?
#                     (<213>\s*(?P<organism>[^<]*))?
#                     (?P<featureTable><220>.*?)?
#                     (?P<publicationData><300>.*?)?
#                     <400>\s*(?P<seqNo400>\d+)(?P<residues>.*)"""
# sequencePattern = re.compile(sequenceRegex, re.DOTALL | re.VERBOSE)
# 
# featureRegex = r"""(<220>\s*(?P<featureHeader>[^<]*))
#                     (<221>\s*(?P<key>[^<]*))?
#                     (<222>\s*(?P<location>[^<]*))?
#                     (<223>\s*(?P<description>[^<]*))?"""
# featurePattern = re.compile(featureRegex, re.DOTALL | re.VERBOSE)
# 
nucRegex = r'[a-z][a-z\s\d]+'
nucPattern = re.compile(nucRegex)
# 
prtRegex = r"[A-Za-z\s]+"
prtPattern = re.compile(prtRegex)

GENERAL_INFORMATION_REGEX = r"""(?P<seqlHeader_raw>[^<]+)?
                (?P<applicant_raw><110>\s+(?P<applicant>[^<]+))
                (?P<title_raw><120>\s+(?P<title>[^<]+))?
                (?P<reference_raw><130>\s+(?P<reference>[^<]+))?
                (?P<applicationNumber_raw><140>\s+(?P<applicationNumber>[^<]+))?
                (?P<filingDate_raw><141>\s+(?P<filingDate>[^<]+))?
                (?P<priorities_raw>((?P<priorityNumber><150>[^<]+)
                 (?P<priorityDate><151>[^<]+))+)*
                (?P<quantity_raw><160>\s+(?P<quantity>[^<]+))
                (?P<software_raw><170>\s+(?P<software>[^<]+))?
                """
 
GENERAL_INFORMATION_PATTERN = re.compile(GENERAL_INFORMATION_REGEX, re.DOTALL | re.VERBOSE)

SEQUENCE_REGEX = r"""
                (?P<seqIdNo_raw><210>\s+(?P<seqIdNo>[^<]+))
                (?P<length_raw><211>\s+(?P<length>[^<]+))?
                (?P<molType_raw><212>\s+(?P<molType>[^<]+))?
                (?P<organism_raw><213>\s+(?P<organism>[^<]+))?
                (?P<features_raw><220>.*?)?
                (?P<publicationData><300>.*?)?
                (?P<residues_raw><400>\s+(?P<seqNo400>\d+)(?P<residues>.*))
"""

SEQUENCE_PATTERN = re.compile(SEQUENCE_REGEX, re.DOTALL | re.VERBOSE)

FEATURE_REGEX = r"""
                (?P<featureHeader_raw><220>\s+(?P<featureHeader>[^<]+))
                (?P<key_raw><221>\s+(?P<key>[^<]+))?
                (?P<location_raw><222>\s+(?P<location>[^<]+))?
                (?P<description_raw><223>\s+(?P<description>[^<]+))?
"""
FEATURE_PATTERN = re.compile(FEATURE_REGEX, re.DOTALL | re.VERBOSE)

def safeStrip(s):
    if s is not None:
        return s.strip()
    else:
        return su.DEFAULT_STRING

class SequenceListing(object):
    def __init__(self, aFilePath):
        blocks = []
        self.filePath = aFilePath
        self.seqlHeader = '-'
        self.applicant = []
        self.title = '-'
        self.reference = '-'
        self.applicationNumber = '-'
        self.filingDate = '-'
        self.priorities = [] # a list of tuples (applNumber, filingDate)
        self.quantity = 0
        self.software = '-'
        
        self.sequences = []
        
        self.quantity_nuc = 0
        self.quantity_prt = 0
        self.quantity_mix = 0

        self.isSeql = False
        
        try:
            with open(aFilePath, 'r') as f:
                rawString = f.read()
                self.charEncoding = chardet.detect(rawString)['encoding']
#                 print self.charEncoding
                u = rawString.decode(self.charEncoding)
                blocks = u.split('<210>')
            self.setGeneralInformation(blocks[0])
#                 pprint.pprint(blocks) 
                
            for s in blocks[1:]:
                reconstructedString = '<210>%s' %s
                currentSeq = Sequence(reconstructedString)
                if currentSeq.successfullyParsed:
                    currentSeq.actualSeqIdNo = blocks.index(s)
                    
                    self.sequences.append(currentSeq)
                    if currentSeq.molType == 'PRT':
                        self.quantity_prt += 1
                    elif currentSeq.molType in ('DNA', 'RNA'):
                        self.quantity_nuc += 1
                        if currentSeq.mixedMode:
                            self.quantity_mix += 1 
                        
        except IOError:
            # self.logger.exception("Invalid input file: %s" % self.in_file_name)
            print 'Invalid file name', self.filePath
    
    def setGeneralInformation(self, aString):
        m = GENERAL_INFORMATION_PATTERN.match(aString)
          
        if m:
            self.seqlHeader_raw = m.group('seqlHeader_raw')
            self.seqlHeader = safeStrip(self.seqlHeader_raw)
            self.applicant_raw = m.group('applicant_raw')
            self.applicant_val = m.group('applicant')
            applicantLines = self.applicant_val.splitlines()
            self.applicant = [a.strip() for a in applicantLines if a.strip() != ''] 
            self.title_raw = m.group('title_raw')
            self.title = su.inOneLine(safeStrip(m.group('title')))
            self.reference_raw = m.group('reference_raw')
            self.reference = safeStrip(m.group('reference'))
            self.applicationNumber_raw = m.group('applicationNumber_raw')
            self.applicationNumber = safeStrip(m.group('applicationNumber'))
            self.filingDate = safeStrip(m.group('filingDate'))
            self.filingDate_raw = m.group('filingDate_raw')
            self.priorities_raw = m.group('priorities_raw')
            self.priorities = su.parsePriorities(self.priorities_raw)
            self.quantity_raw = m.group('quantity_raw')
            self.quantity = safeStrip(m.group('quantity'))
            self.software_raw = m.group('software_raw')
            self.software = safeStrip(m.group('software'))
            self.isSeql = True
            
        else:
            print 'File', self.filePath
            print 'SequenceListing: No match for general information pattern.'
    
             
class Sequence(object):
    def __init__(self, aStr):
        self.successfullyParsed = False
        self.features = []
        self.residues_nuc = '-'
        self.residues_prt = '-'
        self.translations = []
 
        self.actualSeqIdNo = 0
        self.actualMolType = '-'
        self.actualLength = 0
        self.mixedMode = False
        self.isSkipCode = False
        
        sm = SEQUENCE_PATTERN.match(aStr)
        
        if sm:
#             print 'Sequence match found.'
            self.seqIdNo_raw = sm.group('seqIdNo_raw')
            self.seqIdNo = safeStrip(sm.group('seqIdNo'))
            self.length_raw = sm.group('length_raw')
            self.length = safeStrip(sm.group('length'))
            self.molType_raw = sm.group('molType_raw')
            self.molType = safeStrip(sm.group('molType'))
            self.organism_raw = sm.group('organism_raw')
            self.organism = safeStrip(sm.group('organism'))
            
            featuresString = sm.group('features_raw')
            if featuresString:
                featureMatchers = FEATURE_PATTERN.finditer(featuresString)
                
                for fm in featureMatchers:
                    self.features.append(Feature(fm))

            self.residues_raw = sm.group('residues_raw')
            self.seqNo400 = safeStrip(sm.group('seqNo400'))
            
            residues = sm.group('residues')
            
            nucList = []
            prtList = []
            for line in residues.splitlines():
                if nucPattern.match(line):
                    nucList.append(line)
                else: #if prtPattern.match(line): TODO: add more robust code
                    prtList.append(line)
 
            self.residues_nuc = ''.join(nucList)
            self.residues_prt = ''.join(prtList)
 
            self.residues_nuc = re.sub(r'[\s,\d]', '', self.residues_nuc)
            self.residues_prt = re.sub(r'[\s,\d]', '', self.residues_prt)
            
            if len(self.residues_nuc) > 0 and len(self.residues_prt) > 0:
                self.mixedMode = True
#             TODO: test it
            if self.residues_nuc == '' and self.residues_prt == '':
                self.isSkipCode = True
                
            if self.mixedMode:
                currentStart = 0
                for f in self.features:
                    if f.key == 'CDS':
                        t = su.getRangeFromLocation(f.location)
                        currentTranslationLength = t[1] - t[0]
                        currentEnd = currentStart + currentTranslationLength +1
                        currentTranslation = self.residues_prt[currentStart:currentEnd]
                        currentStart = currentEnd 
                        self.translations.append(currentTranslation)
                        f.translation = currentTranslation
            self.__setActualMolType__()
            self.__setActualLength__()
            self.successfullyParsed = True 
        else:
#             print 'File', self.filePath
            print 'Sequence: No match for sequence pattern for input:', aStr 
     
    def __setActualMolType__(self):
        if self.residues_nuc == '':
            if self.residues_prt!= '':
                self.actualMolType = 'PRT'
            else:
                self.actualMolType = None
        elif 't' not in self.residues_nuc:
            self.actualMolType = 'RNA'
        else:
            self.actualMolType = 'DNA'
 
    def __setActualLength__(self):
        al = len(self.residues_nuc)
        if al > 0:
            self.actualLength = al
        else:
            self.actualLength = len(self.residues_prt)/3 
         
    def printSeq(self):
        print 'seqIdNo:', self.seqIdNo
        print 'length:', self.length
        print 'molType:', self.molType
        print 'organism:', self.organism
 
        print 'actualMolType:', self.actualMolType
        print 'actualLength', self.actualLength
        print 'isSkipCode', self.isSkipCode
        print 'mixedMode', self.mixedMode
 
        for f in self.features:
            f.printFeat()
 
        print 'seqNo400:', self.seqNo400
        print 'residues_nuc:', self.residues_nuc
        print 'residues_prt:', self.residues_prt 
            
class Feature(object):
    def __init__(self, fm):
        self.featureHeader_raw = fm.group('featureHeader_raw')
        self.featureHeader = safeStrip(fm.group('featureHeader'))
        self.key_raw = fm.group('key_raw')
        self.key = safeStrip(fm.group('key'))
        self.location_raw = fm.group('location_raw')
        self.location = safeStrip(fm.group('location'))
        self.description_raw = fm.group('description_raw')
        self.description = su.inOneLine(safeStrip(fm.group('description')))
        self.translation = su.DEFAULT_STRING
        
    def printFeat(self):
        print '\tfeatureHeader:', self.featureHeader
        print '\tkey:', self.key
        print '\tlocation:', self.location
        print '\tdescription:%s\n' %self.description
        print '\ttranslation:%s\n' %self.translation

