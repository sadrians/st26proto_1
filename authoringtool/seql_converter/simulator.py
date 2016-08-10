'''
Created on Aug 7, 2016

@author: ad
'''
import os 
import pprint
import csv 
from django.conf import settings
import re 
from converter import St25To26Converter
from st25parser.seqlparser_new import SequenceListing
from st25parser import seqlutils as su 
from size_estimation_new import FileSizeComparator
import converter_util as cu 

class Simulator(object):
    def __init__(self, inDir, outDir, statDir):
        self.inDir = inDir 
        self.outDir = outDir
        self.statDir = statDir
        
        self.seedFilePath = os.path.join(inDir, 'seed_test.txt') 
        with open(self.seedFilePath, 'r') as f:
            self.seedString = f.read()
            
        self.featureTestFiles = []
        self.sequenceTestFiles = []
    
    def createFeatureTestData(self, howManyFiles):
        featureString = """<220>\n\r
<221> dummy_key\n\r
<222> 1..20\n\r
<223>  dummy maximum possible description according to ST.25 max \n\r
        260 chars on max 4 lines dummy filling text to reach 260 chars \n\r
        260 chars on max 4 lines dummy filling text to reach 260 chars \n\r
        260 chars on max 4 lines dummy filling text to rea \n\r\n\r"""
        with open(self.seedFilePath, 'r') as seedF:
            s = seedF.read()
            for i in range(1, howManyFiles+1):
                newFilePath = self.seedFilePath.replace('.txt', '%i.txt' % i)
                newFilePath = newFilePath.replace('seed', 'f')
                with open(newFilePath, 'w') as wr:
                    newString = s.replace('<400>  1', '%s<400>  1' % ((i-1)* featureString))
                    wr.write(newString)
                self.featureTestFiles.append(newFilePath)
                    
    def createSequenceTestData(self, howManyFiles):
        sequenceString = """<210>  %i\n\r
<211>  10\n\r
<212>  DNA\n\r
<213>  Artificial Sequence\n\r
\n\r
<220>\n\r
<223>  Forward primer for YFP gene\n\r
\n\r
<400>  %i\n\r
tgttccacgg                                               10\n\r\n\r"""
        toBeAdded = []
        for i in range(1, howManyFiles+1):
            
            newBaseName = 's_test%i.txt' % i 
            newfp = os.path.join(self.inDir, newBaseName)
            with open(newfp, 'w') as swr:
                swr.write(self.seedString.replace('<160>  1', '<160>  %i' % i))
                swr.write(''.join(toBeAdded))
            toBeAdded.append(sequenceString %(i+1,i+1))
            
            self.sequenceTestFiles.append(newfp)
    
    
    def test_dependency(self, aToken, aTag):
        with open(os.path.join(self.statDir, '%sstat.csv' % aToken), 'w') as wr:
            wr.write('%s\n' %('file,%scount,size_st25,size_st26,r26vs25,incr_st25,incr_st26' % aToken))
            
            files = [f for f in os.listdir(self.inDir) if '.DS' not in f and f.startswith(aToken)]
            di = {}
            for f in files:
                c = St25To26Converter(os.path.join(self.inDir, f))
                xmlPath_large = c.generateXmlFile(self.outDir)
                xmlPath = cu.cleanAndWriteXmlFile(xmlPath_large)
                di[f] = xmlPath
            
            initialFile = files[0]
            
            prev_size_st25 = os.path.getsize(os.path.join(self.inDir, initialFile))
            prev_size_st26 = os.path.getsize(di[initialFile])
            
#             for f in sorted(di.keys(), key=lambda x: os.path.getsize(os.path.join(self.inDir, f))):
            if aToken == 'f_':
                currentList = self.featureTestFiles 
            elif aToken == 's_':
                currentList = self.sequenceTestFiles
            for fp in currentList:
#                 fp = os.path.join(self.inDir, f)
                with open(fp, 'r') as fr:
                    s = fr.read()
                    feature_count = s.count(aTag)
                
                currentSize_st25 = os.path.getsize(fp)
                bn = os.path.basename(fp)
                currentSize_st26 = os.path.getsize(di[bn])
                 
                wr.write('%s,%i,%i,%i,%s,%i,%i\n' %(bn, 
                                            feature_count, 
                                           currentSize_st25,
                                           currentSize_st26, 
                                           '%0.1f' % (float(currentSize_st26)/currentSize_st25),
                                           currentSize_st25 - prev_size_st25, 
                                           currentSize_st26 - prev_size_st26))
                 
                prev_size_st25 = currentSize_st25
                prev_size_st26 = currentSize_st26 
                
    def test_residues_dependency(self, aToken):
        with open(os.path.join(self.statDir, '%sstat.csv' % aToken), 'w') as wr:
            wr.write('%s\n' %('file,%scount,%schars,size_st25,size_st26,r26vs25' %(aToken, aToken)))
            
            files = [f for f in os.listdir(self.inDir) if '.DS' not in f and f.startswith(aToken)]
            di = {}
            for f in files:
                c = St25To26Converter(os.path.join(self.inDir, f))
                xmlPath_large = c.generateXmlFile(self.outDir)
                xmlPath = cu.cleanAndWriteXmlFile(xmlPath_large)
                di[f] = xmlPath
            
            for f in sorted(di.keys()):
                fp = os.path.join(self.inDir, f)
                    
                currentSize_st25 = os.path.getsize(fp)
                currentSize_st26 = os.path.getsize(di[f])
                
                with open(fp, 'r') as f:
                    s = f.read()
                    l = s.split('<400>  1')
                    
                    item211 = re.search('<211>\s+(\d+)', s)
                    s1Length = int(item211.group(1))
                    
#                     print l[1]
                 
                wr.write('%s,%i,%i,%i,%i,%s\n' %(os.path.basename(fp), 
                                           s1Length,
                                        len(l[1]),
                                           currentSize_st25,
                                           currentSize_st26,
                                           '%0.1f' % (float(currentSize_st26)/currentSize_st25), 
                                           ))
                       
# ==================== main =========================
if __name__ == "__main__":
        
    inDir = r'/Users/ad/pyton/test/st26fileSize/test/in_ST25'
    statsDir = r'/Users/ad/pyton/test/st26fileSize/test/stats'
    outDir = r'/Users/ad/pyton/test/st26fileSize/test/out_ST26'
    
    inDirFixture = r'/Users/ad/pyton/test/st26fileSize/test/fixtureTest'
    
    sim = Simulator(inDir, outDir, statsDir)
    sim.createFeatureTestData(20)
    sim.createSequenceTestData(20)
    sim.test_dependency('f_', '<220>')
#     sim.test_dependency('s_', '<210>')
#     sim.test_residues_dependency('r_')
#     sim.test_residues_dependency('p_')
#     sim.test_residues_dependency('m_')

























#     inDirPath = r'/Users/ad/pyton/test/st26fileSize/in_ST25'
#     outDirPath = r'/Users/ad/pyton/test/st26fileSize/stats'
#     xmlOutDirPath = r'/Users/ad/pyton/test/st26fileSize/out_ST26'
#     statsFilePath = os.path.join(outDirPath, 'stats.csv')
#     
#     f6_1 = os.path.join(settings.BASE_DIR, 'seql_converter', 
#                         'st25parser', 'testdata', 'file6_1.txt') # seq 1 cds not div by 3
#     f6503 = os.path.join(inDirPath, 'WO2012-006503.txt')# 170 missing
#     
#     l = [os.path.join(inDirPath, a) for a in os.listdir(inDirPath) if '.DS' not in a]
#     largeFiles = ['WO2012-018754.txt', 'WO2012-028993.txt']
#     
#     testList = [fp for fp in l if os.path.basename(fp) not in largeFiles]
# #     pprint.pprint(testList)
#     
#     f18754 = os.path.join(inDirPath, 'WO2012-018754.txt')
    
#     extractTotals([f18754], outDirPath, xmlOutDirPath, statsFilePath)

#     extractTotals(l[:5], outDirPath, xmlOutDirPath, statsFilePath)
#     extractTotals(testList, outDirPath, xmlOutDirPath, statsFilePath)

#     cu.compareGeneralInformation(testList, outDirPath, xmlOutDirPath)
#     compareElementsInCsvAndXmlFiles(l, outDirPath, xmlOutDirPath)
    
#     ex = r'/Users/ad/pyton/projects/ftp/wipo/extracted'
#     exl = [os.path.join(ex, a) for a in os.listdir(ex) if '.DS' not in a]

#     clean file names
#     for fp in l:
#         os.rename(fp, fp.replace('-001.zip', ''))        
#     fp = os.path.join(inDirPath, 'WO2012-006443.txt')
#     
#     with open(fp, 'r') as f:
#         s = f.read()
#         l = s.split('<210>  2')
# #         print l[0] 
#         
#         with open(os.path.join(inDir, 'test.txt'), 'w') as wr:
#             wr.write(l[0])
# =====================================================

