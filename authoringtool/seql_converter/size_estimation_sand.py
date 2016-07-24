'''
Created on Jul 15, 2016

@author: ad
'''
import os 
import pprint
import csv 
from django.conf import settings

from size_estimation import FileSizeComparator
import converter_util as cu 


# ==================== main =========================
if __name__ == "__main__":
    inputDir = os.path.join(settings.BASE_DIR, 'seql_converter', 'st25parser', 
                  'testData')
    f5 = os.path.join(inputDir, 'file5.txt')
    f1004 = os.path.join(inputDir, 'WO2012-001004-001.zip.txt')
        
    inDirPath = r'/Users/ad/pyton/test/st26fileSize/in_ST25'
    outDirPath = r'/Users/ad/pyton/test/st26fileSize/stats'
    xmlOutDirPath = r'/Users/ad/pyton/test/st26fileSize/out_ST26'
    statsFilePath = os.path.join(outDirPath, 'stats.csv')
        
#     l = [f5, f1004]
    l = [os.path.join(inDirPath, a) for a in os.listdir(inDirPath) if '.DS' not in a]
 
    totalsList = []
    for f in l[1:2]:
        fsc = FileSizeComparator(f, outDirPath, xmlOutDirPath)
        totalsList.append(fsc.totals) 
        fsc.compareElementsInCsvAndXmlFiles()
#         pprint.pprint(fsc.totals)
    with open(statsFilePath, 'wb') as csvfile:
        wr = csv.writer(csvfile, delimiter=',')
        wr.writerow(cu.STATS_HEADER)
        for t in totalsList:
            currentRow = [t[col] for col in cu.STATS_HEADER]
            wr.writerow(currentRow)
            
        
        
        
        
# =====================================================



# # pprint.pprint(l)
# 
# 
# for fp in l:
#     print fp
#     outf = fp.replace('.txt', '_lengths.txt')
#     outf = outf.replace('converter_in', 'converter_out')
#     writeSizes(fp, outf)
