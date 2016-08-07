# -*- coding: utf-8 -*-
'''
Created on 3 Sep 2015
Updated on 2 Jul 2016
@author: ad
'''
import django
django.setup()
# 
from django.conf import settings
import unittest
import os

from seqlparser_new import SequenceListing
import seqlutils

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

def getAbsPath(aFileName):
    return os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 'testData', aFileName)
        
class TestSequenceListing(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        
        cls.sl1 = SequenceListing(getAbsPath('file1.txt'))
        cls.sl2 = SequenceListing(getAbsPath('file2.txt'))
        cls.sl5 = SequenceListing(getAbsPath('file5.txt'))
        cls.sl6 = SequenceListing(getAbsPath('file6.txt'))
        cls.sl32 = SequenceListing(getAbsPath('file32.txt'))
        cls.sl32_1 = SequenceListing(getAbsPath('file32_1.txt'))
        cls.sl32_2 = SequenceListing(getAbsPath('file32_2.txt'))
        cls.sl32_3 = SequenceListing(getAbsPath('file32_3.txt'))
        cls.sl32_4 = SequenceListing(getAbsPath('file32_4.txt'))
        cls.sl32_8 = SequenceListing(getAbsPath('file32_8.txt'))
        cls.sl32_9 = SequenceListing(getAbsPath('file32_9.txt'))
        cls.sl33_1 = SequenceListing(getAbsPath('file33_1.txt'))
        cls.sl1004 = SequenceListing(getAbsPath('WO2012-001004-001.zip.txt'))
        cls.sl6083_1 = SequenceListing(getAbsPath('WO2012-006083_1.txt'))
        cls.sltest_1_feature = SequenceListing(getAbsPath('test_1_feature.txt'))
        
        
        cls.sequences1 = [seq for seq in cls.sl1.generateSequence()]
        cls.seq1_1 = cls.sequences1[0]
        cls.seq1_2 = cls.sequences1[1]
        cls.seq1_3 = cls.sequences1[2]
        
        sequences2 = [seq for seq in cls.sl2.generateSequence()]
        cls.seq2_3 = sequences2[2]

        cls.sequences5 = [seq for seq in cls.sl5.generateSequence()]
        cls.seq5_5 = cls.sequences5[4]
        cls.seq5_37 = cls.sequences5[36]
        cls.seq5_40 = cls.sequences5[39]
        
        sequences6 = [seq for seq in cls.sl6.generateSequence()]
        cls.seq6_4 = sequences6[3]
        
        sequences32 = [seq for seq in cls.sl32.generateSequence()]
        cls.seq32_5 = sequences32[4]
        
        cls.sequences32_8 = [seq for seq in cls.sl32_8.generateSequence()]
        
        cls.sequences33_1 = [seq for seq in cls.sl33_1.generateSequence()]
        cls.seq33_1_1 = cls.sequences33_1[0]
        cls.seq33_1_2 = cls.sequences33_1[1]
        
        sequences1004 = [seq for seq in cls.sl1004.generateSequence()]
        cls.seq1004_1 = sequences1004[0]
        cls.seq1004_7 = sequences1004[6]
        
        cls.sequences6083_1 = [seq for seq in cls.sl6083_1.generateSequence()]
        cls.sl6083_1_seq_1 = cls.sequences6083_1[0] # 212 is RNA
        cls.sl6083_1_seq_2 = cls.sequences6083_1[1] # 212 is DNA instead of RNA
        cls.sl6083_1_seq_3 = cls.sequences6083_1[2] # 212 is abc instead of RNA
        cls.sl6083_1_seq_4 = cls.sequences6083_1[3] # 212 is missing
        
        cls.sltest_1_feature_sequences = [seq for seq in cls.sltest_1_feature.generateSequence()]

#         cls.seq6_1 = SequenceListing.getSequenceFromFile(infilename6, 1)
#         cls.seq6_4 = SequenceListing.getSequenceFromFile(infilename6, 4) # skip code
#         cls.seq32_5 = SequenceListing.getSequenceFromFile(infilename32, 5)
#  
#         cls.seq33_1_2 = SequenceListing.getSequenceFromFile(infilename33_1, 2)
  
#         # cls.seq016177_3 = cls.sl016177.sequences[2]
    
    @withMethodName
    def test_parsePriorities(self):
        ins = '<150>  61536558 - prio1\r\n\r\n<151>  2001-01-01\r\n\r\n'
        exp = [('61536558 - prio1', '2001-01-01')]
        self.assertEqual(exp, seqlutils.parsePriorities(ins))
        
#         p = """
# #<150>   61536558
# # 
# # <151>  2011-09-19
# # 
# # <150>  61536539
# # 
# # <151>  2012-09-19
# # 
# # 
# # 
# # <150>  61536580
# # 
# # <151>  2013-09-19
# #         """
#         res = seqlutils.parsePriorities(p)
#         self.assertListEqual([('61536558', '2011-09-19'), 
#                               ('61536539', '2012-09-19'), 
#                               ('61536580', '2013-09-19')], res)
    
    @withMethodName
    def test_isSeql(self):
        self.assertTrue(self.sl1.isSeql)
        self.assertTrue(self.sl5.isSeql)
        self.assertTrue(self.sltest_1_feature.isSeql)
#         self.assertTrue(not self.sl_input_no_seql.isSeql)
#         self.assertTrue(not SequenceListing('abc').isSeql)
         
        # test if closing bracket missing from 120
#         self.assertTrue(self.sl32_5.isSeql)
        # what's special with this sl? why do we need this test?
#         self.assertTrue(self.sl058291.isSeql)
#         self.assertTrue(self.sl6503.isSeql)
    
    @withMethodName
    def test_seqlHeader(self):
        seqlHeader_exp = '''                         SEQUENCE LISTING\r\n\r\n'''
        self.assertEqual(seqlHeader_exp, self.sl5.seqlHeader_raw)
        self.assertEqual('SEQUENCE LISTING', self.sl1.seqlHeader)
        self.assertEqual('SEQUENCE LISTING', self.sl5.seqlHeader)
    
    @withMethodName
    def test_applicant(self):
           
        self.assertEqual(['OPX Biotechnologies, Inc.'], self.sl1.applicant)
        self.assertEqual(['OPX Biotechnologies, Inc.', 'Universite Paris II'], self.sl2.applicant)
#         self.assertEqual(['Merck Sharp & Dohme Corp.',
#                           'Chen, Zhiyu',
#                           'Lancaster, Thomas M.',
#                           'Zion, Todd C.'], self.sl33_1.applicant)
#         # item110 empty
        self.assertEqual([], self.sl32_9.applicant)
#         #applicant with one line
        self.assertEqual(self.sl32.applicant, ["OPX Biotechnologies, Inc."])
#         #applicant with 2 lines
        self.assertEqual(self.sl32_1.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
#         #applicant with 2 lines, item120 missing
        self.assertEqual(self.sl32_2.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
#         applicant with non ASCII chars
#         a = self.sl41670.applicant
#         self.assertEqual('Technische Universität Dortmund and Heinrich-Heine', a[0])
#         self.assertEqual('Universität Düsseldorf', a[1])

    @withMethodName
    def test_title(self):
        self.assertEqual(self.sl32.title, "COMPOSITIONS AND METHODS REGARDING DIRECT NADH UTILIZATION TO PRODUCE 3-HYDROXYPROPIONIC ACID AND RELATED CHEMICALS AND PRODUCTS")
        # item120 missing
        self.assertEqual(seqlutils.DEFAULT_STRING, self.sl32_2.title)
        # item120 empty
        self.assertEqual('', self.sl32_3.title)
    
    @withMethodName
    def test_reference(self):
        reference_exp = """<130>  BIOA-006/01WO\r\n\r\n"""
        self.assertEqual(reference_exp, self.sl5.reference_raw)
        
        self.assertEqual(None, self.sl5.applicationNumber_raw)
        self.assertEqual("34246761601", self.sl32.reference)
        #reference element is missing
        self.assertEqual(seqlutils.DEFAULT_STRING, self.sl2.reference)
  
    @withMethodName
    def test_applicationNumber(self):
        self.assertEqual("61536464", self.sl32.applicationNumber)
  
    @withMethodName
    def test_filingDate(self):
        self.assertEqual(None, self.sl5.filingDate_raw)
        self.assertEqual(self.sl32.filingDate, "2012-09-19")
    
    @withMethodName
    def test_priorities(self):
        priorities_exp = '<150>  US 61/677,959\r\n<151>  2012-07-31\r\n\r\n'
        self.assertEqual(priorities_exp, self.sl5.priorities_raw)
        
        pr32 = self.sl32.priorities
        self.assertEqual(3, len(pr32))
           
        self.assertListEqual([('61536558 - prio1', '2001-01-01'), 
                              ('61536539 - prio2', '2002-02-02 - pd'),
                              ('61536539 - prio3', '2003-03-03')], 
                             self.sl1.priorities)
        self.assertListEqual([], self.sl2.priorities)
        
        self.assertEqual(len(self.sl32_4.priorities), 3)

        actual_pn = [self.sl32_4.priorities[i][0] for i in range(3)]
        expected_pn = ['61536558', '61536539', '61536540']
        self.assertEqual(actual_pn, expected_pn)
# 
        actual_pd = [self.sl32_4.priorities[i][1] for i in range(3)]
        expected_pd = ['2011-09-19x1', '2011-09-19x2', '2011-09-19x3']
        self.assertEqual(actual_pd, expected_pd)

        #no priority
        self.assertEqual(len(self.sl2.priorities), 0)
        
    @withMethodName
    def test_quantity(self):
        quantity_exp = """<160>  39    \r\n\r\n"""
        self.assertEqual(quantity_exp, self.sl5.quantity_raw)
        
        self.assertEqual('5', self.sl32.quantity)
  
    @withMethodName
    def test_software(self):
        software_exp = """<170>  PatentIn version 3.5\r\n\r\n"""
        self.assertEqual(software_exp, self.sl5.software_raw)
        
        self.assertEqual(self.sl32.software, "PatentIn version 3.5")
    
    @withMethodName
    def test_Sequence(self):    
        self.assertEqual(40, len(self.sequences5))
        self.assertEqual(1, len(self.sltest_1_feature_sequences))
        
        seqIdNo1_exp = '<210>  1\r\n'
        self.assertEqual(seqIdNo1_exp, self.sequences5[0].seqIdNo_raw)
        self.assertEqual('1', self.sequences5[0].seqIdNo)
        
        length2_exp = '<211>  525\r\n'
        self.assertEqual(length2_exp, self.sequences5[1].length_raw)
        self.assertEqual('525', self.sequences5[1].length)
        
        molt3_exp = '<212>  PRT\r\n'
        self.assertEqual(molt3_exp, self.sequences5[2].molType_raw)
        self.assertEqual('PRT', self.sequences5[2].molType)
        
        organism1_exp = '<213>  Homo sapiens\r\n\r\n'
        self.assertEqual(organism1_exp, self.sequences5[0].organism_raw)
        self.assertEqual('Homo sapiens', self.sequences5[0].organism)
        
        organism40_exp = '<213>  Chloroflexus aurantiacus\r\n\r\n'
        self.assertEqual(organism40_exp, self.sequences5[39].organism_raw)
        self.assertEqual('Chloroflexus aurantiacus', self.sequences5[39].organism)
           
        self.assertFalse(self.sequences5[0].features)
           
        features4 = self.sequences5[3].features
        self.assertEqual(6, len(features4))
        
#         this test file was created on mac. features are not properly parsed, 
#         not clear why????????????
#         f_test = self.sltest_1_feature_sequences[0].features 
#         self.assertEqual(1, len(f_test))
        
           
        self.assertEqual('<220>\r\n', features4[0].featureHeader_raw)
        self.assertEqual('', features4[0].featureHeader)
        self.assertEqual(None, features4[0].key_raw)
        self.assertEqual(seqlutils.DEFAULT_STRING, features4[0].key)
        self.assertEqual(None, features4[0].location_raw)
        self.assertEqual(seqlutils.DEFAULT_STRING, features4[0].location)
        self.assertEqual('<223>  Sulfatase motif\r\n\r\n\r\n', features4[0].description_raw)
        self.assertEqual('Sulfatase motif', features4[0].description)
           
        self.assertEqual('<220>\r\n', features4[5].featureHeader_raw)
        self.assertEqual('', features4[5].featureHeader)
        self.assertEqual('<221>  MISC_FEATURE\r\n', features4[5].key_raw)
        self.assertEqual('MISC_FEATURE', features4[5].key)
        self.assertEqual('<222>  (5)..(5)\r\n', features4[5].location_raw)
        self.assertEqual('(5)..(5)', features4[5].location)
        self.assertEqual('<223>  Xaa = Any amino acid\r\n\r\n', features4[5].description_raw)
        self.assertEqual('Xaa = Any amino acid', features4[5].description)
           
            
        residues40_exp = '<400>  40\r\n\r\nMet Ser Gly Thr Gly Arg Leu Ala Gly Lys Ile Ala Leu Ile Thr Gly \r\n1               5                   10                  15      \r\n\r\n\r\nGly Ala Gly Asn Ile Gly Ser Glu Leu Thr Arg Arg Phe \r\n            20                  25         \r\n'
           
        self.assertEqual(residues40_exp, self.sequences5[39].residues_raw)

        seq1_2 = self.sequences1[1]
        seq5_5 = self.sequences5[4]
        sl6083_1_seq_1 = self.sequences6083_1[0]
        
        self.assertEqual('2', seq1_2.seqIdNo)
        self.assertEqual('5', seq5_5.seqIdNo)
        self.assertEqual('49', seq1_2.length)
        self.assertEqual('5', seq5_5.length)
        self.assertEqual(seq1_2.molType, "DNA")
        self.assertEqual(seq5_5.molType, "PRT")
        self.assertEqual(seq1_2.organism, "homo sapiens")
        self.assertEqual(seq5_5.organism, "Artificial Sequence")
        self.assertEqual(49, seq1_2.actualLength)
        self.assertEqual(5, seq5_5.actualLength)
#         # self.seq1_2.printSeq()
        self.assertEqual('DNA', seq1_2.actualMolType)
        self.assertEqual('RNA', sl6083_1_seq_1.actualMolType)
        self.assertEqual('PRT', seq5_5.actualMolType)
#         self.assertTrue(seq5_5.successfullyParsed)

    @withMethodName
    def test_seqNo400(self):
        exp_items400 = [str(a) for a in range(1,41)]
        act_items400 = [seq.seqNo400 for seq in self.sequences5]

        self.assertEqual(act_items400, exp_items400)
 
    @withMethodName
    def test_residues(self):
        
        exp1 = 'MetSerGlyThrGlyArgLeuAlaGlyLysIleAlaLeuIleThrGlyGlyAlaGlyAsnIleGlySerGluLeuThrArgArgPhe'
        self.assertEqual('', self.seq1_1.residues_nuc)
        self.assertEqual(exp1, self.seq1_1.residues_prt)
#  
        exp2 = 'atgatgatgatgatgatgtacctgcagaccccgtttccctggtgccagtggcagaggagtc'
        self.assertEqual(exp2, self.seq1_3.residues_nuc)
        self.assertEqual('', self.seq1_3.residues_prt)
  
        exp3 = 'augaugaugaugaugauguaccugcagaccccguuucccuggugccaguggcagaggaguc'
        self.assertEqual(exp3, self.seq2_3.residues_nuc)
        self.assertEqual('', self.seq2_3.residues_prt)
  
        exp4dna = 'atcgaccgtctccacaggtatgacacagagccagaccgtgacagtggaccagcaggagatcctgaaccgggccaatgaggtggaagctcccatggccgac'
        exp4prt = 'MetThrGlnSerGlnThrValThrValAspGlnGlnGluIleLeuAsnArgAlaAsnGluValGluAlaProMetAlaAsp'
        self.assertEqual(exp4dna, self.seq32_5.residues_nuc)
        self.assertEqual(exp4prt, self.seq32_5.residues_prt)
 
        self.assertEqual('XaaGlyXaaXaaXaa', self.seq5_5.residues_prt)
  
        exp40 = 'MetSerGlyThrGlyArgLeuAlaGlyLysIleAlaLeuIleThrGlyGlyAlaGlyAsnIleGlySerGluLeuThrArgArgPhe'
        self.assertEqual(exp40, self.seq5_40.residues_prt)

    @withMethodName
    def test_mixedmode(self):
        #test that False is returned for a PRT seq
        self.assertTrue(not self.seq1_1.mixedMode)
        self.assertEqual([], self.seq1_1.translations)
#         #test that False is returned for a DNA seq without mixed mode
        self.assertTrue(not self.seq1_2.mixedMode)
#         #test that False is returned for a RNA seq
        self.assertTrue(not self.seq2_3.mixedMode)
#         #test that True is returned for a DNA seq with mixed mode
        self.assertTrue(self.seq32_5.mixedMode)
    
    @withMethodName
    def test_featureTranslation(self):
#         test for translation attribute
        for f in self.seq1_1.features:
            self.assertEqual(seqlutils.DEFAULT_STRING, f.translation)
         
        features1004_1 = self.seq1004_1.features
 
        translation1__0_exp = 'MetLysArgValIleThrLeuPheAlaValLeuLeuMetGlyTrpSerValAsnAlaTrpSerPheAlaCysLysThrAlaAsnGlyThrAlaIleProIleGlyGlyGlySerAlaAsnValTyrValAsnLeuAlaProAlaValAsnValGlyGlnAsnLeuValValAspLeuSerThrGlnIlePheCysHisAsnAspTyrProGluThrIleThrAspTyrValThrLeuGlnArgGlyAlaAlaTyrGlyGlyValLeuSerSerPheSerGlyThrValLysTyrAsnGlySerSerTyrProPheProThrThrSerGluThrProArgValValTyrAsnSerArgThrAspLysProTrpProValAlaLeuTyrLeuThrProValSerSerAlaGlyGlyValAlaIleLysAlaGlySerLeuIleAlaValLeuIleLeuArgGlnThrAsnAsnTyrAsnSerAspAspPheGlnPheValTrpAsnIleTyrAlaAsnAsnAspValValValProThrGlyGlyCysAspValSerAlaArgAspValThrValThrLeuProAspTyrProGlySerValProIleProLeuThrValTyrCysAlaLysSerGlnAsnLeuGlyTyrTyrLeuSerGlyThrThrAlaAspAlaGlyAsnSerIlePheThrAsnThrAlaSerPheSerProAlaGlnGlyValGlyValGlnLeuThrArgAsnGlyThrIleIleProAlaAsnAsnThrValSerLeuGlyAlaValGlyThrSerAlaValSerLeuGlyLeuThrAlaAsnTyrAlaArgThrGlyGlyGlnValThrAlaGlyAsnValGlnSerIleIleGlyValThrPheValTyrGln'
        self.assertEqual(translation1__0_exp, features1004_1[0].translation)
         
        features1004_7 = self.seq1004_7.features
         
        translation7_0_exp = 'MetLysLysSerLeuValLeuLysAlaSerValAlaValAlaThrLeuValProMetLeuSerPheAlaAlaGluGlyGluPhe'
        translation7_1_exp = 'AspProAlaLysAlaAlaPheAspSerLeuGlnAlaSerAlaThrGluTyrIleGlyTyrAlaTrpAlaMetValValValIleValGlyAlaThrIleGlyIleLysLeuPheLysLysPheThrSerLysAlaSer'
 
        self.assertEqual(translation7_0_exp, features1004_7[1].translation)
        self.assertEqual(translation7_1_exp, features1004_7[2].translation)
         
    @withMethodName
    def test_translations(self):
        self.assertEqual([], self.seq1_1.translations)
        translation1__0_exp = 'MetLysArgValIleThrLeuPheAlaValLeuLeuMetGlyTrpSerValAsnAlaTrpSerPheAlaCysLysThrAlaAsnGlyThrAlaIleProIleGlyGlyGlySerAlaAsnValTyrValAsnLeuAlaProAlaValAsnValGlyGlnAsnLeuValValAspLeuSerThrGlnIlePheCysHisAsnAspTyrProGluThrIleThrAspTyrValThrLeuGlnArgGlyAlaAlaTyrGlyGlyValLeuSerSerPheSerGlyThrValLysTyrAsnGlySerSerTyrProPheProThrThrSerGluThrProArgValValTyrAsnSerArgThrAspLysProTrpProValAlaLeuTyrLeuThrProValSerSerAlaGlyGlyValAlaIleLysAlaGlySerLeuIleAlaValLeuIleLeuArgGlnThrAsnAsnTyrAsnSerAspAspPheGlnPheValTrpAsnIleTyrAlaAsnAsnAspValValValProThrGlyGlyCysAspValSerAlaArgAspValThrValThrLeuProAspTyrProGlySerValProIleProLeuThrValTyrCysAlaLysSerGlnAsnLeuGlyTyrTyrLeuSerGlyThrThrAlaAspAlaGlyAsnSerIlePheThrAsnThrAlaSerPheSerProAlaGlnGlyValGlyValGlnLeuThrArgAsnGlyThrIleIleProAlaAsnAsnThrValSerLeuGlyAlaValGlyThrSerAlaValSerLeuGlyLeuThrAlaAsnTyrAlaArgThrGlyGlyGlnValThrAlaGlyAsnValGlnSerIleIleGlyValThrPheValTyrGln'
        translation7__0_exp = 'MetLysLysSerLeuValLeuLysAlaSerValAlaValAlaThrLeuValProMetLeuSerPheAlaAlaGluGlyGluPhe'
        translation7__1_exp = 'AspProAlaLysAlaAlaPheAspSerLeuGlnAlaSerAlaThrGluTyrIleGlyTyrAlaTrpAlaMetValValValIleValGlyAlaThrIleGlyIleLysLeuPheLysLysPheThrSerLysAlaSer'
         
        translations1 = self.seq1004_1.translations 
        translations7 = self.seq1004_7.translations 
         
        self.assertEqual(translation1__0_exp, translations1[0])
        self.assertEqual(translation7__0_exp, translations7[0])
        self.assertEqual(translation7__1_exp, translations7[1])
        
    @withMethodName
    def test_actualMolType(self):
        '''
        Test that actualMolType is correctly set for 211 invalid, missing.
        '''
        self.assertEqual('RNA', self.sl6083_1_seq_2.actualMolType)
        self.assertEqual('RNA', self.sl6083_1_seq_3.actualMolType)
        self.assertEqual('RNA', self.sl6083_1_seq_4.actualMolType)

    @withMethodName
    def test_feature(self):
        self.assertEqual(len(self.seq5_5.features), 6)
 
        def checkFeature(featureId, fh, k, l, d):
            f = self.seq5_5.features[featureId]
            self.assertEqual(fh, f.featureHeader)
            self.assertEqual(k, f.key)
            self.assertEqual(l, f.location)
            self.assertEqual(d, f.description)
         
        checkFeature(0, '', seqlutils.DEFAULT_STRING, seqlutils.DEFAULT_STRING, 'Sulfatase motifs')
        checkFeature(1, '', 'MISC_FEATURE', '(1)..(1)', 'Xaa = Any amino acid or absent')
        checkFeature(2, '', 'MOD_RES', '(2)..(2)', 'Formylglycine')
        checkFeature(3, '', 'MISC_FEATURE', '(3)..(3)', 'Xaa = Any amino acid or absent')
        checkFeature(4, '', 'MISC_FEATURE', '(4)..(4)', 'Xaa = Pro or Ala second description line - test')
        checkFeature(5, '', 'MISC_FEATURE', '(5)..(5)', 'Xaa = Any amino acid')

        # #test for feature without key and location
        self.assertEqual('', self.seq32_5.features[0].featureHeader)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq32_5.features[0].key)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq32_5.features[0].location)
        self.assertEqual('Sequence from Mycobacterium tuberculosis artificially optimised for expression in human cells.',
                         self.seq32_5.features[0].description)

        # #test for feature without description
        self.assertEqual('', self.seq32_5.features[1].featureHeader)
        self.assertEqual('CDS', self.seq32_5.features[1].key)
        self.assertEqual('(20)..(1399)', self.seq32_5.features[1].location)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq32_5.features[1].description)
 
    @withMethodName
    def test_incompleteSequence(self):
        '''
        Test that an incomplete sequence (211 missing) is
        correctly parsed.
        '''
        
#         self.assertEqual(3, len(self.sl33_1.sequences))
        self.assertEqual(3, len(self.sequences33_1))

        self.assertEqual('2', self.seq33_1_2.seqIdNo)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq33_1_2.length)
        self.assertEqual('DNA', self.seq33_1_2.molType)
        self.assertEqual('Artificial Sequence', self.seq33_1_2.organism)
        self.assertEqual(447, self.seq33_1_2.actualLength)

    @withMethodName
    def test_skipCodeSequence1(self):
        '''Test skip code sequence when processResidues is False.
        '''
        self.assertTrue(not self.seq1_2.isSkipCode)
 
        self.assertEqual('4', self.seq6_4.seqIdNo)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq6_4.length)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq6_4.molType)
        self.assertEqual(seqlutils.DEFAULT_STRING, self.seq6_4.organism)
        self.assertEqual(0, self.seq6_4.actualLength)
        self.assertEqual(None, self.seq6_4.actualMolType)
        self.assertEqual([], self.seq6_4.features)
#         self.assertEqual([], self.seq6_4.publication)
        self.assertEqual('4', self.seq6_4.seqNo400)
        self.assertEqual('', self.seq6_4.residues_nuc)
        self.assertEqual('', self.seq6_4.residues_prt)
        self.assertTrue(self.seq6_4.isSkipCode)
# 
    @withMethodName
    def test_actualSeqIdNo(self):
        '''Test actualSeqId.
        '''
        # self.seq1_1.print_sequence()
        self.assertEqual(1, self.seq1_1.actualSeqIdNo)
        #not first not last seq
        self.assertEqual(5, self.seq5_5.actualSeqIdNo)
        #last seq
        self.assertEqual(40, self.seq5_40.actualSeqIdNo)
        #last seq is skip code
        self.assertEqual(4, self.seq6_4.actualSeqIdNo)

#         #seq 2 has actualSeqIdNo correct
        self.assertEqual(2, self.sequences32_8[1].actualSeqIdNo)
#         #seq 4 has seq_id_no correct
        self.assertEqual('4', self.sequences32_8[2].seqIdNo)
#         # but actualSeqIdNo is not equal to seq_id_no
        self.assertEqual(3, self.sequences32_8[2].actualSeqIdNo)

    @withMethodName
    def test_quantities(self):
        self.assertEqual(11, self.sl1004.quantity_nuc)
        self.assertEqual(6, self.sl1004.quantity_prt)
        self.assertEqual(4, self.sl1004.quantity_mix)
        self.assertEqual(18, self.sl1004.quantity_ftr)
        
        
#         sl with skip code
        self.assertEqual(1, self.sl6.quantity_nuc)
        self.assertEqual(2, self.sl6.quantity_prt)
        self.assertEqual(1, self.sl6.quantity_mix)
        self.assertEqual(2, self.sl6.quantity_ftr)
        

#     #test publication for sequence with no feature
#     def test_publication1(self):
#         #test for no publication
#         self.assertEqual(len(self.seq32_5.publication), 0)
#
#         self.assertEqual(len(self.seq1_1.publication), 1)
#         self.assertEqual(self.seq1_1.publication[0]['item300'], su.EMPTY)
#
#         self.assertEqual(self.seq1_1.publication[0]['item301'], "test 301 xxx line2")
#         self.assertEqual(self.seq1_1.publication[0]['item302'], "test 302")
#         self.assertEqual(self.seq1_1.publication[0]['item303'],  seqlutils.DEFAULT_STRING)
#         self.assertEqual(self.seq1_1.publication[0]['item305'], "test 305 line2 test 305")
#
#         exp_pub306_313 = [seqlutils.DEFAULT_STRING]*8
#         l = ['item' + str(i) for i in range(306, 314)]
#         act_pub306_313 = [self.seq1_1.publication[0][curritem] for curritem in l]
#         self.assertEqual(act_pub306_313, exp_pub306_313)
#
#     #test for sequence with incomplete feature (223 missing) and 2 publication blocks
#     def test_publication2(self):
#         self.assertEqual(self.seq1_2.seq_id_no, "2")#just to make sure that it works ...
#         self.assertEqual(len(self.seq1_2.publication), 2)
#         self.assertEqual(self.pub1_2_1['item300'], su.EMPTY)
#
#         self.assertEqual(self.pub1_2_1['item301'], "Doe, Richard")
#         self.assertEqual(self.pub1_2_1['item302'], "Isolation and Characterization of a Gene Encoding a Protease from Paramecium sp.")
#         self.assertEqual(self.pub1_2_1['item303'], 'Journal of Genes')
#         self.assertEqual(self.pub1_2_1['item304'], '1')
#         self.assertEqual(self.pub1_2_1['item305'], '4')
#         self.assertEqual(self.pub1_2_1['item306'], '1-7')
#         self.assertEqual(self.pub1_2_1['item307'], '1988-20-10')
#         self.assertEqual(self.pub1_2_1['item308'], seqlutils.DEFAULT_STRING)
#         self.assertEqual(self.pub1_2_1['item309'], seqlutils.DEFAULT_STRING)
#         self.assertEqual(self.pub1_2_1['item310'], seqlutils.DEFAULT_STRING)
#         self.assertEqual(self.pub1_2_1['item311'], su.EMPTY)
#         self.assertEqual(self.pub1_2_1['item312'], seqlutils.DEFAULT_STRING)
#         self.assertEqual(self.pub1_2_1['item313'], 'FROM 1 TO 30')

