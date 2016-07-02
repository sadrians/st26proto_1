'''
Created on Jun 18, 2016

@author: ad
'''
import os
# from fileinput import filename
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()

from django.utils import timezone
from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier
from populate_db import add_title, copySequenceListing

from sequencelistings.util import expandFormula 

def myCopyScript(aFileName):
    sl = SequenceListing.objects.filter(fileName=aFileName)[0] 
    copySequenceListing(sl)
    print 'Done with copying', aFileName


def createInMemorySeql():
    sl = SequenceListing(
            fileName = 'test_xmlsqlxxx',
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
    
    return sl 

def test_createInMemorySeql():
    sl = createInMemorySeql()
    print 'Seql'
    print sl
    print 'is editable:', sl.isEditable
    print 'applicant reference:', sl.applicantFileReference
    print 'Done.'
    
# test_createInMemorySeql()
# seqls = SequenceListing.objects.all()
# print seqls 
# for sl in seqls:
#     print sl
#     print 'is editable:', sl.isEditable





# myCopyScript('Invention_SEQL')

# print 'GGGX'*100
# print expandFormula('cg(agg)4..7')