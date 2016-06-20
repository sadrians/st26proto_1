'''
Created on Jun 18, 2016

@author: ad
'''
import os
# from fileinput import filename
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authoringtool.settings')
 
import django
django.setup()
 
from sequencelistings.models import SequenceListing, Title, Sequence, Feature, Qualifier
from populate_db import add_title, copySequenceListing

from sequencelistings.util import expandFormula 

def myCopyScript(aFileName):
    sl = SequenceListing.objects.filter(fileName=aFileName)[0] 
    copySequenceListing(sl)
    print 'Done with copying', aFileName

# myCopyScript('Invention_SEQL')

# print 'GGGX'*100
# print expandFormula('cg(agg)4..7')