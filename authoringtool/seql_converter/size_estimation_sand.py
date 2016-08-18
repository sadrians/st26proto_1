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
from size_estimation_new import FileSizeComparator, DirectEstimator
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

def listEstimatedAndActualSize(aListOfFilePaths, aReportFilePath):
    with open(aReportFilePath, 'w') as wr:
        wr.write('file,estimated_size,actual_size,estimated_vs_actual\n')
        for f in aListOfFilePaths:
            print f 
            de = DirectEstimator(f)
            wr.write('%s,%i,%i,%s\n' % (os.path.basename(f), de.estimatedSize,
                     de.foundSize, '%.1f' % (float(de.estimatedSize)/de.foundSize)))

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
    estimatedSizeFilePath = os.path.join(outDirPath, 'estimatedVsActualSize.csv')
    
#     code for the final report ===============================================
# ================ 1 general stats file ===============================================
    l = [os.path.join(inDirPath, a) for a in os.listdir(inDirPath) if '.DS' not in a]
#     largeFiles = ['WO2012-018754.txt', 'WO2012-028993.txt']
    largeFiles = ['WO2012-015765.txt', 'WO2012-018754.txt', 'WO2012-028993.txt'] 
    
    testList = [fp for fp in l if os.path.basename(fp) not in largeFiles]
    
#     extractTotals(testList, outDirPath, xmlOutDirPath, statsFilePath)
#     extractTotals(l, outDirPath, xmlOutDirPath, statsFilePath)
        
# ================ 2 general info size file ===============================================

#     cu.compareGeneralInformation(l, outDirPath, xmlOutDirPath)

# ================ 3 estimated and actual size file ===============================================
    
#     listEstimatedAndActualSize(l, estimatedSizeFilePath)

#     print 'GENERAL_INFORMATION_SIZE', cu.GENERAL_INFORMATION_SIZE
#     print 'SEQUENCE_SIZE', cu.SEQUENCE_SIZE
#     print 'FEATURE_SOURCE_SIZE', cu.FEATURE_SOURCE_SIZE
#     print 'FEATURE_SIZE', cu.FEATURE_SIZE





















# ================ extra process 4 more files with large size ===============================================
    
#     inDirPath_extra = r'/Users/ad/pyton/test/st26fileSize/in_ST25_old'
#     extra_list = [os.path.join(inDirPath_extra, a) for a in os.listdir(inDirPath_extra) if '.DS' not in a]
    
    
    
#     end code for the final report===============================================    
    
#     l = [os.path.join(inDirPath, a) for a in os.listdir(inDirPath) if '.DS' not in a]
# #     largeFiles = ['WO2012-018754.txt', 'WO2012-028993.txt']
#     largeFiles = ['WO2012-015765.txt', 'WO2012-018754.txt', 'WO2012-028993.txt'] 
#     
#     testList = [fp for fp in l if os.path.basename(fp) not in largeFiles]
# #     pprint.pprint(testList)
#     
# #     extractTotals(l[:5], outDirPath, xmlOutDirPath, statsFilePath)  
#     extractTotals(testList, outDirPath, xmlOutDirPath, statsFilePath)
























#     for f in testList:
#         de = DirectEstimator(f)
#         print f 
#         print de.estimatedSize
#         print de.foundSize
#     



#     f6_1 = os.path.join(settings.BASE_DIR, 'seql_converter', 
#                         'st25parser', 'testdata', 'file6_1.txt') # seq 1 cds not div by 3
#     f6503 = os.path.join(inDirPath, 'WO2012-006503.txt')# 170 missing

#     cu.compareGeneralInformation(testList, outDirPath, xmlOutDirPath)
#     compareElementsInCsvAndXmlFiles(l, outDirPath, xmlOutDirPath)
    
#     ex = r'/Users/ad/pyton/projects/ftp/wipo/extracted'
#     exl = [os.path.join(ex, a) for a in os.listdir(ex) if '.DS' not in a]
    
    
#     code for the final report ===============================================
# ================ 1 general stats file ===============================================
    
# #     clean file names
#     for fp in extra_list:
#         print fp 
#         os.rename(fp, fp.replace('-001.zip', ''))

#     inDir = r'/Users/ad/pyton/test/st26fileSize/test/in_ST25'
#     statsDir = r'/Users/ad/pyton/test/st26fileSize/test/stats'
#     outDir = r'/Users/ad/pyton/test/st26fileSize/test/out_ST26'
#         
#     test_dependency_on_feature(inDir, outDir, statsDir)
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

# def compareGeneralInformation(aList, outDirPath, xmlOutDirPath):
#     outf = os.path.join(outDirPath, 'genInfo_comparison.csv')
#     with open(outf, 'wb') as csvfile:
#         wr = csv.writer(csvfile, delimiter=',')
#         wr.writerow(['file', 'genInfo_chars_st25', 'genInfo_chars_st25_clean', 'genInfo_chars_st26'])
#         for fp in aList:
#             bn = os.path.basename(fp)
#             fileName = bn[:-4]
#             print fileName
#             xmlFileName = '%s_ST26_clean.xml' % fileName 
#             print xmlFileName
#             xmlFileNamePath = os.path.join(xmlOutDirPath, xmlFileName)
#             with open(fp, 'r') as f25, open(xmlFileNamePath, 'r') as f26:
#                 genInfo25 = f25.read().split('<210>')[0]
# #                 print genInfo25
# #                 genInfo25_clean = genInfo25.replace(re.compile(r'\s'), '')
#                 genInfo25_clean = re.sub(r'\s', '', genInfo25)
#                 genInfo26 = f26.read().split('<SequenceData sequenceIDNumber="1">')[0]
# #                 print genInfo26
#                 wr.writerow([bn, len(genInfo25), len(genInfo25_clean), len(genInfo26)])