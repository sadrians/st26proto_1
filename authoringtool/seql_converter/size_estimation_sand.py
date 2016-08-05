'''
Created on Jul 15, 2016

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

def extractTotals(aList, outDirPath, xmlOutDirPath, statsFilePath):
    totalsList = []
    for f in aList:
        fsc = FileSizeComparator(f, outDirPath, xmlOutDirPath)
        totalsList.append(fsc.totals) 
#         pprint.pprint(fsc.totals)
    
    with open(statsFilePath, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(cu.STATS_HEADER)
        for t in totalsList:
            currentRow = [t[col] for col in cu.STATS_HEADER]
            wr.writerow(currentRow)
            
def compareGeneralInformation(aList, outDirPath, xmlOutDirPath):
    outf = os.path.join(outDirPath, 'genInfo_comparison.csv')
    with open(outf, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(['file', 'genInfo_chars_st25', 'genInfo_chars_st25_clean', 'genInfo_chars_st26'])
        for fp in aList:
            bn = os.path.basename(fp)
            fileName = bn[:-4]
            print fileName
            xmlFileName = '%s_ST26_clean.xml' % fileName 
            print xmlFileName
            xmlFileNamePath = os.path.join(xmlOutDirPath, xmlFileName)
            with open(fp, 'r') as f25, open(xmlFileNamePath, 'r') as f26:
                genInfo25 = f25.read().split('<210>')[0]
#                 print genInfo25
#                 genInfo25_clean = genInfo25.replace(re.compile(r'\s'), '')
                genInfo25_clean = re.sub(r'\s', '', genInfo25)
                genInfo26 = f26.read().split('<SequenceData sequenceIDNumber="1">')[0]
#                 print genInfo26
                wr.writerow([bn, len(genInfo25), len(genInfo25_clean), len(genInfo26)])

def compareElementsInCsvAndXmlFiles(aList, outDirPath, xmlOutDirPath):
    for fp in aList:
        fsc = FileSizeComparator(fp, outDirPath, xmlOutDirPath)
        fsc.compareElementsInCsvAndXmlFiles()

        
# ==================== main =========================
if __name__ == "__main__":
        
    inDirPath = r'/Users/ad/pyton/test/st26fileSize/in_ST25'
    outDirPath = r'/Users/ad/pyton/test/st26fileSize/stats'
    xmlOutDirPath = r'/Users/ad/pyton/test/st26fileSize/out_ST26'
    statsFilePath = os.path.join(outDirPath, 'stats.csv')
    
    f6_1 = os.path.join(settings.BASE_DIR, 'seql_converter', 
                        'st25parser', 'testdata', 'file6_1.txt') # seq 1 cds not div by 3
    f6503 = os.path.join(inDirPath, 'WO2012-006503.txt')# 170 missing
    
    l = [os.path.join(inDirPath, a) for a in os.listdir(inDirPath) if '.DS' not in a]
    
    f18754 = os.path.join(inDirPath, 'WO2012-018754.txt')
    
#     extractTotals([f18754], outDirPath, xmlOutDirPath, statsFilePath)

    extractTotals(l[:5], outDirPath, xmlOutDirPath, statsFilePath)
#     compareGeneralInformation(l, outDirPath, xmlOutDirPath)
#     compareElementsInCsvAndXmlFiles(l, outDirPath, xmlOutDirPath)
    
#     ex = r'/Users/ad/pyton/projects/ftp/wipo/extracted'
#     exl = [os.path.join(ex, a) for a in os.listdir(ex) if '.DS' not in a]

#     clean file names
#     for fp in l:
#         os.rename(fp, fp.replace('-001.zip', ''))
        
        
        
        
# =====================================================

