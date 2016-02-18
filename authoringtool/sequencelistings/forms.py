'''
Created on Apr 11, 2015

@author: ad
'''

from django.forms import Form, ModelForm, CharField, ChoiceField, PasswordInput
from django.contrib.auth.models import User 
from models import SequenceListing, Title, Sequence, Feature, Qualifier 
import util

class SequenceListingForm(ModelForm):
#     filingDate = DateField()
    
    class Meta:
        model = SequenceListing
        fields = [
                  'fileName', 
                  'applicantFileReference',
                  'IPOfficeCode', 
                  'applicationNumberText', 
                  'filingDate', 
                  'earliestPriorityIPOfficeCode', 
                  'earliestPriorityApplicationNumberText', 
                  'earliestPriorityFilingDate', 
                  'applicantName', 
                  'applicantNameLanguageCode', 
                  'applicantNameLatin', 
                  'inventorName', 
                  'inventorNameLanguageCode', 
                  'inventorNameLatin', 
                  ]
        

class TitleForm(ModelForm):
    class Meta:
        model = Title
        fields = [
                'inventionTitle', 
                'inventionTitleLanguageCode'
                ] 
        
class SequenceForm(ModelForm):
    organism = CharField(label='Organism', max_length=200)

    class Meta:
        model = Sequence
        fields = [
#                   'sequenceListing', 
#                 'sequenceIdNo', 
#                   'length',
                  'moltype',
#                   'division',
#                   'otherSeqId',
                  'residues'] 

class FeatureForm(ModelForm):
    c = []
    def __init__(self, *args, **kwargs):
        moltype = kwargs.pop('mt')
        super(FeatureForm, self).__init__(*args, **kwargs)
        if moltype == 'AA':
            c = util.FEATURE_KEYS_PRT 
        else:
            c = util.FEATURE_KEYS_DNA
 
        self.fields['featureKey'] = ChoiceField(choices=c, label='Feature key')
         
    class Meta:
        model = Feature
        fields = ['featureKey', 'location']   
        
class MultipleFeatureForm(Form):
    featureChoice = []
    qualifierChoice = []
    def __init__(self, *args, **kwargs):
        moltype = kwargs.pop('moltype')
        super(MultipleFeatureForm, self).__init__(*args, **kwargs)
        if moltype == 'AA':
            featureChoice = util.FEATURE_KEYS_PRT 
        else:
            featureChoice = util.FEATURE_KEYS_DNA

        self.fields['featureKey'] = ChoiceField(choices=featureChoice, label='Feature key')
        self.fields['location'] = CharField(max_length=100, label='Location')
        self.fields['qualifierName'] = CharField(max_length=100, label='Qualifier name')
        self.fields['qualifierValue'] = CharField(max_length=100, label='Qualifier value')
        
        
class QualifierForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        c=[]
        feature = kwargs.pop('feature')
        fk = feature.featureKey
        super(QualifierForm, self).__init__(*args, **kwargs)
        if fk in util.QUALIFIER_CHOICE.keys():
            c = util.QUALIFIER_CHOICE.get(fk)
        
        if c:
            self.fields['qualifierName'] = ChoiceField(choices=c, label='Qualifier name') 
        else:
            self.fields['qualifierName'] = CharField(max_length=100, label='Qualifier name')
            
        self.fields.keyOrder = ['qualifierName', 'qualifierValue']  

    class Meta:
        model = Qualifier
        fields = [
                'qualifierName', 
                  'qualifierValue']

class UserForm(ModelForm):
    password = CharField(widget=PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class FormulaForm(Form):
    reg1 = CharField(label='region1', max_length=500)
    x1 = CharField(label='occurence1', max_length=500, help_text='Ex: 4 or 6..20')
    reg2 = CharField(label='region2', max_length=500)
    x2 = CharField(label='occurence2', max_length=500, help_text='Ex: 4 or 6..20')
#     reg3 = CharField(label='region3', max_length=500)
#     x3 = CharField(label='occurence3', max_length=500, help_text='Ex: 4 or 6..20')
#     reg4 = CharField(label='region4', max_length=500)
#     x4 = CharField(label='occurence4', max_length=500, help_text='Ex: 4 or 6..20')
#     reg5 = CharField(label='region5', max_length=500)
#     x5 = CharField(label='occurence5', max_length=500, help_text='Ex: 4 or 6..20')





# class QualifierForm(ModelForm):
# #     qualifierNameChoice = ChoiceField(label='Qualifier name', choices=qualnamelist)
#     
#     class Meta:
#         model = Qualifier
#         fields = ['qualifierName', 
#                   'qualifierValue']
        
    
# from django.forms import ModelForm 
# from django.forms.models import inlineformset_factory 
# 
# from models import SequenceListing, Sequence, Feature, Qualifier 
# 
# class SequenceListingForm(ModelForm):
#     class Meta:
#         model = SequenceListing 
#         
# SequenceFormSet = inlineformset_factory(SequenceListing, Sequence)
# FeatureFormSet = inlineformset_factory(SequenceListing, Feature)
# QualifierFormSet = inlineformset_factory(SequenceListing, Qualifier)


# class FeatureForm(ModelForm):
#     c = []
#     def __init__(self, *args, **kwargs):
#         moltype = kwargs.pop('mt')
# #         print 'featureform moltype:', moltype
# #         print 'featureform moltype:', kwargs.pop('mt')
#         
#         super(FeatureForm, self).__init__(*args, **kwargs)
#         
# #         pass
#         if moltype == 'PRT':
#             c = util.FEATURE_KEYS_PRT 
#         else:
#             c = util.FEATURE_KEYS_DNA
# #     fk = ChoiceField(choices=util.FEATURE_KEYS_DNA)
#         self.fields['fk'] = ChoiceField(choices=c)
# 
#     
#     class Meta:
#         model = Feature
#         fields = [
# #                   'sequence', 
# #                 'featureKey', 
#                   'location']

# class FeatureForm(ModelForm):
#     fk = ChoiceField(choices=util.FEATURE_KEYS_DNA)
#     
#     class Meta:
#         model = Feature
#         fields = [
# #                   'sequence', 
#                   'featureKey', 
#                   'location']
