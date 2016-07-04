# -*- coding: utf-8 -*-
'''
Created on 3 Sep 2015
Updated on 2 Jul 2016
@author: ad
'''
import django
django.setup()

from django.conf import settings
import unittest
import os

from seqlparser import SequenceListing, GeneralInformation
import seqlutils

def withMethodName(func):
    def inner(*args, **kwargs):
        print 'Running %s ...' % func.__name__
        func(*args, **kwargs)
    return inner

class TestSequenceListing(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        def getAbsPath(aFileName):
            return os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 'testData', aFileName)
        def getSeql(aFileName):
            return SequenceListing(getAbsPath(aFileName))
        
#         infilename1 = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 'testData', 'file1.txt')
#         cls.sl1 = SequenceListing(infilename1)
        
        cls.sl1 = getSeql('file1.txt')
        cls.sl2 = getSeql('file2.txt')
        cls.sl5 = getSeql('file5.txt')
        cls.sl6 = getSeql('file6.txt')
        cls.sl32 = getSeql('file32.txt')
        cls.sl32_2 = getSeql('file32_2.txt') # 120 is missing
        cls.sl32_3 = getSeql('file32_3.txt') # 120 is empty
        cls.sl32_4 = getSeql('file32_4.txt')
        cls.sl32_5 = getSeql('file32_5.txt') # closing bracket missing from 120
        cls.sl32_8 = getSeql('file32_8.txt') # seq 3 is missing
        cls.sl32_9 = getSeql('file32_9.txt') # 110 is empty
        cls.sl33_1 = getSeql('file33_1.txt')
        cls.sl6083_1 = getSeql('WO2012-006083_1.txt')
        cls.sl058291 = getSeql('WO2012-058291-001.zip.txt') # what's special with this sl?
        cls.sl_input_no_seql = getSeql('no_st25_example.txt') # not sequence listing file
                
        infilename1 = getAbsPath('file1.txt')
        infilename2 = getAbsPath('file2.txt')
        infilename5 = getAbsPath('file5.txt')
        infilename6 = getAbsPath('file6.txt')
        infilename32 = getAbsPath('file32.txt')
        infilename33_1 = getAbsPath('file33_1.txt')
        f6083_1 = getAbsPath('WO2012-006083_1.txt')

        cls.seq1_1 = SequenceListing.getSequenceFromFile(infilename1, 1)
        cls.seq1_2 = SequenceListing.getSequenceFromFile(infilename1, 2)
        cls.seq1_3 = SequenceListing.getSequenceFromFile(infilename1, 3)
        #
        # # cls.pub1_2_1 = cls.seq1_2.publication[1]
        #
        cls.seq2_3 = SequenceListing.getSequenceFromFile(infilename2, 3)

        cls.seq5_5 = SequenceListing.getSequenceFromFile(infilename5, 5)
        cls.seq5_37 = SequenceListing.getSequenceFromFile(infilename5, 37)
        cls.seq5_40 = SequenceListing.getSequenceFromFile(infilename5, 40)

        cls.seq6_1 = SequenceListing.getSequenceFromFile(infilename6, 1)
        cls.seq6_4 = SequenceListing.getSequenceFromFile(infilename6, 4) # skip code
        cls.seq32_5 = SequenceListing.getSequenceFromFile(infilename32, 5)

        cls.seq33_1_2 = SequenceListing.getSequenceFromFile(infilename33_1, 2)

        cls.sl6083_1_seq_1 = SequenceListing.getSequenceFromFile(f6083_1, 1) # 212 is RNA
        cls.sl6083_1_seq_2 = SequenceListing.getSequenceFromFile(f6083_1, 2) # 212 is DNA instead of RNA
        cls.sl6083_1_seq_3 = SequenceListing.getSequenceFromFile(f6083_1, 3) # 212 is abc instead of RNA
        cls.sl6083_1_seq_4 = SequenceListing.getSequenceFromFile(f6083_1, 4) # 212 is missing

        # cls.seq016177_3 = cls.sl016177.sequences[2]

    @withMethodName
    def test_isSeql(self):
        self.assertTrue(self.sl1.isSeql)
        self.assertTrue(not self.sl_input_no_seql.isSeql)
        self.assertTrue(not SequenceListing('abc').isSeql)
        print 'xxx'
        # test if closing bracket missing from 120
        self.assertTrue(self.sl32_5.isSeql)
        # what's special with this sl? why do we need this test?
        self.assertTrue(self.sl058291.isSeql)

# ==========Tests for GeneralInformation===========================
    @withMethodName
    def test_applicant(self):
        
        self.assertEqual(['OPX Biotechnologies, Inc.'], self.sl1.generalInformation.applicant)
        self.assertEqual(['OPX Biotechnologies, Inc.', 'Universite Paris II'], self.sl2.generalInformation.applicant)
        self.assertEqual(['Merck Sharp & Dohme Corp.',
                          'Chen, Zhiyu',
                          'Lancaster, Thomas M.',
                          'Zion, Todd C.'], self.sl33_1.generalInformation.applicant)
#         # item110 empty
        self.assertEqual([], self.sl32_9.generalInformation.applicant)

    @withMethodName
    def test_title(self):
        self.assertEqual(self.sl32.generalInformation.title, "COMPOSITIONS AND METHODS REGARDING DIRECT NADH UTILIZATION TO PRODUCE 3-HYDROXYPROPIONIC ACID AND RELATED CHEMICALS AND PRODUCTS")
        # item120 missing
        self.assertEqual(None, self.sl32_2.generalInformation.title)
        # item120 empty
        self.assertEqual('', self.sl32_3.generalInformation.title)

    @withMethodName
    def test_reference(self):
        self.assertEqual(self.sl32.generalInformation.reference, "34246761601")
        #reference element is missing
        self.assertEqual(self.sl2.generalInformation.reference, None)

    @withMethodName
    def test_applicationNumber(self):
        self.assertEqual(self.sl32.generalInformation.applicationNumber, "61536464")

    @withMethodName
    def test_filingDate(self):
        self.assertEqual(self.sl32.generalInformation.filingDate, "2012-09-19")
        
    @withMethodName
    def test_priority(self):
        pr32 = self.sl32.generalInformation.priority
        self.assertEqual(3, len(pr32))
        
        self.assertListEqual([('61536558 - prio1', '2001-01-01'), 
                              ('61536539 - prio2', '2002-02-02 - pd'),
                              ('61536539 - prio3', '2003-03-03')], 
                             self.sl1.generalInformation.priority)
        
        self.assertListEqual([], self.sl2.generalInformation.priority)
        
    @withMethodName
    def test_quantity(self):
        self.assertEqual('5', self.sl32.generalInformation.quantity)

    @withMethodName
    def test_software(self):
        self.assertEqual(self.sl32.generalInformation.software, "PatentIn version 3.5")

# ==========Tests for Sequence===========================

    @withMethodName
    def test_sequence(self):
        self.assertEqual(self.seq1_2.seqIdNo, "2")
        self.assertEqual(self.seq5_5.seqIdNo, "5")
        self.assertEqual(self.seq1_2.length, "49")
        self.assertEqual(self.seq5_5.length, "5")
        self.assertEqual(self.seq1_2.molType, "DNA")
        self.assertEqual(self.seq5_5.molType, "PRT")
        self.assertEqual(self.seq1_2.organism, "homo sapiens")
        self.assertEqual(self.seq5_5.organism, "Artificial Sequence")
        self.assertEqual(self.seq1_2.actualLength, 49)
        self.assertEqual(self.seq5_5.actualLength, 5)
        # self.seq1_2.printSeq()
        self.assertEqual('DNA', self.seq1_2.actualMolType)
        self.assertEqual('RNA', self.sl6083_1_seq_1.actualMolType)
        self.assertEqual('PRT', self.seq5_5.actualMolType)
        self.assertTrue(self.seq5_5.successfullyParsed)

    @withMethodName
    def test_feature(self):
        self.assertEqual(len(self.seq5_5.features), 6)

        def checkFeature(featureId, fh, k, l, d):
            f = self.seq5_5.features[featureId]
            self.assertEqual(fh, f.featureHeader)
            self.assertEqual(k, f.key)
            self.assertEqual(l, f.location)
            self.assertEqual(d, f.description)

        checkFeature(0, '', '-', '-', 'Sulfatase motifs')
        checkFeature(1, '', 'MISC_FEATURE', '(1)..(1)', 'Xaa = Any amino acid or absent')
        checkFeature(2, '', 'MOD_RES', '(2)..(2)', 'Formylglycine')
        checkFeature(3, '', 'MISC_FEATURE', '(3)..(3)', 'Xaa = Any amino acid or absent')
        checkFeature(4, '', 'MISC_FEATURE', '(4)..(4)', 'Xaa = Pro or Ala second description line - test')
        checkFeature(5, '', 'MISC_FEATURE', '(5)..(5)', 'Xaa = Any amino acid')


        # #test for feature without key and location
        self.assertEqual('', self.seq32_5.features[0].featureHeader)
        self.assertEqual('-', self.seq32_5.features[0].key)
        self.assertEqual('-', self.seq32_5.features[0].location)
        self.assertEqual('Sequence from Mycobacterium tuberculosis artificially optimised for expression in human cells.',
                         self.seq32_5.features[0].description)

        # #test for feature without description
        self.assertEqual('', self.seq32_5.features[1].featureHeader)
        self.assertEqual('CDS', self.seq32_5.features[1].key)
        self.assertEqual('(20)..(1399)', self.seq32_5.features[1].location)
        self.assertEqual('-', self.seq32_5.features[1].description)

    @withMethodName
    def test_mixedmode(self):
        #test that False is returned for a PRT seq
        self.assertTrue(not self.seq1_1.mixedMode)
#         #test that False is returned for a DNA seq without mixed mode
        self.assertTrue(not self.seq1_2.mixedMode)
#         #test that False is returned for a RNA seq
        self.assertTrue(not self.seq2_3.mixedMode)
#         #test that True is returned for a DNA seq with mixed mode
        self.assertTrue(self.seq32_5.mixedMode)

    @withMethodName
    def test_seqNo400(self):
        exp_items400 = [str(a) for a in range(1,41)]
        seq = []
        for s in self.sl5.generateSequence():
            seq.append(s)
        act_items400 = [seq.seqNo400 for seq in seq]
        self.assertEqual(act_items400, exp_items400)

    @withMethodName
    def test_residues(self):
        exp1 = 'MetSerGlyThrGlyArgLeuAlaGlyLysIleAlaLeuIleThrGlyGlyAlaGlyAsnIleGlySerGluLeuThrArgArgPhe'
        self.assertEqual('', self.seq1_1.residues_nuc)
        self.assertEqual(exp1, self.seq1_1.residues_prt)

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
    def test_incompleteSequence(self):
        '''
        Test that an incomplete sequence (211 missing) is
        correctly parsed.
        '''
        seq = []
        for s in self.sl33_1.generateSequence():
            seq.append(s)
        self.assertEqual(3, len(seq))
        self.assertEqual('2', self.seq33_1_2.seqIdNo)
        self.assertEqual(None, self.seq33_1_2.length)
        self.assertEqual('DNA', self.seq33_1_2.molType)
        self.assertEqual('Artificial Sequence', self.seq33_1_2.organism)
        self.assertEqual(447, self.seq33_1_2.actualLength)

    @withMethodName
    def test_actualMolType(self):
        '''
        Test that actualMolType is correctly set for 211 invalid, missing.
        '''
        self.assertEqual('RNA', self.sl6083_1_seq_2.actualMolType)
        self.assertEqual('RNA', self.sl6083_1_seq_3.actualMolType)
        self.assertEqual('RNA', self.sl6083_1_seq_4.actualMolType)

    @withMethodName
    def test_skipCodeSequence1(self):
        '''Test skip code sequence when processResidues is False.
        '''
        self.assertTrue(not self.seq1_2.isSkipCode)

        self.assertEqual(self.seq6_4.seqIdNo, "4")
        self.assertEqual(self.seq6_4.length, None)
        self.assertEqual(self.seq6_4.molType, None)
        self.assertEqual(self.seq6_4.organism, None)
        self.assertEqual(0, self.seq6_4.actualLength)
        self.assertEqual(None, self.seq6_4.actualMolType)
        self.assertEqual([], self.seq6_4.features)
#         self.assertEqual([], self.seq6_4.publication)
        self.assertEqual(self.seq6_4.seqNo400, '4')
        self.assertEqual('', self.seq6_4.residues_nuc)
        self.assertEqual('', self.seq6_4.residues_prt)
        self.assertTrue(self.seq6_4.isSkipCode)

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

        sl32_8_sequences = []

        for s in self.sl32_8.generateSequence():
            sl32_8_sequences.append(s)

        #seq 2 has actualSeqIdNo correct
        self.assertEqual(2, sl32_8_sequences[1].actualSeqIdNo)
        #seq 4 has seq_id_no correct
        self.assertEqual('4', sl32_8_sequences[2].seqIdNo)
        # but actualSeqIdNo is not equal to seq_id_no
        self.assertEqual(3, sl32_8_sequences[2].actualSeqIdNo)

class Test_GeneralInformation(unittest.TestCase):
    
    @withMethodName
    def test_parsePriority(self):
        p = """
  61536558

<151>  2011-09-19

<150>  61536539

<151>  2012-09-19



<150>  61536580

<151>  2013-09-19
        """
        res = GeneralInformation.parsePriority(p)
        self.assertListEqual([('61536558', '2011-09-19'), 
                              ('61536539', '2012-09-19'), 
                              ('61536580', '2013-09-19')], res)
        

# ==========Tests for Feature===========================

    # def test_feature1(self):
    #     chunks = []
    #     gen = su.generateChunks(self.infilename5, '<210>')
    #     for c in gen:
    #         chunks.append(c)
    #     c5 = chunks[5]['chunk']
    #     print c5
    #     fiter = re.finditer(sp.featurePattern, c5)
    #
    #     for m in fiter:
    #         # print 'key', m.group('key')
    #         f = sp.Feature1(m)
    #         f.printFeat()

#     def test_priority(self):
#         self.assertEqual(len(self.sl32_4.generalInformation.priority), 3)
#
#         actual_pn = [self.sl32_4.generalInformation.priority[i]['priority_number'] for i in range(3)]
#         expected_pn = ['61536558', '61536539', '61536540']
#         self.assertEqual(actual_pn, expected_pn)
#
#         actual_pd = [self.sl32_4.generalInformation.priority[i]['priority_date'] for i in range(3)]
#         expected_pd = ['2011-09-19x1', '2011-09-19x2', '2011-09-19x3']
#         self.assertEqual(actual_pd, expected_pd)
#
#         #no priority
#         self.assertEqual(len(self.sl2.generalInformation.priority), 0)
#

#     def test_header(self):
#         self.assertEqual(self.sl1.generalInformation.header, 'SEQUENCE LISTING')
#         self.assertEqual(self.sl5.generalInformation.header, 'SEQUENCE LISTING')
#
#     def test_applicant(self):
#         #applicant with one line
#         self.assertEqual(self.sl32.generalInformation.applicant, ["OPX Biotechnologies, Inc."])
#         #applicant with 2 lines
#         self.assertEqual(self.sl32_1.generalInformation.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
#         #applicant with 2 lines, item120 missing
#         self.assertEqual(self.sl32_2.generalInformation.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
# #         applicant with non ASCII chars
# #         a = self.sl41670.generalInformation.applicant
# #         self.assertEqual('Technische Universität Dortmund and Heinrich-Heine', a[0])
# #         self.assertEqual('Universität Düsseldorf', a[1])

#     def test_skipCodeSequence2(self):
#         '''Test skip code sequence when processResidues is True.
#         '''
#         self.assertEqual(self.seq016177_3.seq_id_no, "3")
#         self.assertEqual(self.seq016177_3.length, None)
#         self.assertEqual(self.seq016177_3.molType, None)
#         self.assertEqual(self.seq016177_3.organism, None)
#         self.assertEqual(0, self.seq016177_3.actualLength)
#         # self.assertEqual(su.VALUE_NOT_SET, self.seq016177_3.actualMolType)
#         self.assertEqual(None, self.seq016177_3.actualMolType)
#         self.assertEqual([], self.seq016177_3.features)
#         self.assertEqual([], self.seq016177_3.publication)
#         self.assertEqual(self.seq016177_3.item400, '3')
#         self.assertEqual('', self.seq016177_3.nucstring)
#         self.assertEqual('', self.seq016177_3.prtstring)
#         self.assertTrue(self.seq016177_3.skipCode)

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
#         self.assertEqual(self.seq1_1.publication[0]['item303'],  None)
#         self.assertEqual(self.seq1_1.publication[0]['item305'], "test 305 line2 test 305")
#
#         exp_pub306_313 = [None]*8
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
#         self.assertEqual(self.pub1_2_1['item308'], None)
#         self.assertEqual(self.pub1_2_1['item309'], None)
#         self.assertEqual(self.pub1_2_1['item310'], None)
#         self.assertEqual(self.pub1_2_1['item311'], su.EMPTY)
#         self.assertEqual(self.pub1_2_1['item312'], None)
#         self.assertEqual(self.pub1_2_1['item313'], 'FROM 1 TO 30')


#
#     def test_sequencegrammar(self):
#         '''
#         Test that the sequence grammar from slparser module raises ParseException.
#         '''
#         f = '/Users/ad/pyton/projects/ftp/wipo/extracted/WO2012-058291-001.zip.txt'
#         l = su.getListOfChunks(f, '<210>')
#         def funct():
#             return sequence.parseString(l[1]['chunk'], l[1]['lineNumber'])
#
#         with self.assertRaises(pyparsing.ParseException) as c:
#             funct()
# #         test the the line number is correctly derived
#         self.assertEqual(24, c.exception.__getattr__('lineno')+ l[1]['lineNumber']-1)

#     def test_emptySequence(self):
#         '''
#         Test that an empty sequence is returned when Sequence class raises ParseException.
#         '''
#         self.assertEqual(3, len(self.sequences_sl33_1))
#         self.assertEqual(None, self.seq33_1_2.seq_id_no)
#         self.assertEqual(None, self.seq33_1_2.length)
#         self.assertEqual(None, self.seq33_1_2.mol_type)
#         self.assertEqual(None, self.seq33_1_2.organism)
#         self.assertEqual([], self.seq33_1_2.feature)


# #     @unittest.skip('test_fileEncoding skipped temporarily ...')
# #     def test_fileEncoding(self):
# #         self.assertEqual('windows-1252', self.sl41670.fileEncoding)
# #



# ==========================================
# # -*- coding: utf-8 -*-
# '''
# Created on Feb 16, 2014
# Updated on Dec 29, 2014
# Updated on Feb 2, 2015 to use generator functionality of SequenceListing class
# Updated on Feb 17, 2015 to use test data from testdata directory
#
# @author: ad
# '''
# import unittest, os
# from tools.seqlparser import SequenceListing
#
# class Test(unittest.TestCase):
#
#     @classmethod
#     def setUpClass(cls):
#
#         infilename1 = os.path.join('testdata', 'file1.txt')
#         cls.sl1 = SequenceListing(infilename1)
#
#         infilename2 = os.path.join('testdata', 'file2.txt')
#         cls.sl2 = SequenceListing(infilename2)
#
#         infilename5 = os.path.join('testdata', 'file5.txt')
#         cls.sl5 = SequenceListing(infilename5)
#
#         # infilename6 = os.path.join('testdata', 'file6.txt')
#         # cls.sl6 = SequenceListing(infilename6)
#
#         infilename32 = os.path.join('testdata', 'file32.txt')
#         cls.sl32 = SequenceListing(infilename32)
#         #
#         # infilename32_1 = os.path.join('testdata', 'file32_1.txt')
#         # cls.sl32_1 = SequenceListing(infilename32_1)
#         #
#         # infilename32_2 = os.path.join('testdata', 'file32_2.txt')
#         # cls.sl32_2 = SequenceListing(infilename32_2)
#         #
#         # infilename32_3 = os.path.join('testdata', 'file32_3.txt')
#         # cls.sl32_3 = SequenceListing(infilename32_3)
#         #
#         # infilename32_4 = os.path.join('testdata', 'file32_4.txt')
#         # cls.sl32_4 = SequenceListing(infilename32_4)
#         #
#         # infilename32_5 = os.path.join('testdata', 'file32_5.txt')
#         # cls.sl32_5 = SequenceListing(infilename32_5)
#
#         # seq 3 is missing
#         # infilename32_6 = os.path.join('testdata', 'file32_6.txt')
#         # cls.sl32_6 = SequenceListing(infilename32_6)
#
#         infilename33_1 = os.path.join('testdata', 'file33_1.txt')
#         cls.sl33_1 = SequenceListing(infilename33_1)
#
#         f6083_1 = os.path.join('testdata', 'WO2012-006083_1.txt')
#         cls.sl6083_1 = SequenceListing(f6083_1)
#         #
#         # infilename016177 = os.path.join('testdata', 'WO2012-016177-001.zip.txt')
#         #
#         # infilename058291 = os.path.join('testdata', 'WO2012-058291-001.zip.txt')
#         # cls.sl058291 = SequenceListing(infilename058291)
#
#         cls.seq1_1 = cls.sl1.sequences[0]
#         cls.seq1_2 = cls.sl1.sequences[1]
#         cls.seq1_3 = cls.sl1.sequences[2]
#
#         # cls.pub1_2_1 = cls.seq1_2.publication[1]
#
#         cls.seq2_3 = cls.sl2.sequences[2]
#
#         cls.seq5_5 = cls.sl5.sequences[4]
#         cls.seq5_40 = cls.sl5.sequences[39]
#
#         # cls.seq6_1 = cls.sl6.sequences[0]
#         # cls.seq6_4 = cls.sl6.sequences[3] # skip code
#         #
#         # # cls.seq6_1.print_sequence()
#         #
#         cls.seq32_5 = cls.sl32.sequences[4]
#
#         # cls.seq33_1_2 = cls.sl33_1.sequences[1]
#
#         cls.sl6083_1_seq_1 = cls.sl6083_1.sequences[0] # 212 is RNA
#         cls.sl6083_1_seq_2 = cls.sl6083_1.sequences[1] # 212 is DNA instead of RNA
#         cls.sl6083_1_seq_3 = cls.sl6083_1.sequences[2] # 212 is abc instead of RNA
#         cls.sl6083_1_seq_4 = cls.sl6083_1.sequences[3] # 212 is missing
#
#         # cls.seq016177_3 = cls.sl016177.sequences[2]
#
#     def test_sequence(self):
#         self.assertEqual(self.seq1_2.seqIdNo, "2")
#         self.assertEqual(self.seq5_5.seqIdNo, "5")
#         self.assertEqual(self.seq1_2.length, "49")
#         self.assertEqual(self.seq5_5.length, "5")
#         self.assertEqual(self.seq1_2.molType, "DNA")
#         self.assertEqual(self.seq5_5.molType, "PRT")
#         self.assertEqual(self.seq1_2.organism, "homo sapiens")
#         self.assertEqual(self.seq5_5.organism, "Artificial Sequence")
#         self.assertEqual(self.seq1_2.actualLength, 49)
#         self.assertEqual(self.seq5_5.actualLength, 5)
#         # self.seq1_2.printSeq()
#         self.assertEqual('DNA', self.seq1_2.actualMolType)
#         self.assertEqual('RNA', self.sl6083_1_seq_1.actualMolType)
#         self.assertEqual('PRT', self.seq5_5.actualMolType)
#
#     def test_feature(self):
#         self.assertEqual(len(self.seq5_5.features), 6)
#
#         def checkFeature(featureId, fh, k, l, d):
#             f = self.seq5_5.features[featureId]
#             self.assertEqual(fh, f.featureHeader)
#             self.assertEqual(k, f.key)
#             self.assertEqual(l, f.location)
#             self.assertEqual(d, f.description)
#
#         checkFeature(0, '', None, None, 'Sulfatase motifs')
#         checkFeature(1, '', 'MISC_FEATURE', '(1)..(1)', 'Xaa = Any amino acid or absent')
#         checkFeature(2, '', 'MOD_RES', '(2)..(2)', 'Formylglycine')
#         checkFeature(3, '', 'MISC_FEATURE', '(3)..(3)', 'Xaa = Any amino acid or absent')
#         checkFeature(4, '', 'MISC_FEATURE', '(4)..(4)', 'Xaa = Pro or Ala second description line - test')
#         checkFeature(5, '', 'MISC_FEATURE', '(5)..(5)', 'Xaa = Any amino acid')
#
#
#         # #test for feature without key and location
#         self.assertEqual('', self.seq32_5.features[0].featureHeader)
#         self.assertEqual(None, self.seq32_5.features[0].key)
#         self.assertEqual(None, self.seq32_5.features[0].location)
#         self.assertEqual('Sequence from Mycobacterium tuberculosis artificially optimised for expression in human cells.',
#                          self.seq32_5.features[0].description)
#
#         # #test for feature without description
#         self.assertEqual('', self.seq32_5.features[1].featureHeader)
#         self.assertEqual('CDS', self.seq32_5.features[1].key)
#         self.assertEqual('(20)..(1399)', self.seq32_5.features[1].location)
#         self.assertEqual(None, self.seq32_5.features[1].description)
#
#
#
#     def test_mixedmode(self):
#         #test that False is returned for a PRT seq
#         self.assertTrue(not self.seq1_1.mixedMode)
# #         #test that False is returned for a DNA seq without mixed mode
#         self.assertTrue(not self.seq1_2.mixedMode)
# #         #test that False is returned for a RNA seq
#         self.assertTrue(not self.seq2_3.mixedMode)
# #         #test that True is returned for a DNA seq with mixed mode
#         self.assertTrue(self.seq32_5.mixedMode)
#
#     def test_seqNo400(self):
#         exp_items400 = [str(a) for a in range(1,41)]
#         act_items400 = [seq.seqNo400 for seq in self.sl5.sequences]
#         self.assertEqual(act_items400, exp_items400)
#
#
#     def test_residues(self):
#         exp1 = 'MetSerGlyThrGlyArgLeuAlaGlyLysIleAlaLeuIleThrGlyGlyAlaGlyAsnIleGlySerGluLeuThrArgArgPhe'
#         self.assertEqual('', self.seq1_1.residues_nuc)
#         self.assertEqual(exp1, self.seq1_1.residues_prt)
#
#         exp2 = 'atgatgatgatgatgatgtacctgcagaccccgtttccctggtgccagtggcagaggagtc'
#         self.assertEqual(exp2, self.seq1_3.residues_nuc)
#         self.assertEqual('', self.seq1_3.residues_prt)
#
#         exp3 = 'augaugaugaugaugauguaccugcagaccccguuucccuggugccaguggcagaggaguc'
#         self.assertEqual(exp3, self.seq2_3.residues_nuc)
#         self.assertEqual('', self.seq2_3.residues_prt)
#
#
#         exp4dna = 'atcgaccgtctccacaggtatgacacagagccagaccgtgacagtggaccagcaggagatcctgaaccgggccaatgaggtggaagctcccatggccgac'
#         exp4prt = 'MetThrGlnSerGlnThrValThrValAspGlnGlnGluIleLeuAsnArgAlaAsnGluValGluAlaProMetAlaAsp'
#         self.assertEqual(exp4dna, self.seq32_5.residues_nuc)
#         self.assertEqual(exp4prt, self.seq32_5.residues_prt)
#
#         self.assertEqual('XaaGlyXaaXaaXaa', self.seq5_5.residues_prt)
#
#         exp40 = 'MetSerGlyThrGlyArgLeuAlaGlyLysIleAlaLeuIleThrGlyGlyAlaGlyAsnIleGlySerGluLeuThrArgArgPhe'
#         self.assertEqual(exp40, self.seq5_40.residues_prt)
#
#     def test_incompleteSequence(self):
#         '''
#         Test that an incomplete sequence (211 missing) is
#         correctly parsed.
#         '''
#
#         self.assertEqual(3, len(self.sl33_1.sequences))
#         seq2 = self.sl33_1.sequences[1]
#         self.assertEqual('2', seq2.seqIdNo)
#         self.assertEqual(None, seq2.length)
#         self.assertEqual('DNA', seq2.molType)
#         self.assertEqual('Artificial Sequence', seq2.organism)
#         self.assertEqual(447, seq2.actualLength)
#
#     def test_molTypeIssues(self):
#         '''
#         Test that actualMolType is correctly set for 211 invalid, missing.
#         '''
#
#         self.assertEqual('RNA', self.sl6083_1_seq_2.actualMolType)
#         self.assertEqual('RNA', self.sl6083_1_seq_3.actualMolType)
#         self.assertEqual('RNA', self.sl6083_1_seq_4.actualMolType)
#
# #     def test_skipCodeSequence1(self):
# #         '''Test skip code sequence when processResidues is False.
# #         '''
# #         self.assertEqual(self.seq6_4.seq_id_no, "4")
# #         self.assertEqual(self.seq6_4.length, su.MISSING)
# #         self.assertEqual(self.seq6_4.molType, su.MISSING)
# #         self.assertEqual(self.seq6_4.organism, su.MISSING)
# #         self.assertEqual(0, self.seq6_4.actualLength)
# #         # self.assertEqual(su.VALUE_NOT_SET, self.seq6_4.actualMolType)
# #         self.assertEqual(su.MISSING, self.seq6_4.actualMolType)
# #         self.assertEqual([], self.seq6_4.features)
# #         self.assertEqual([], self.seq6_4.publication)
# #         self.assertEqual(self.seq6_4.item400, '4')
# #         self.assertEqual(su.MISSING, self.seq6_4.nucstring)
# #         self.assertEqual(su.MISSING, self.seq6_4.prtstring)
# #         self.assertTrue(not self.seq6_4.skipCode)
# #
# #     def test_skipCodeSequence2(self):
# #         '''Test skip code sequence when processResidues is True.
# #         '''
# #         self.assertEqual(self.seq016177_3.seq_id_no, "3")
# #         self.assertEqual(self.seq016177_3.length, su.MISSING)
# #         self.assertEqual(self.seq016177_3.molType, su.MISSING)
# #         self.assertEqual(self.seq016177_3.organism, su.MISSING)
# #         self.assertEqual(0, self.seq016177_3.actualLength)
# #         # self.assertEqual(su.VALUE_NOT_SET, self.seq016177_3.actualMolType)
# #         self.assertEqual(su.MISSING, self.seq016177_3.actualMolType)
# #         self.assertEqual([], self.seq016177_3.features)
# #         self.assertEqual([], self.seq016177_3.publication)
# #         self.assertEqual(self.seq016177_3.item400, '3')
# #         self.assertEqual('', self.seq016177_3.nucstring)
# #         self.assertEqual('', self.seq016177_3.prtstring)
# #         self.assertTrue(self.seq016177_3.skipCode)
# #
#     def test_actualSeqIdNo(self):
#         '''Test actualSeqId.
#         '''
#         # self.seq1_1.print_sequence()
#         self.assertEqual(1, self.seq1_1.actualSeqIdNo)
#         #not first not last seq
#         self.assertEqual(5, self.seq5_5.actualSeqIdNo)
#         #last seq
#         self.assertEqual(40, self.seq5_40.actualSeqIdNo)
#         #last seq is skip code
#         # self.assertEqual(4, self.seq6_4.actualSeqIdNo)
# #
# #         sl32_6_sequences = []
# #
# #         for s in self.sl32_6.generateSequence():
# #             sl32_6_sequences.append(s)
# #
# #         #seq 2 has actualSeqIdNo correct
# #         self.assertEqual(2, sl32_6_sequences[1].actualSeqIdNo)
# #         #seq 4 has seq_id_no correct
# #         self.assertEqual('4', sl32_6_sequences[2].seq_id_no)
# #         # but actualSeqIdNo is not equal to seq_id_no
# #         self.assertEqual(3, sl32_6_sequences[2].actualSeqIdNo)
# #
# #
# #         # seq5_37 = SequenceListing.getSequenceFromFile(self.infilename5,37)
# #         # self.assertEqual(37, seq5_37.actualSeqIdNo)
# #         # seq5_37.seq_id_no = 100
# #         # self.assertTrue(not seq5_37.actualSeqIdNo == 37)
#
# #     def test_emptySequence(self):
# #         '''
# #         Test that an empty sequence is returned when Sequence class raises ParseException.
# #         '''
# #         self.assertEqual(3, len(self.sequences_sl33_1))
# #         self.assertEqual(su.MISSING, self.seq33_1_2.seq_id_no)
# #         self.assertEqual(su.MISSING, self.seq33_1_2.length)
# #         self.assertEqual(su.MISSING, self.seq33_1_2.mol_type)
# #         self.assertEqual(su.MISSING, self.seq33_1_2.organism)
# #         self.assertEqual([], self.seq33_1_2.feature)
#
#
# # #     @unittest.skip('test_fileEncoding skipped temporarily ...')
# # #     def test_fileEncoding(self):
# # #         self.assertEqual('windows-1252', self.sl41670.fileEncoding)
# # #
# # #     @unittest.skip('skipped bc successfullyParsed still not implemented...')
# #     def test_successfullyParsed(self):
# #         self.assertTrue(self.sl1.successfullyParsed)
# #         self.assertTrue(not SequenceListing('abc').successfullyParsed)
# #         self.assertTrue(not SequenceListing('testdata' + '/no_st25_example.txt').successfullyParsed)
# #         # test if closing bracket missing from 120
# #         self.assertTrue(self.sl32_5.successfullyParsed)
# #         self.assertTrue(self.sl058291.successfullyParsed)
# #
# #     def test_header(self):
# #         self.assertEqual(self.sl1.generalInformation.header, 'SEQUENCE LISTING')
# #         self.assertEqual(self.sl5.generalInformation.header, 'SEQUENCE LISTING')
# #
# #     def test_applicant(self):
# #         #applicant with one line
# #         self.assertEqual(self.sl32.generalInformation.applicant, ["OPX Biotechnologies, Inc."])
# #         #applicant with 2 lines
# #         self.assertEqual(self.sl32_1.generalInformation.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
# #         #applicant with 2 lines, item120 missing
# #         self.assertEqual(self.sl32_2.generalInformation.applicant, ["OPX Biotechnologies, Inc.", "biOasis Technologies, Inc."])
# # #         applicant with non ASCII chars
# # #         a = self.sl41670.generalInformation.applicant
# # #         self.assertEqual('Technische Universität Dortmund and Heinrich-Heine', a[0])
# # #         self.assertEqual('Universität Düsseldorf', a[1])
# #
# #     def test_title(self):
# #         self.assertEqual(self.sl32.generalInformation.title, "COMPOSITIONS AND METHODS REGARDING DIRECT NADH UTILIZATION TO PRODUCE 3-HYDROXYPROPIONIC ACID AND RELATED CHEMICALS AND PRODUCTS")
# #         # item120 missing
# #         self.assertEqual(self.sl32_2.generalInformation.title, su.MISSING)
# #         # item120 empty
# #         self.assertEqual(self.sl32_3.generalInformation.title, su.EMPTY)
# #
# #     def test_reference(self):
# #         self.assertEqual(self.sl32.generalInformation.reference, "34246761601")
# #         #reference element is missing
# #         self.assertEqual(self.sl2.generalInformation.reference, su.MISSING)
# #
# #     def test_applicationNumber(self):
# #         self.assertEqual(self.sl32.generalInformation.application_number, "61536464")
# #
# #     def test_filingDate(self):
# #         self.assertEqual(self.sl32.generalInformation.filing_date, "2012-09-19")
# #
# #     def test_priority(self):
# #         self.assertEqual(len(self.sl32_4.generalInformation.priority), 3)
# #
# #         actual_pn = [self.sl32_4.generalInformation.priority[i]['priority_number'] for i in range(3)]
# #         expected_pn = ['61536558', '61536539', '61536540']
# #         self.assertEqual(actual_pn, expected_pn)
# #
# #         actual_pd = [self.sl32_4.generalInformation.priority[i]['priority_date'] for i in range(3)]
# #         expected_pd = ['2011-09-19x1', '2011-09-19x2', '2011-09-19x3']
# #         self.assertEqual(actual_pd, expected_pd)
# #
# #         #no priority
# #         self.assertEqual(len(self.sl2.generalInformation.priority), 0)
# #
# #     def test_numberOfSequences(self):
# #         self.assertEqual(self.sl32.generalInformation.number_of_sequences, "5")
# #
# #     def test_software(self):
# #         self.assertEqual(self.sl32.generalInformation.software, "PatentIn version 3.5")
#
#
# #
# #     #test for sequence with no feature
# #     def test_publication1(self):
# #         #test for no publication
# #         self.assertEqual(len(self.seq32_5.publication), 0)
# #
# #         self.assertEqual(len(self.seq1_1.publication), 1)
# #         self.assertEqual(self.seq1_1.publication[0]['item300'], su.EMPTY)
# #
# #         self.assertEqual(self.seq1_1.publication[0]['item301'], "test 301 xxx line2")
# #         self.assertEqual(self.seq1_1.publication[0]['item302'], "test 302")
# #         self.assertEqual(self.seq1_1.publication[0]['item303'],  su.MISSING)
# #         self.assertEqual(self.seq1_1.publication[0]['item305'], "test 305 line2 test 305")
# #
# #         exp_pub306_313 = [su.MISSING]*8
# #         l = ['item' + str(i) for i in range(306, 314)]
# #         act_pub306_313 = [self.seq1_1.publication[0][curritem] for curritem in l]
# #         self.assertEqual(act_pub306_313, exp_pub306_313)
# #
# #     #test for sequence with incomplete feature (223 missing) and 2 publication blocks
# #     def test_publication2(self):
# #         self.assertEqual(self.seq1_2.seq_id_no, "2")#just to make sure that it works ...
# #         self.assertEqual(len(self.seq1_2.publication), 2)
# #         self.assertEqual(self.pub1_2_1['item300'], su.EMPTY)
# #
# #         self.assertEqual(self.pub1_2_1['item301'], "Doe, Richard")
# #         self.assertEqual(self.pub1_2_1['item302'], "Isolation and Characterization of a Gene Encoding a Protease from Paramecium sp.")
# #         self.assertEqual(self.pub1_2_1['item303'], 'Journal of Genes')
# #         self.assertEqual(self.pub1_2_1['item304'], '1')
# #         self.assertEqual(self.pub1_2_1['item305'], '4')
# #         self.assertEqual(self.pub1_2_1['item306'], '1-7')
# #         self.assertEqual(self.pub1_2_1['item307'], '1988-20-10')
# #         self.assertEqual(self.pub1_2_1['item308'], su.MISSING)
# #         self.assertEqual(self.pub1_2_1['item309'], su.MISSING)
# #         self.assertEqual(self.pub1_2_1['item310'], su.MISSING)
# #         self.assertEqual(self.pub1_2_1['item311'], su.EMPTY)
# #         self.assertEqual(self.pub1_2_1['item312'], su.MISSING)
# #         self.assertEqual(self.pub1_2_1['item313'], 'FROM 1 TO 30')
#
#
# #
# #     def test_sequencegrammar(self):
# #         '''
# #         Test that the sequence grammar from slparser module raises ParseException.
# #         '''
# #         f = '/Users/ad/pyton/projects/ftp/wipo/extracted/WO2012-058291-001.zip.txt'
# #         l = su.getListOfChunks(f, '<210>')
# #         def funct():
# #             return sequence.parseString(l[1]['chunk'], l[1]['lineNumber'])
# #
# #         with self.assertRaises(pyparsing.ParseException) as c:
# #             funct()
# # #         test the the line number is correctly derived
# #         self.assertEqual(24, c.exception.__getattr__('lineno')+ l[1]['lineNumber']-1)
# #