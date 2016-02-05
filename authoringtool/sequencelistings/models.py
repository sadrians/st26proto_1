from django.db import models
import util 
from django.core.exceptions import ObjectDoesNotExist, ValidationError 
from django.core.validators import RegexValidator 
import re 

# MOLTYPE_CHOICES = [('DNA', 'DNA'), ('RNA', 'RNA'), ('AA', 'AA')]

regex_nuc = '^[a,c,g,t,u,n]{10,}$'
regex_prt = '^[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X]{4,}$'
pattern_nuc = re.compile(regex_nuc)
pattern_prt = re.compile(regex_prt)
        

class SequenceListing(models.Model):
#     xml attributes
    fileName = models.CharField('File name', max_length=100)
    dtdVersion = models.CharField('DTD version', max_length=10)
    softwareName = models.CharField('Software name', max_length=50)
    softwareVersion = models.CharField('Software version', max_length=100)
    productionDate = models.DateField('Production date')

#     xml children (except sequences which are represented as a separate Model)
    
    IPOfficeCode = models.CharField('IP office code', max_length=2)
    applicationNumberText = models.CharField('Application number text', max_length=20)
    filingDate = models.DateField('Filing date')

    applicantFileReference = models.CharField('Applicant file reference', max_length=30)
    
    earliestPriorityIPOfficeCode = models.CharField('Earliest priority IP office code', max_length=2)
    earliestPriorityApplicationNumberText = models.CharField('Earliest priority application number text', max_length=20)
    earliestPriorityFilingDate = models.DateField('Earliest priority filing date')

    applicantName = models.CharField('Applicant name', max_length=200)
    applicantNameLanguageCode = models.CharField('Applicant name language code', max_length=2)
    applicantNameLatin = models.CharField('Applicant name Latin', max_length=200)

    inventorName = models.CharField('Inventor name', max_length=200)
    inventorNameLanguageCode = models.CharField('Inventor name language code', max_length=2)
    inventorNameLatin = models.CharField('Inventor name Latin', max_length=200)
    
    sequenceTotalQuantity = models.IntegerField('Sequence total quantity', default=0)
        
    def __unicode__(self):
        return 'Sequence listing %s' %self.fileName
    
    def getFirstTitle(self):
        return self.title_set.all()[0].inventionTitle
    
class Title(models.Model):
    sequenceListing = models.ForeignKey(SequenceListing) 
    inventionTitle = models.CharField('Invention title', max_length=200)
    inventionTitleLanguageCode = models.CharField('Invention title language code', max_length=2)

    def __unicode__(self):
        return '%s / title %s (%s)' % (self.sequenceListing, 
                                       self.inventionTitle, 
                                       self.inventionTitleLanguageCode)


class Sequence(models.Model): #good
    sequenceListing = models.ForeignKey(SequenceListing)
    
    sequenceIdNo = models.IntegerField('SEQ. ID. NO.', default=0)
    length = models.IntegerField('Length', default=0)
    moltype = models.CharField('Molecule type', max_length=3, choices=util.MOLTYPE_CHOICES)
    division = models.CharField('Division', max_length=3, default='PAT')
    otherSeqId = models.CharField('Other seq ID', max_length=100, default='-')
 
    residues = models.TextField()
 
    def __unicode__(self):
        return str(self.sequenceListing) + ' / seq ' + str(self.sequenceIdNo)
         
    def save(self, *args, **kwargs):
        if not self.pk: # so it's an INSERT, not UPDATE
            self.sequenceIdNo = self.sequenceListing.sequenceTotalQuantity + 1
            self.sequenceListing.sequenceTotalQuantity += 1
            self.sequenceListing.save()
        self.length = len(self.residues)
        super(Sequence, self).save(*args, **kwargs)
        
    def clean(self):
        if self.moltype == 'AA':
            p = pattern_prt  
        else:
            p = pattern_nuc
        if not p.match(self.residues):
            raise ValidationError('Enter a valid residue symbol.')
    
#     this method is to be used only temporarily for Berthold    
    def delete(self, *args, **kwargs):
        subsequentSequencesSet = self.sequenceListing.sequence_set.filter(sequenceIdNo__gt=self.sequenceIdNo)
        super(Sequence, self).delete(*args, **kwargs)
        self.sequenceListing.sequenceTotalQuantity = len(self.sequenceListing.sequence_set.all())
        self.sequenceListing.save()
        for s in subsequentSequencesSet:
            oldSequenceIdNo = int(s.sequenceIdNo)
            s.sequenceIdNo = oldSequenceIdNo - 1
            s.save()
#         print 'SEQ ID NO %i from sequence listing %s has been deleted.' %(self.sequenceIdNo, self.sequenceListing.pk)
    
        
    def inspectSequence(self):
#         print 'sequenceTotalQuantity', self.sequenceListing.sequenceTotalQuantity
        print 'sequenceListing', self.sequenceListing 
        print 'sequenceIdNo', self.sequenceIdNo
        print 'length', self.length
        print 'moltype', self.moltype
        print 'division', self.division
        print 'otherSeqId', self.otherSeqId
        print 'residues', self.residues
        
    def getOrganism(self):
        result = None
        
        sourceFeatureKey = 'source'
        organismQualifierName = 'organism'
        
        if self.moltype == 'AA':
            sourceFeatureKey = 'SOURCE'
            organismQualifierName = 'ORGANISM'
        try:
            sourceFeature = self.feature_set.get(featureKey=sourceFeatureKey)
            organismQualifier = sourceFeature.qualifier_set.get(qualifierName = organismQualifierName)
            
        except ObjectDoesNotExist:
            organismQualifier = None
        
        if organismQualifier:
            result = organismQualifier.qualifierValue
            
        return result
 


# class Sequence(models.Model): #good
#     sequenceListing = models.ForeignKey(SequenceListing)
#     
#     sequenceIdNo = models.IntegerField('SEQ. ID. NO.', default=0)
#     length = models.IntegerField('Length', default=0)
#     moltype = models.CharField('Molecule type', max_length=3, choices=util.MOLTYPE_CHOICES)
#     division = models.CharField('Division', max_length=3, default='PAT')
#     otherSeqId = models.CharField('Other seq ID', max_length=100, default='-')
#  
#     residues = models.TextField()
#  
#     def __unicode__(self):
#         return str(self.sequenceListing) + ' / seq ' + str(self.sequenceIdNo)
#          
#     def save(self, *args, **kwargs):
#         self.sequenceIdNo = self.sequenceListing.sequenceTotalQuantity + 1
#         self.sequenceListing.sequenceTotalQuantity += 1
#         self.sequenceListing.save()
#         super(Sequence, self).save(*args, **kwargs)
#         
#     def inspectSequence(self):
#         print 'sequenceTotalQuantity', self.sequenceListing.sequenceTotalQuantity
#         print 'sequenceListing', self.sequenceListing 
#         print 'sequenceIdNo', self.sequenceIdNo
#         print 'length', self.length
#         print 'moltype', self.moltype
#         print 'division', self.division
#         print 'otherSeqId', self.otherSeqId
#         print 'residues', self.residues
#         
#     def getOrganism(self):
#         result = None
#         
#         sourceFeatureKey = 'source'
#         organismQualifierName = 'organism'
#         
#         if self.moltype == 'AA':
#             sourceFeatureKey = 'SOURCE'
#             organismQualifierName = 'ORGANISM'
#         try:
#             sourceFeature = self.feature_set.get(featureKey=sourceFeatureKey)
#             organismQualifier = sourceFeature.qualifier_set.get(qualifierName = organismQualifierName)
#             
#         except ObjectDoesNotExist:
#             organismQualifier = None
#         
#         if organismQualifier:
#             result = organismQualifier.qualifierValue
#             
#         return result
 
    

class Feature(models.Model):
    sequence = models.ForeignKey(Sequence)
    featureKey = models.CharField('Feature key', max_length=100,
#                                                 choices=DNA_FEATURE_KEY_CHOICES,
                                                )
    location = models.CharField('Location', max_length=100)
   
    def __unicode__(self):
        return str(self.sequence) + ' / ' + self.featureKey  + ' / ' + self.location
        

class Qualifier(models.Model):
    feature = models.ForeignKey(Feature)
    qualifierName = models.CharField('Qualifier name', max_length=100)
    qualifierValue = models.CharField('Qualifier value', max_length=1000)

    def __unicode__(self):
        return str(self.feature) + ' / ' + self.qualifierName
















# class Feature(models.Model):
#     sequence = models.ForeignKey(Sequence)
#     ch = None
#     featureKey = models.CharField('Feature key', max_length=100,
#                                                 choices=ch,
#                                                 )
#     location = models.CharField('Location', max_length=100)
#   
#     def __init__(self, *args, **kwargs):
#         print 'Feature init called'
#         super(Feature, self).__init__(*args, **kwargs)
#         if self.sequence.moltype == 'AA':
#             ch=util.FEATURE_KEYS_PRT
#             print 'Feature init called in aa branch. moltype is: %s' % self.sequence.moltype
#             
#         else:
#             ch=util.FEATURE_KEYS_DNA
#             print 'Feature init called in else branch. moltype is: %s' % self.sequence.moltype
#         print 'so ch is: ', ch
#   
#     def __unicode__(self):
#         return str(self.sequence) + ' / ' + self.featureKey  + ' / ' + self.location
     
#     def setKeyChoices(self, moltype):   
# class Feature(models.Model):
# #     TODO:add the full set of feature key values. For the moment using this as example:
# #     dnaSource = 'source'
# #     dnaMiscFeature = 'miscelaneous feature'
# #     dnaModBase = 'modified base'
# 
# #     DNA_FEATURE_KEY_CHOICES = (
# #         (dnaSource, 'source'),
# #         (dnaMiscFeature, 'misc_feature'),
# #         (dnaModBase, 'mod_base'),
# #     )
#     
#     sequence = models.ForeignKey(Sequence)
#     
# #     def __init__(self,  *args, **kwargs):
# #         moltype = self.sequence.moltype
# #         if moltype == 'AA':
# #             self.c = util.FEATURE_KEYS_PRT
# #         else:
# #             self.c = util.FEATURE_KEYS_DNA 
# #         super(Feature, self).__init__(self,  *args, **kwargs)
#         
#     featureKey = models.CharField('Feature key', max_length=100,
#                                                     choices=c,
#                                                     )
#     location = models.CharField('Location', max_length=100)
#     
#     
#     
#     def __unicode__(self):
#         return str(self.sequence) + ' / ' + self.featureKey  + ' / ' + self.location
