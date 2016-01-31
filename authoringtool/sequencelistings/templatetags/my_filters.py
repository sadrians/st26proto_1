'''
Created on May 5, 2015

@author: ad
'''
from django import template

register = template.Library()

@register.filter(name='access')
def access(di, k):
    return di[k]