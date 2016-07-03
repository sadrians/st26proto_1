'''
Created on Jul 2, 2016

@author: ad
'''
import os
import datetime 

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
        self.seql_st26 = self.createInMemorySeql(self.seql_st25)
        
#         applicationNumberRegex = r'(?P<alpha>\D*)(?P<numeric>\d+)'
#         self.applicationNumberPattern = re.compile(applicationNumberRegex)
     
    def getFirstApplicant(self, aListOfApplicants):
        if aListOfApplicants:
            return aListOfApplicants[0]
        else:
            return '-' #TODO: remove hardcoded string

    def createInMemorySeql(self, aSeql_st25):
        applicationNumberAsTuple = converter_util.applicationNumberAsTuple(aSeql_st25.generalInformation.applicationNumber)
        
        priorityNumberAsTuple = ('', '')
        priorityDate = ''
        
        aSeql_st25_priority = aSeql_st25.generalInformation.priority
        if aSeql_st25_priority:
            
            firstPriority = aSeql_st25_priority[0]
            priorityNumberAsTuple = converter_util.applicationNumberAsTuple(firstPriority[0])
            priorityDateAsString = firstPriority[1]
            priorityDate = datetime.datetime.strptime(priorityDateAsString, '%Y-%m-%d').date()
        
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
               
                applicantName = self.getFirstApplicant(aSeql_st25.generalInformation.applicant),
                applicantNameLanguageCode = 'XX',
                applicantNameLatin = self.getFirstApplicant(aSeql_st25.generalInformation.applicant),
               
                inventorName = 'Mary Dupont',
                inventorNameLanguageCode = 'FR',
                inventorNameLatin = 'Mary Dupont', 
                
                sequenceTotalQuantity = aSeql_st25.generalInformation.quantity       
                ) 
        
        return sl 
    
    def createXmlFile(self, sl, outputDir):
        xml = render_to_string('xml_template.xml', {'sequenceListing': sl,
                                }).encode('utf-8', 'strict')
    
        xmlFilePath = os.path.join(outputDir, '%s.xml' % sl.fileName)
        
        with open(xmlFilePath, 'w') as gf:
            gf.write(xml) 
        
# def test_createInMemorySeql():
#     sc = St25To26Converter()
#     sl = sc.createInMemorySeql()
#     print 'Seql'
#     print sl
#     outDir = r'/Users/ad/pyton/projects/test/xml_output'
#     sc.createXmlFile(sl, outDir)
#     print 'Created xml file.'
# #     print 'is editable:', sl.isEditable
# #     print 'applicant reference:', sl.applicantFileReference
# #     print 'Done.'
#     
# test_createInMemorySeql()