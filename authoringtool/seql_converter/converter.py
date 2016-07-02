'''
Created on Jul 2, 2016

@author: ad
'''
import os 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.template.loader import render_to_string
from django.utils import timezone

from st25parser.seqlparser import SequenceListing as Seql_st25

from sequencelistings.models import SequenceListing  as Seql_st26, Title, Sequence, Feature, Qualifier 

class St25To26Converter(object):
    
    def __init__(self, st25FilePath):
        base = os.path.basename(st25FilePath)
        self.fileName = os.path.splitext(base)[0]
        
        self.seql_st25 = Seql_st25(st25FilePath)
        
    
    def createInMemorySeql(self):
        
        self.seql_st26 = Seql_st26(
                fileName = 'test_xmlsqlyyy',
                dtdVersion = '1',
                softwareName = 'prototype',
                softwareVersion = '0.1',
                productionDate = timezone.now().date(),
                  
                applicantFileReference = '123',
           
                IPOfficeCode = 'EP',
                applicationNumberText = '2015123456',
                filingDate = timezone.now().date(),
               
                earliestPriorityIPOfficeCode = 'US',
                earliestPriorityApplicationNumberText = '998877',
                earliestPriorityFilingDate = timezone.now().date(),
               
                applicantName = 'John Smith',
                applicantNameLanguageCode = 'EN',
                applicantNameLatin = 'same',
               
                inventorName = 'Mary Dupont',
                inventorNameLanguageCode = 'FR',
                inventorNameLatin = 'Mary Dupont',        
                ) 
        
        return self.seql_st26 
    
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