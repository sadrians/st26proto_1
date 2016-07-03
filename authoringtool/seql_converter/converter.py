'''
Created on Jul 2, 2016

@author: ad
'''
import os
import datetime 
from seql_converter.st25parser.seqlparser import SequenceListing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.template.loader import render_to_string
from django.utils import timezone

from st25parser.seqlparser import SequenceListing as Seql_st25

from sequencelistings.models import SequenceListing  as Seql_st26, Title, Sequence, Feature, Qualifier 

import converter_util

class St25To26Converter(object):
    
    def __init__(self, st25FilePath):
        base = os.path.basename(st25FilePath)
        self.fileName = os.path.splitext(base)[0]
        
        self.seql_st25 = Seql_st25(st25FilePath)
        self.seql_st26 = self.getSequenceListingSt26(self.seql_st25)
        self.titles_st26 = self.getTitlesSt26()
        self.sequences_st26 = self.getSequencesSt26()

    def getSequenceListingSt26(self, aSeql_st25):
#         set first applicant value
        seql_st26_applicantName = '-'
        aSeql_st25_applicant = aSeql_st25.generalInformation.applicant
        if aSeql_st25_applicant:
            seql_st26_applicantName = aSeql_st25_applicant[0]
        
#         set applicationNumber
        applicationNumberAsTuple = converter_util.applicationNumberAsTuple(aSeql_st25.generalInformation.applicationNumber)
        
#         set earliest priority 
        priorityNumberAsTuple = ('', '')
        priorityDate = ''
        
        aSeql_st25_priority = aSeql_st25.generalInformation.priority
        if aSeql_st25_priority:
            
            firstPriority = aSeql_st25_priority[0]
            priorityNumberAsTuple = converter_util.applicationNumberAsTuple(firstPriority[0])
            priorityDateAsString = firstPriority[1]
            priorityDate = datetime.datetime.strptime(priorityDateAsString, '%Y-%m-%d').date()
        
#         create SequenceListing instance
        sl = Seql_st26(
                fileName = self.fileName,
                dtdVersion = '1',
                softwareName = 'prototype',
                softwareVersion = '0.1',
                productionDate = timezone.now().date(),
                  
                applicantFileReference = aSeql_st25.generalInformation.reference,
           
                IPOfficeCode = applicationNumberAsTuple[0],
                applicationNumberText = applicationNumberAsTuple[1],
                filingDate = datetime.datetime.strptime(aSeql_st25.generalInformation.filingDate, '%Y-%m-%d').date(),
               
                earliestPriorityIPOfficeCode = priorityNumberAsTuple[0],
                earliestPriorityApplicationNumberText = priorityNumberAsTuple[1],
                earliestPriorityFilingDate = priorityDate,
               
                applicantName = seql_st26_applicantName,
                applicantNameLanguageCode = 'XX',
                applicantNameLatin = seql_st26_applicantName,
                
                inventorName = '-',
                inventorNameLanguageCode = 'XX',
                inventorNameLatin = '-', 
                
                sequenceTotalQuantity = aSeql_st25.generalInformation.quantity       
                ) 
        
        return sl 

    def getTitlesSt26(self):
        seql_st25_title = self.seql_st25.generalInformation.title
#         assuming is not None 
        seql_st25_titleOneLine = seql_st25_title.replace(r'\s', '')
        t = Title(sequenceListing = self.seql_st26, 
                  inventionTitle = seql_st25_titleOneLine,
                  inventionTitleLanguageCode = 'XX')
        return [t]
#         print 't', t 
     
    def getSequencesSt26(self):
        result = []
        
        for s25 in self.seql_st25.generateSequence():
            residues_st26 = ''
            if s25.molType in ('DNA', 'RNA'):
                residues_st26 = s25.residues_nuc 
            else:
                residues_st26 = converter_util.oneLetterCode(s25.residues_prt)
            
            s26 = Sequence(sequenceListing = self.seql_st26,
                sequenceIdNo = s25.seqIdNo,
                length = s25.length,
                moltype = s25.molType,
                division = 'PAT',
#                 otherSeqId = '-', #optional, so we don't include it in converted sl
                residues = residues_st26)
            result.append(s26)
        return result
            
    def generateXmlFile(self, outputDir):
        xml = render_to_string('conv_xml_template.xml', 
                               {'sequenceListing': self.seql_st26,
                                'titles': self.titles_st26,
                                'sequences': self.sequences_st26,
                                }).encode('utf-8', 'strict')
        xmlFilePath = os.path.join(outputDir, '%s.xml' % self.fileName)
        with open(xmlFilePath, 'w') as gf:
            gf.write(xml) 
            
#         assert os.path.isfile(xmlFilePath)
#         with open(xmlFilePath) as f:
#             print '='*50
#             print f.read()
        
