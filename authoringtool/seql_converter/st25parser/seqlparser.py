__author__ = 'ad'

import re
import os 
import seqlutils as su

pa = '<210>'

def tag(i):
    return '<?%i>?' % i

generalInformationRegex = r"""(?P<header>[^<]*)
                            <110>\s*(?P<applicant>[^<]*)
                            ({tag120}\s*(?P<title>[^<]*))?
                            ({tag130}\s*(?P<reference>[^<]*))?
                            ({tag140}\s*(?P<applicationNumber>[^<]*))?
                            ({tag141}\s*(?P<filingDate>[^<]*))?
                            ({tag150}\s*(?P<priority>.*))*
                            ({tag160}\s*(?P<quantity>[^<]*))
                            ({tag170}\s*(?P<software>[^<]*))?
                            """.format(tag120 = tag(120),
                                       tag130 = tag(130),
                                       tag140 = tag(140),
                                       tag141 = tag(141),
                                       tag150 = tag(150),
                                       tag160 = tag(160),
                                       tag170 = tag(170))

generalInformationPattern = re.compile(generalInformationRegex, re.DOTALL | re.VERBOSE)

# (<151>\s*(?P<priorityDate>[^<]*))*
# priorityRegex = r"""(<150>\s*(?P<prNumber>[^<]*?)<151>\s*(?P<prDate>[^<]*))+"""
# priorityPattern = re.compile(priorityRegex, re.MULTILINE)

sequenceRegex = r"""<210>\s*(?P<seqIdNo>[^<]*)
                    (<211>\s*(?P<length>[^<]*))?
                    (<212>\s*(?P<molType>[^<]*))?
                    (<213>\s*(?P<organism>[^<]*))?
                    (?P<featureTable><220>.*?)?
                    (?P<publicationData><300>.*?)?
                    <400>\s*(?P<seqNo400>\d+)(?P<residues>.*)"""
sequencePattern = re.compile(sequenceRegex, re.DOTALL | re.VERBOSE)

featureRegex = r"""(<220>\s*(?P<featureHeader>[^<]*))
                    (<221>\s*(?P<key>[^<]*))?
                    (<222>\s*(?P<location>[^<]*))?
                    (<223>\s*(?P<description>[^<]*))?"""
featurePattern = re.compile(featureRegex, re.DOTALL | re.VERBOSE)

nucRegex = r'[a-z][a-z\s\d]+'
nucPattern = re.compile(nucRegex)

prtRegex = r"[A-Za-z\s]+"
prtPattern = re.compile(prtRegex)

def safeStrip(s):
    if s is not None:
        return s.strip()
    else:
#         return s
        return su.DEFAULT_STRING

class SequenceListing(object):
    def __init__(self, inFile):
#         print inFile 
        self.isSeql = False
        try:
            self.seqlGenerator = su.generateChunks(inFile, pa)
            generalInformationString = self.seqlGenerator.next()['chunk']
            self.generalInformation = GeneralInformation(generalInformationString)

            if self.generalInformation.genInfoPatternFound:
                self.isSeql = True

            # print 'SequenceListing initialised for file', inFile
        except IOError:
            # self.logger.exception("Invalid input file: %s" % self.in_file_name)
            print 'Invalid file name', inFile

    def generateSequence(self):
        '''
        Yield one Sequence at a time.
        :return: Sequence
        '''
        # try:
        counter = 0
        for elem in self.seqlGenerator:
            counter += 1
            chunk = elem['chunk']
            lineNumber = elem['lineNumber']
            try:
                seq = Sequence(chunk)
                seq.actualSeqIdNo = counter
                yield seq
            except SeqlException as se:
                # self.logger.exception(
                #     '*Input file: %s\n\t*ParseException (while parsing sequence) in line number %s, column %s. The line is: %s' % (
                #         self.in_file_name,
                #         pe.__getattr__('lineno') + lineNumber - 1,
                #         pe.__getattr__('col'), pe.__getattr__('line')))
                su.logger.exception('Exception in line %s' % lineNumber)
                su.logger.exception(se)

    @classmethod
    def getSequenceFromFile(cls, aFile, aSeqIdNo):
        '''
        Return the Sequence instance corresponding to aSeqIdNo in aFile.
        The assumption is that seqIdNo = actualSeqIdNo.

        :param aFile: a sequence listing file
        :param aSeqIdNo: int representing the seq id no
        :return: Sequence
        '''
        # TODO: test it
        listOfChunks = []
        for c in su.generateChunks(aFile, pa):
            listOfChunks.append(c)


        inputString = listOfChunks[aSeqIdNo]['chunk']

        seq = Sequence(inputString)
        seq.actualSeqIdNo = aSeqIdNo#TODO: to see if this is OK

        return seq


class GeneralInformation(object):
    def __init__(self, inStr):
        self.genInfoPatternFound = False
        self.applicant = []
        self.title = '-'
        self.reference = '-'
        self.applicationNumber = '-'
        self.filingDate = '-'
        self.priority = [] # a list of tuples (applNumber, filingDate)
        self.quantity = 0
        self.software = '-'
        
        m = generalInformationPattern.match(inStr)
        
        if m:
            applicantLines = m.group('applicant').splitlines()
            self.applicant = [a.strip() for a in applicantLines if a.strip() != ''] 
            self.title = su.inOneLine(safeStrip(m.group('title')))
            self.reference = safeStrip(m.group('reference'))
            self.applicationNumber = safeStrip(m.group('applicationNumber'))
            self.filingDate = safeStrip(m.group('filingDate'))
            
            pg = m.group('priority')
#             if pg.endswith('<'):
#                 pg = pg[:1]
#             print 'pg'
#             print pg
            if pg:
                self.priority = self.parsePriority(safeStrip(pg[:-1]))
            
            self.quantity = safeStrip(m.group('quantity'))
            self.software = safeStrip(m.group('software'))
            self.genInfoPatternFound = True

    @classmethod
    def parsePriority(self, aString):
        result = []
#         if aString != '':
        if aString not in (None, ''):

            pr = '<150>' + aString
            
            
            result = []
            if aString != '':
                pr = '<150>' + aString 
        #         print pr
                prList = pr.split('<150>')
#                 print prList
                
                for p in prList[1:]:
                    l = p.split('<151>')
#                     print l
                    result.append((safeStrip(l[0]), safeStrip(l[1])))
        
        
        return result

class Sequence(object):
    def __init__(self, inStr):
        # print 'seq input', inStr
        self.successfullyParsed = False
        self.features = []
        self.residues_nuc = '-'
        self.residues_prt = '-'

        self.actualSeqIdNo = 0
        self.actualMolType = '-'
        self.actualLength = 0
        self.mixedMode = False
        self.isSkipCode = False

        m = sequencePattern.match(inStr)
        if m:
            self.seqIdNo = safeStrip(m.group('seqIdNo'))
            self.length = safeStrip(m.group('length'))
            self.molType = safeStrip(m.group('molType'))
            self.organism = safeStrip(m.group('organism'))

            featureTable = safeStrip(m.group('featureTable'))

            self.seqNo400 = safeStrip(m.group('seqNo400'))

            if featureTable:
                fiter = re.finditer(featurePattern, featureTable)
                for fmatcher in fiter:
                    if fmatcher:
                        self.features.append(Feature(fmatcher))

            residues = m.group('residues')
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
            if self.residues_nuc == '' and self.residues_prt == '':
                self.isSkipCode = True

            self.__setActualMolType__()
            self.__setActualLength__()
            self.successfullyParsed = True #TODO: to add unittest for False

            # print '='*30
        else:
            raise SeqlException('Parser failed for input:\n%s' % inStr)

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


class SeqlException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg


class Feature(object):
    def __init__(self, m):
        # print '\tf inStr xx%sxx' %inStr
        # TODO: code needed for 220 missing
        self.featureHeader = '-'
        self.key = '-'
        self.location = '-'
        self.description = '-'

        self.featureHeader = safeStrip(m.group('featureHeader'))
        if m.group('key'):
            self.key = safeStrip(m.group('key'))
        if m.group('location'):
            self.location = safeStrip(m.group('location'))
        if m.group('description'):
            self.description = safeStrip(m.group('description'))
        if self.description:
            self.description = su.inOneLine(self.description)

    def printFeat(self):
        print '\tfeatureHeader:', self.featureHeader
        print '\tkey:', self.key
        print '\tlocation:', self.location
        print '\tdescription:%s\n' %self.description

# ===================================

# class SequenceListingSizeAnalyser(object):
#     def __init__(self, inFile):
# #         print inFile 
#         self.isSeql = False
#         try:
#             self.seqlGenerator = su.generateChunks(inFile, pa)
#             generalInformationString = self.seqlGenerator.next()['chunk']
#             self.generalInformationMatcher = generalInformationPattern.match(generalInformationString)
# 
#             if self.generalInformation.genInfoPatternFound:
#                 self.isSeql = True
# 
#             # print 'SequenceListing initialised for file', inFile
#         except IOError:
#             # self.logger.exception("Invalid input file: %s" % self.in_file_name)
#             print 'Invalid file name', inFile
# 
# #     def generateSequence(self):
# #         '''
# #         Yield one Sequence at a time.
# #         :return: Sequence
# #         '''
# #         # try:
# #         counter = 0
# #         for elem in self.seqlGenerator:
# #             counter += 1
# #             chunk = elem['chunk']
# #             lineNumber = elem['lineNumber']
# #             try:
# #                 seq = Sequence(chunk)
# #                 seq.actualSeqIdNo = counter
# #                 yield seq
# #             except SeqlException as se:
# #                 # self.logger.exception(
# #                 #     '*Input file: %s\n\t*ParseException (while parsing sequence) in line number %s, column %s. The line is: %s' % (
# #                 #         self.in_file_name,
# #                 #         pe.__getattr__('lineno') + lineNumber - 1,
# #                 #         pe.__getattr__('col'), pe.__getattr__('line')))
# #                 su.logger.exception('Exception in line %s' % lineNumber)
# #                 su.logger.exception(se)
# # 
# #     @classmethod
# #     def getSequenceFromFile(cls, aFile, aSeqIdNo):
# #         '''
# #         Return the Sequence instance corresponding to aSeqIdNo in aFile.
# #         The assumption is that seqIdNo = actualSeqIdNo.
# # 
# #         :param aFile: a sequence listing file
# #         :param aSeqIdNo: int representing the seq id no
# #         :return: Sequence
# #         '''
# #         # TODO: test it
# #         listOfChunks = []
# #         for c in su.generateChunks(aFile, pa):
# #             listOfChunks.append(c)
# # 
# # 
# #         inputString = listOfChunks[aSeqIdNo]['chunk']
# # 
# #         seq = Sequence(inputString)
# #         seq.actualSeqIdNo = aSeqIdNo#TODO: to see if this is OK
# # 
# #         return seq
# # 
# # 
# # class GeneralInformation(object):
# #     def __init__(self, inStr):
# #         self.genInfoPatternFound = False
# #         self.applicant = []
# #         self.title = '-'
# #         self.reference = '-'
# #         self.applicationNumber = '-'
# #         self.filingDate = '-'
# #         self.priority = [] # a list of tuples (applNumber, filingDate)
# #         self.quantity = 0
# #         self.software = '-'
# #         
# #         m = generalInformationPattern.match(inStr)
# #         
# #         if m:
# #             applicantLines = m.group('applicant').splitlines()
# #             self.applicant = [a.strip() for a in applicantLines if a.strip() != ''] 
# #             self.title = su.inOneLine(safeStrip(m.group('title')))
# #             self.reference = safeStrip(m.group('reference'))
# #             self.applicationNumber = safeStrip(m.group('applicationNumber'))
# #             self.filingDate = safeStrip(m.group('filingDate'))
# #             
# #             pg = m.group('priority')
# # #             if pg.endswith('<'):
# # #                 pg = pg[:1]
# # #             print 'pg'
# # #             print pg
# #             if pg:
# #                 self.priority = self.parsePriority(safeStrip(pg[:-1]))
# #             
# #             self.quantity = safeStrip(m.group('quantity'))
# #             self.software = safeStrip(m.group('software'))
# #             self.genInfoPatternFound = True
# # 
# #     @classmethod
# #     def parsePriority(self, aString):
# #         result = []
# # #         if aString != '':
# #         if aString not in (None, ''):
# # 
# #             pr = '<150>' + aString
# #             
# #             
# #             result = []
# #             if aString != '':
# #                 pr = '<150>' + aString 
# #         #         print pr
# #                 prList = pr.split('<150>')
# # #                 print prList
# #                 
# #                 for p in prList[1:]:
# #                     l = p.split('<151>')
# # #                     print l
# #                     result.append((safeStrip(l[0]), safeStrip(l[1])))
# #         
# #         
# #         return result
# # 
# # class Sequence(object):
# #     def __init__(self, inStr):
# #         # print 'seq input', inStr
# #         self.successfullyParsed = False
# #         self.features = []
# #         self.residues_nuc = '-'
# #         self.residues_prt = '-'
# # 
# #         self.actualSeqIdNo = 0
# #         self.actualMolType = '-'
# #         self.actualLength = 0
# #         self.mixedMode = False
# #         self.isSkipCode = False
# # 
# #         m = sequencePattern.match(inStr)
# #         if m:
# #             self.seqIdNo = safeStrip(m.group('seqIdNo'))
# #             self.length = safeStrip(m.group('length'))
# #             self.molType = safeStrip(m.group('molType'))
# #             self.organism = safeStrip(m.group('organism'))
# # 
# #             featureTable = safeStrip(m.group('featureTable'))
# # 
# #             self.seqNo400 = safeStrip(m.group('seqNo400'))
# # 
# #             if featureTable:
# #                 fiter = re.finditer(featurePattern, featureTable)
# #                 for fmatcher in fiter:
# #                     if fmatcher:
# #                         self.features.append(Feature(fmatcher))
# # 
# #             residues = m.group('residues')
# #             nucList = []
# #             prtList = []
# #             for line in residues.splitlines():
# #                 if nucPattern.match(line):
# #                     nucList.append(line)
# #                 else: #if prtPattern.match(line): TODO: add more robust code
# #                     prtList.append(line)
# # 
# #             self.residues_nuc = ''.join(nucList)
# #             self.residues_prt = ''.join(prtList)
# # 
# #             self.residues_nuc = re.sub(r'[\s,\d]', '', self.residues_nuc)
# #             self.residues_prt = re.sub(r'[\s,\d]', '', self.residues_prt)
# # 
# #             if len(self.residues_nuc) > 0 and len(self.residues_prt) > 0:
# #                 self.mixedMode = True
# #             if self.residues_nuc == '' and self.residues_prt == '':
# #                 self.isSkipCode = True
# # 
# #             self.__setActualMolType__()
# #             self.__setActualLength__()
# #             self.successfullyParsed = True #TODO: to add unittest for False
# # 
# #             # print '='*30
# #         else:
# #             raise SeqlException('Parser failed for input:\n%s' % inStr)
# # 
# #     def __setActualMolType__(self):
# #         if self.residues_nuc == '':
# #             if self.residues_prt!= '':
# #                 self.actualMolType = 'PRT'
# #             else:
# #                 self.actualMolType = None
# #         elif 't' not in self.residues_nuc:
# #             self.actualMolType = 'RNA'
# #         else:
# #             self.actualMolType = 'DNA'
# # 
# #     def __setActualLength__(self):
# #         al = len(self.residues_nuc)
# #         if al > 0:
# #             self.actualLength = al
# #         else:
# #             self.actualLength = len(self.residues_prt)/3
# # 
# #     def printSeq(self):
# #         print 'seqIdNo:', self.seqIdNo
# #         print 'length:', self.length
# #         print 'molType:', self.molType
# #         print 'organism:', self.organism
# # 
# #         print 'actualMolType:', self.actualMolType
# #         print 'actualLength', self.actualLength
# #         print 'isSkipCode', self.isSkipCode
# #         print 'mixedMode', self.mixedMode
# # 
# #         for f in self.features:
# #             f.printFeat()
# # 
# #         print 'seqNo400:', self.seqNo400
# #         print 'residues_nuc:', self.residues_nuc
# #         print 'residues_prt:', self.residues_prt
# # 
# # 
# # class SeqlException(Exception):
# #     def __init__(self, msg):
# #         self.msg = msg
# # 
# #     def __repr__(self):
# #         return self.msg
# # 
# # 
# # class Feature(object):
# #     def __init__(self, m):
# #         # print '\tf inStr xx%sxx' %inStr
# #         # TODO: code needed for 220 missing
# #         self.featureHeader = '-'
# #         self.key = '-'
# #         self.location = '-'
# #         self.description = '-'
# # 
# #         self.featureHeader = safeStrip(m.group('featureHeader'))
# #         if m.group('key'):
# #             self.key = safeStrip(m.group('key'))
# #         if m.group('location'):
# #             self.location = safeStrip(m.group('location'))
# #         if m.group('description'):
# #             self.description = safeStrip(m.group('description'))
# #         if self.description:
# #             self.description = su.inOneLine(self.description)
# # 
# #     def printFeat(self):
# #         print '\tfeatureHeader:', self.featureHeader
# #         print '\tkey:', self.key
# #         print '\tlocation:', self.location
# #         print '\tdescription:%s\n' %self.description

