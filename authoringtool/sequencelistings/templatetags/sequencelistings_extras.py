'''
Created on Feb 2, 2016

@author: ad
'''

from django import template
from sequencelistings.models import SequenceListing 

register = template.Library()

@register.inclusion_tag('sequencelistings/seqls.html')
def get_sequenceListing_list(sequenceListing=None):
    """used for populating the sidebar with links to sequence listings"""
    return {'seqls': SequenceListing.objects.all(), 'act_seql': sequenceListing}