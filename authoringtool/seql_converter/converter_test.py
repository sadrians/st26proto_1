'''
Created on Jul 2, 2016

@author: ad
'''
from django.test import TestCase
import os 
from django.conf import settings 
from converter import St25To26Converter 
import sequencelistings.util as slsu
import converter_util

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

class Test_St25To26Converter(TestCase):
    @classmethod
    def getAbsPath(cls, aFileName):
        return os.path.join(settings.BASE_DIR, 'seql_converter', 
                            'st25parser', 'testData', aFileName)
    def setUp(self):
        self.f1 = self.getAbsPath('file1.txt')
        self.f1004 = self.getAbsPath('WO2012-001004-001.zip.txt')
        self.f33_1 = self.getAbsPath('file33_1.txt')
        self.f80 = self.getAbsPath('file80.txt')
        self.f6550 = self.getAbsPath('WO2012-006550-001.zip.txt')
        self.f63219 = self.getAbsPath('WO2012-063219-001.zip.txt')
         
        self.sc1 = St25To26Converter(self.f1)
        self.sc1004 = St25To26Converter(self.f1004)
        self.sc33_1 = St25To26Converter(self.f33_1)
        self.sc80 = St25To26Converter(self.f80)
        self.sc6550 = St25To26Converter(self.f6550)
        self.sc63219 = St25To26Converter(self.f63219) 
        
#     @classmethod
#     def setUpClass(cls):
#         cls.f1 = cls.getAbsPath('file1.txt')
#         cls.f1004 = cls.getAbsPath('WO2012-001004-001.zip.txt')
#         cls.f33_1 = cls.getAbsPath('file33_1.txt')
#         cls.f80 = cls.getAbsPath('file80.txt')
#         cls.f6550 = cls.getAbsPath('WO2012-006550-001.zip.txt')
#         cls.f63219 = cls.getAbsPath('WO2012-063219-001.zip.txt')
#          
#         cls.sc1 = St25To26Converter(cls.f1)
#         cls.sc1004 = St25To26Converter(cls.f1004)
#         cls.sc33_1 = St25To26Converter(cls.f33_1)
#         cls.sc80 = St25To26Converter(cls.f80)
#         cls.sc6550 = St25To26Converter(cls.f6550)
#         cls.sc63219 = St25To26Converter(cls.f63219)  
        
    def tearDown(self):
        pass
 
    @withMethodName
    def test_getSequenceListingSt26(self):
         
        self.assertEqual('file1', self.sc1.fileName)
         
        self.assertEqual('file1_ST26', self.sc1.seql_st26.fileName)
        self.assertEqual('34246761601', self.sc1.seql_st26.applicantFileReference)
         
        self.assertEqual(converter_util.DEFAULT_CODE, self.sc1.seql_st26.IPOfficeCode)
        self.assertEqual('61536464', self.sc1.seql_st26.applicationNumberText)
         
        self.assertEqual(converter_util.DEFAULT_CODE, self.sc80.seql_st26.IPOfficeCode)
        self.assertEqual('Not yet assigned', self.sc80.seql_st26.applicationNumberText)
         
        self.assertEqual(2012, self.sc1.seql_st26.filingDate.year)
        self.assertEqual(9, self.sc1.seql_st26.filingDate.month)
        self.assertEqual(19, self.sc1.seql_st26.filingDate.day)
        
        self.assertEqual(None, self.sc33_1.seql_st26.filingDate)
        
        self.assertEqual(1900, self.sc6550.seql_st26.filingDate.year)
        self.assertEqual(1, self.sc6550.seql_st26.filingDate.month)
        self.assertEqual(1, self.sc6550.seql_st26.filingDate.day)
        
        self.assertEqual('', self.sc1004.seql_st26.IPOfficeCode)
        self.assertEqual('', self.sc1004.seql_st26.applicationNumberText)
        self.assertEqual(None, self.sc1004.seql_st26.filingDate)
        
        self.assertEqual('', self.sc63219.seql_st26.IPOfficeCode)
        self.assertEqual('', self.sc63219.seql_st26.applicationNumberText)
        self.assertEqual(None, self.sc63219.seql_st26.filingDate)
         
        self.assertEqual(converter_util.DEFAULT_CODE, self.sc1.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61536558 - prio1', self.sc1.seql_st26.earliestPriorityApplicationNumberText)
         
        self.assertEqual('US', self.sc80.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('61/678,367', self.sc80.seql_st26.earliestPriorityApplicationNumberText)
         
        self.assertEqual(2001, self.sc1.seql_st26.earliestPriorityFilingDate.year)
        self.assertEqual(1, self.sc1.seql_st26.earliestPriorityFilingDate.month)
        self.assertEqual(1, self.sc1.seql_st26.earliestPriorityFilingDate.day)
        
        self.assertEqual('', self.sc63219.seql_st26.earliestPriorityIPOfficeCode)
        self.assertEqual('', self.sc63219.seql_st26.earliestPriorityApplicationNumberText)
        self.assertEqual(None, self.sc63219.seql_st26.earliestPriorityFilingDate)
 
        self.assertEqual('OPX Biotechnologies, Inc.', self.sc1.seql_st26.applicantName)
        self.assertEqual(converter_util.DEFAULT_CODE, self.sc1.seql_st26.applicantNameLanguageCode)
        self.assertEqual('', self.sc1.seql_st26.applicantNameLatin)
        
        self.assertEqual('', self.sc1.seql_st26.inventorName)
        self.assertEqual('', self.sc1.seql_st26.inventorNameLanguageCode)
        self.assertEqual('', self.sc1.seql_st26.inventorNameLatin)
 
        self.assertEqual(4, self.sc1.seql_st26.sequenceTotalQuantity)
        
        self.assertEqual(11, self.sc63219.seql_st26.sequenceTotalQuantity)
         
    @withMethodName
    def test_setTitleSt26(self):
        t = self.sc1.seql_st26.title_set.all()[0]
        self.assertEqual('COMPOSITIONS AND METHODS REGARDING DIRECT NADH UTILIZATION TO PRODUCE 3-HYDROXYPROPIONIC ACID AND RELATED CHEMICALS AND PRODUCTS', 
                         t.inventionTitle)
        self.assertEqual(converter_util.DEFAULT_CODE, t.inventionTitleLanguageCode)
         
    @withMethodName
    def test_setSequencesSt26(self):
 
        sequences = self.sc1.seql_st26.sequence_set.all()
        self.assertEqual(4, sequences.count())
         
        s2 = sequences.get(sequenceIdNo=2)
        s4 = sequences.get(sequenceIdNo=4)
         
        self.assertEqual('DNA', s2.moltype)
        self.assertEqual('AA', s4.moltype)
         
        self.assertEqual('ttgaccaagctggggaccccggtcccttgggaccagtggcagaggagtc', s2.residues)
         
        features_s2 = s2.feature_set.all()
         
        self.assertEqual("3'clip", features_s2[1].featureKey)
        self.assertEqual("1..30", features_s2[1].location)
                
        sequences_1004 = self.sc1004.seql_st26.sequence_set.all()
        sequence_1004_1 = sequences_1004.get(sequenceIdNo=1)
        sequence_1004_7 = sequences_1004.get(sequenceIdNo=7)
        
        self.assertEqual(903, sequence_1004_1.length)
        features_1004_1 = sequence_1004_1.feature_set.all()
        
        self.assertEqual("CDS", features_1004_1[1].featureKey)
        self.assertEqual("(1)..(903)", features_1004_1[1].location)
        
#         test that feature description missing is not converted to empty element
        s1 = sequences.get(sequenceIdNo=1)
        features_s1 = s1.feature_set.all()
        for f in features_s1:
            qualifiers = f.qualifier_set.all()
            for q in qualifiers:
                self.assertFalse(q.qualifierName in ['note', "NOTE"])
        
        features_s4 = s4.feature_set.all()
        for f in features_s4:
            qualifiers = f.qualifier_set.all()
            for q in qualifiers:
                if q.qualifierName == 'NOTE':
                    exp = 'influenza virus A hemagglutinin subtype H9'
                    self.assertEqual(exp, q.qualifierValue)
                

#         ============== tests for mixed mode ==================================   
        translQualifier_seq1 = features_1004_1[1].qualifier_set.all()[0]
        self.assertEqual("translation", translQualifier_seq1.qualifierName)
        
        translQualValue_exp = converter_util.oneLetterCode(self.sc1004.seql_st25.sequences[0].residues_prt)
        self.assertEqual(translQualValue_exp, translQualifier_seq1.qualifierValue)
        
        features_1004_7 = sequence_1004_7.feature_set.all()
        
        self.assertEqual("CDS", features_1004_7[1].featureKey)
        self.assertEqual("(1)..(84)", features_1004_7[1].location)
        
        translQualifier7_1 = features_1004_7[1].qualifier_set.all()[0]
        self.assertEqual("translation", translQualifier7_1.qualifierName)
        
        translQualifier7_2 = features_1004_7[2].qualifier_set.all()[0]
        self.assertEqual("translation", translQualifier7_2.qualifierName)
        
        translation1 = converter_util.oneLetterCode('MetLysLysSerLeuValLeuLysAlaSerValAlaValAlaThrLeuValProMetLeuSerPheAlaAlaGluGlyGluPhe')
        translation2 = converter_util.oneLetterCode('AspProAlaLysAlaAlaPheAspSerLeuGlnAlaSerAlaThrGluTyrIleGlyTyrAlaTrpAlaMetValValValIleValGlyAlaThrIleGlyIleLysLeuPheLysLysPheThrSerLysAlaSer')
        
        self.assertEqual(translation1, translQualifier7_1.qualifierValue)
        self.assertEqual(translation2, translQualifier7_2.qualifierValue)
        
#         ============== tests for simple feature conversion ==================================   
        sourceFeature_1004_7 = features_1004_7[0]
        noteQual = sourceFeature_1004_7.qualifier_set.get(qualifierName='note')
        self.assertEqual('pc89 major coat protein PVIII', noteQual.qualifierValue)
    
#     @withMethodName
#     def test_getTranslations(self):
#         sequence_1004_1 = self.sc1004.seql_st25.getSequenceFromFile(self.f1004, 1)
#         sequence_1004_2 = self.sc1004.seql_st25.getSequenceFromFile(self.f1004, 2)
#         sequence_1004_7 = self.sc1004.seql_st25.getSequenceFromFile(self.f1004, 7)
#         
#         t1_1_exp = r'MetLysArgValIleThrLeuPheAlaValLeuLeuMetGlyTrpSerValAsnAlaTrpSerPheAlaCysLysThrAlaAsnGlyThrAlaIleProIleGlyGlyGlySerAlaAsnValTyrValAsnLeuAlaProAlaValAsnValGlyGlnAsnLeuValValAspLeuSerThrGlnIlePheCysHisAsnAspTyrProGluThrIleThrAspTyrValThrLeuGlnArgGlyAlaAlaTyrGlyGlyValLeuSerSerPheSerGlyThrValLysTyrAsnGlySerSerTyrProPheProThrThrSerGluThrProArgValValTyrAsnSerArgThrAspLysProTrpProValAlaLeuTyrLeuThrProValSerSerAlaGlyGlyValAlaIleLysAlaGlySerLeuIleAlaValLeuIleLeuArgGlnThrAsnAsnTyrAsnSerAspAspPheGlnPheValTrpAsnIleTyrAlaAsnAsnAspValValValProThrGlyGlyCysAspValSerAlaArgAspValThrValThrLeuProAspTyrProGlySerValProIleProLeuThrValTyrCysAlaLysSerGlnAsnLeuGlyTyrTyrLeuSerGlyThrThrAlaAspAlaGlyAsnSerIlePheThrAsnThrAlaSerPheSerProAlaGlnGlyValGlyValGlnLeuThrArgAsnGlyThrIleIleProAlaAsnAsnThrValSerLeuGlyAlaValGlyThrSerAlaValSerLeuGlyLeuThrAlaAsnTyrAlaArgThrGlyGlyGlnValThrAlaGlyAsnValGlnSerIleIleGlyValThrPheValTyrGln'
#         
#         translations1_act = self.sc1004.getTranslations(sequence_1004_1)
#         self.assertEqual(t1_1_exp, translations1_act[0])
#         
#         translations2_act = self.sc1004.getTranslations(sequence_1004_2)
#         
#         self.assertEqual([], translations2_act)
#         
#         t7_1_exp = r'MetLysLysSerLeuValLeuLysAlaSerValAlaValAlaThrLeuValProMetLeuSerPheAlaAlaGluGlyGluPhe'
#         t7_2_exp = r'AspProAlaLysAlaAlaPheAspSerLeuGlnAlaSerAlaThrGluTyrIleGlyTyrAlaTrpAlaMetValValValIleValGlyAlaThrIleGlyIleLysLeuPheLysLysPheThrSerLysAlaSer'
#         
#         translations7_act = self.sc1004.getTranslations(sequence_1004_7)
#         self.assertEqual(t7_1_exp, translations7_act[0])
#         self.assertEqual(t7_2_exp, translations7_act[1])
         
    @withMethodName
    def test_generateXmlFile(self):
        od = os.path.join(settings.BASE_DIR, 'seql_converter', 'test', 'output')
         
        self.sc1.generateXmlFile(od)
        filePath1 = os.path.join(od, '%s.xml' % self.sc1.seql_st26.fileName)
        
        self.sc1004.generateXmlFile(od)
        filePath1004 = os.path.join(od, '%s.xml' % self.sc1004.seql_st26.fileName)
         
        self.assertTrue(os.path.isfile(filePath1))
        self.assertTrue(slsu.validateDocumentWithDtd(filePath1, slsu.XML_DTD_PATH))
        
        with open(filePath1, 'r') as f1:
            s1 = f1.read()
            self.assertEqual(1, s1.count('<ST26SequenceListing'))
            self.assertEqual(4, s1.count('<SequenceData'))
            self.assertEqual(4, s1.count('<INSDSeq_feature-table>'))
            self.assertEqual(5, s1.count('<INSDFeature>'))
            self.assertEqual(4, s1.count('<INSDFeature_quals>'))
            self.assertEqual(9, s1.count('<INSDQualifier>'))
        with open(filePath1004, 'r') as f1004:
            s1004 = f1004.read()    
            self.assertEqual(0, s1004.count('<ApplicationIdentification>'))
            self.assertEqual(1, s1004.count('<ApplicationNumberText'))
            self.assertEqual(1, s1004.count('<FilingDate>'))
#             f1_0 2q
#             f1_1 1q
#             f2_0 2q
#             f3_0 3q
#             f3_1 2q
#             f4_0 3q
#             f5_0 2q
#             f5_1 1q
#             f6_0 2q
#             f7_0 3q
#             f7_1 1q
#             f7_2 1q
#             f8_0 3q
#             f9_0 3q
#             f10_0 3q
#             f11_0 3q
#             f12_0 3q
#             f13_0 3q
#             f14_0 3q
#             f15_0 3q
#             f16_0 3q
#             f17_0 3q
            self.assertEqual(22, s1004.count('<INSDFeature>'))
            self.assertEqual(22, s1004.count('<INSDFeature_quals>'))
            self.assertEqual(53, s1004.count('<INSDQualifier>'))
#             no empty elements
            self.assertEqual(0, s1004.count('></'))

#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
#             self.assertEqual(, s.count('<'))
            

#         self.assertTrue(slsu.validateDocumentWithSchema(filePath1, slsu.XML_SCHEMA_PATH))
