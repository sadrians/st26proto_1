from django.db import models
import util 
from django.core.exceptions import ObjectDoesNotExist, ValidationError 
from django.core.validators import RegexValidator 
import re 

regex_nuc = '^[a,c,g,t,u,n,v,k,r,s,b,h,d]{10,}$' #TODO: add the full set of valid chars
regex_prt = '^[A,C,D,E,F,G,H,I,K,L,M,N,O,P,Q,R,S,T,U,V,W,Y,X,J]{4,}$'
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
    
    isEditable = models.BooleanField('Is editable', default=True)
        
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
        self.residues = util.expandFormula(self.residues)
        self.length = len(self.residues)
        super(Sequence, self).save(*args, **kwargs)
        
    def clean(self):
        if self.moltype == 'AA':
            p = pattern_prt  
        else:
            p = pattern_nuc
        self.residues = util.expandFormula(self.residues)
        
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


