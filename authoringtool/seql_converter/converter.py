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
    
    def generateXmlFile(self, outputDir):
        xml = render_to_string('xml_template.xml', 
                               {'sequenceListing': self.seql_st26,
                                }).encode('utf-8', 'strict')
        xmlFilePath = os.path.join(outputDir, '%s.xml' % self.fileName)
        with open(xmlFilePath, 'w') as gf:
            gf.write(xml) 
            
#         assert os.path.isfile(xmlFilePath)
#         with open(xmlFilePath) as f:
#             print '='*50
#             print f.read()
        
