'''
Created on Jan 28, 2016

@author: ad
Used only for testing. Not suitable for real population!!!
'''
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')

import django
django.setup()

from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier

def clearData():
    Qualifier.objects.all().delete()
    Feature.objects.all().delete()
    Sequence.objects.all().delete()
    Title.objects.all().delete()
    SequenceListing.objects.all().delete()
    print 'Data cleared.'

def populate():
    clearData()
    
    sl1 = SequenceListing.objects.get_or_create(fileName='file1', 
                dtdVersion='1.0', 
                softwareName='ST26 authoring tool prototype', 
                softwareVersion='0.1', 
               productionDate='2016-01-28', 
               IPOfficeCode='EP', 
               applicationNumberText='1511223344.5', 
               filingDate='2016-01-29', 
               applicantFileReference='EP123', 
               earliestPriorityIPOfficeCode='US', 
               earliestPriorityApplicationNumberText='12121212', 
               earliestPriorityFilingDate='2015-01-29', 
               applicantName='applicant1', 
               applicantNameLanguageCode='EN', 
               applicantNameLatin='applicant1', 
               inventorName='inventor1', 
               inventorNameLanguageCode='EN', 
               inventorNameLatin='inventor1', 
               sequenceTotalQuantity=0)[0]
            
    print 'created', sl1 
               
    add_title(sl1, 'title1', 'EN')
    add_title(sl1, 'title2', 'FR')
    
    s1 = add_sequence(sl1, 1, 20, 'DNA', residues='agtcacactttcattca')
    
    s2 = add_sequence(sl1, 2, 10, 'AA', residues='MTGGRASERT')

    f_s1_1 = add_feature(s1, 'source', '1..20')
    f_s1_2 = add_feature(s1, 'allele', '7..8')
    f_s2_1 = add_feature(s2, 'SOURCE', '1..10')
    f_s2_2 = add_feature(s2, 'VARIATION', '5')
    
    q_f_s1_1 = add_qualifier(f_s1_1, 'organism', 'homo sapiens')
    
    q_f_s1_2 = add_qualifier(f_s1_1, 'mol_type', 'genomic DNA')
    q_f_s2_1 = add_qualifier(f_s2_1, 'ORGANISM', 'mus')
    q_f_s2_2 = add_qualifier(f_s2_1, 'MOL_TYPE', 'protein')
    
#     ================================================

    sl2 = SequenceListing.objects.get_or_create(fileName='file2', 
                dtdVersion='1.0', 
                softwareName='ST26 authoring tool prototype', 
                softwareVersion='0.1', 
               productionDate='2016-01-24', 
               IPOfficeCode='EP', 
               applicationNumberText='1299887766.5', 
               filingDate='2014-08-03', 
               applicantFileReference='WO123', 
               earliestPriorityIPOfficeCode='JP', 
               earliestPriorityApplicationNumberText='54545454', 
               earliestPriorityFilingDate='2013-12-29', 
               applicantName='applicant2', 
               applicantNameLanguageCode='EN', 
               applicantNameLatin='applicant2', 
               inventorName='inventor2', 
               inventorNameLanguageCode='EN', 
               inventorNameLatin='inventor2', 
               sequenceTotalQuantity=0)[0]
            
    print 'created', sl2 
               
    add_title(sl2, 'title3', 'EN')
    add_title(sl2, 'title4', 'JP')
    
    s3 = add_sequence(sl2, 1, 30, 'DNA', residues='agtcncttagggacccaacactttcattca')
    
    s4 = add_sequence(sl2, 2, 5, 'AA', residues='MTERT')

    f_s3_1 = add_feature(s3, 'source', '1..30')
    f_s3_2 = add_feature(s3, 'allele', '4..6')
    f_s4_1 = add_feature(s4, 'SOURCE', '1..5')
    f_s4_2 = add_feature(s4, 'VARIATION', '3')
    
    q_f_s3_1 = add_qualifier(f_s3_1, 'organism', 'homo sapiens')
    
    q_f_s3_2 = add_qualifier(f_s3_1, 'mol_type', 'genomic DNA')
    q_f_s4_1 = add_qualifier(f_s4_1, 'ORGANISM', 'mus')
    q_f_s4_2 = add_qualifier(f_s4_1, 'MOL_TYPE', 'protein')

    print 'Done with population script.'

def add_title(sl, it, itlc):
    t = Title.objects.get_or_create(sequenceListing=sl, 
                                    inventionTitle=it, 
                                    inventionTitleLanguageCode=itlc)[0]
    print 'created', t
    return t 

def add_sequence(sequenceListing, sequenceIdNo, length, moltype, residues):
    s = Sequence.objects.get_or_create(sequenceListing=sequenceListing, 
                sequenceIdNo=sequenceIdNo, length=length, 
                moltype=moltype, residues=residues)[0]
    print 'created', s 
    return s 

def add_feature(sequence, featureKey, location):
    f = Feature.objects.get_or_create(sequence=sequence, 
                featureKey=featureKey, location=location)[0]
    
    print 'created', f
    return f 

def add_qualifier(feature, qualifierName, qualifierValue):
    q = Qualifier.objects.get_or_create(feature=feature, 
                qualifierName=qualifierName, 
                qualifierValue=qualifierValue)[0]
    
    print 'created', q 
    return q 

def mytest():
    sls = SequenceListing.objects.all()
    
    print sls 
    sl1 = sls[0]
    print sl1.title_set.all()[0].inventionTitle

# Start execution here!
if __name__ == '__main__':
    print "Starting Creator population script..."
    populate()
#     clearData()

#     mytest()