'''
Created on Jul 2, 2016

@author: ad
'''
import os
import datetime 
from seql_converter.st25parser.seqlparser import SequenceListing
# import converter_util as cu 

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.template.loader import render_to_string
from django.utils import timezone

from st25parser.seqlparser import SequenceListing as Seql_st25
from st25parser import seqlutils

from sequencelistings.models import SequenceListing  as Seql_st26, Title, Sequence, Feature, Qualifier 

import converter_util

class St25To26Converter(object):
    
    def __init__(self, st25FilePath):
        base = os.path.basename(st25FilePath)
        self.fileName = os.path.splitext(base)[0]
        
        self.seql_st25 = Seql_st25(st25FilePath)
        self.seql_st26 = self.getSequenceListingSt26(self.seql_st25)
        self.setTitleSt26()
        self.setSequencesSt26()
        
    def getSequenceListingSt26(self, aSeql_st25):

#         set first applicant value
        aSeql_st25_applicant = aSeql_st25.generalInformation.applicant
        if aSeql_st25_applicant:
            seql_st26_applicantName = aSeql_st25_applicant[0]
        else:
            seql_st26_applicantName = seqlutils.DEFAULT_STRING

#         set applicationNumber as a tuple
        applicationNumberAsTuple = converter_util.applicationNumberAsTuple(aSeql_st25.generalInformation.applicationNumber)

#         set filingDate
        fd = self.seql_st25.generalInformation.filingDate
        if fd != seqlutils.DEFAULT_STRING:
            filingDateAsString = fd 
        else:
            filingDateAsString = converter_util.DEFAULT_DATE_STRING
        
#         set earliest priority 
        priorityNumberAsTuple = ('', '')
        priorityDate = converter_util.DEFAULT_DATE_STRING
                
        aSeql_st25_priority = aSeql_st25.generalInformation.priority
        
        if aSeql_st25_priority:
            firstPriority = aSeql_st25_priority[0]
            priorityNumberAsTuple = converter_util.applicationNumberAsTuple(firstPriority[0])
            priorityDateAsString = firstPriority[1]
            priorityDate = datetime.datetime.strptime(priorityDateAsString, '%Y-%m-%d').date()
        
#         create SequenceListing instance
        sl = Seql_st26(
                fileName = '%s_ST26' % self.fileName,
                dtdVersion = '1',
                softwareName = 'prototype',
                softwareVersion = '0.1',
                productionDate = timezone.now().date(),
                  
                applicantFileReference = aSeql_st25.generalInformation.reference,
#                 applicantFileReference = applicantFileReference,
                
                IPOfficeCode = applicationNumberAsTuple[0],
                applicationNumberText = applicationNumberAsTuple[1],
                filingDate = datetime.datetime.strptime(filingDateAsString, '%Y-%m-%d').date(),
                earliestPriorityIPOfficeCode = priorityNumberAsTuple[0],
                earliestPriorityApplicationNumberText = priorityNumberAsTuple[1],
                earliestPriorityFilingDate = priorityDate,
               
                applicantName = seql_st26_applicantName,
                applicantNameLanguageCode = converter_util.DEFAULT_CODE,
                applicantNameLatin = seql_st26_applicantName,
                
                inventorName = '-',
                inventorNameLanguageCode = converter_util.DEFAULT_CODE,
                inventorNameLatin = '-', 
                
#                 sequenceTotalQuantity = aSeql_st25.generalInformation.quantity       
                ) 
        sl.save()
        return sl 

    def setTitleSt26(self):
        seql_st25_title = self.seql_st25.generalInformation.title
#         assuming is not None 
        seql_st25_titleOneLine = seql_st25_title.replace(r'\s', '')
        t = Title(sequenceListing = self.seql_st26, 
                  inventionTitle = seql_st25_titleOneLine,
                  inventionTitleLanguageCode = converter_util.DEFAULT_CODE)
        t.save()
        return [t]
    
    def setSequencesSt26(self):
        
        for s25 in self.seql_st25.generateSequence():
            residues_st26 = ''
            if s25.molType in ('DNA', 'RNA'):
                molType_st26 = s25.molType
                sourceKey = 'source'
                organismQualifierName = 'organism'
                mol_typeQualifierName = 'mol_type'
                mol_typeQualifierValue = 'genomic %s' % s25.molType
                noteQualifierName = 'note'
                residues_st26 = s25.residues_nuc 
            else:
                molType_st26 = 'AA'
                sourceKey = 'SOURCE'
                organismQualifierName = 'ORGANISM'
                mol_typeQualifierName = 'MOL_TYPE'
                mol_typeQualifierValue = 'protein'
                noteQualifierName = 'NOTE'
                residues_st26 = converter_util.oneLetterCode(s25.residues_prt)
            
            s26 = Sequence(sequenceListing = self.seql_st26,
                sequenceIdNo = s25.seqIdNo,
                length = s25.length,
                moltype = molType_st26,
                division = 'PAT',
#                 otherSeqId = '-', #optional, so we don't include it in converted sl
                residues = residues_st26)
            
            s26.save()
            
            sourceFeature = Feature(sequence=s26, 
                                    featureKey = sourceKey,
                                    location = '1..%s' % s26.length)
            sourceFeature.save()
            
            organismQualifier = Qualifier(feature=sourceFeature,
                                          qualifierName=organismQualifierName,
                                          qualifierValue=s25.organism)
            organismQualifier.save()
            
            mol_typeQualifier = Qualifier(feature=sourceFeature,
                                          qualifierName=mol_typeQualifierName,
                                          qualifierValue=mol_typeQualifierValue)
            mol_typeQualifier.save()
            
            for f in s25.features:
                
                currentFeature = Feature(sequence=s26,
                                         featureKey = f.key,
                                         location = f.location)
                currentFeature.save()
                if f.key != seqlutils.DEFAULT_STRING:
                    currentQualifier = Qualifier(feature=currentFeature,
                                              qualifierName=noteQualifierName,
                                              qualifierValue=f.description)
                    currentQualifier.save()
                
                if f.key == 'CDS':
                    translationQualifierValue = converter_util.oneLetterCode(f.translation)
                    translationQualifier = Qualifier(feature=currentFeature,
                                          qualifierName='translation',
                                          qualifierValue=translationQualifierValue)
                    translationQualifier.save()
                         
    def generateXmlFile(self, outputDir):
#         strftime('%Y-%m-%d') dates are not in the prescribed ST.26 format!!!!!
        self.seql_st26.productionDate = timezone.now()
        self.seql_st26.save()
        xml = render_to_string('xml_template.xml', 
                               {'sequenceListing': self.seql_st26,
                                }).encode('utf-8', 'strict')
        xmlFilePath = os.path.join(outputDir, '%s.xml' % self.seql_st26.fileName)
        with open(xmlFilePath, 'w') as gf:
            gf.write(xml) 
            
        self.seql_st26.delete()
        print 'Converted to xml file', xmlFilePath 
        return xmlFilePath

        
