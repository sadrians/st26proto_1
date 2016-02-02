'''
Created on Feb 2, 2016

@author: ad
'''

from django import template
from sequencelistings.models import SequenceListing 

register = template.Library()

@register.inclusion_tag('sequencelistings/seqls.html')
def get_seqls_list():
    return {'seqls': SequenceListing.objects.all()}