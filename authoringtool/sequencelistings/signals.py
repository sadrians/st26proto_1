# '''
# Created on Feb 6, 2016
# 
# @author: ad
# '''
# from django.db.models.signals import post_init
# from django.dispatch import receiver 
# from django.conf import settings
# from sequencelistings.models import Feature
# import os.path  
# 
# @receiver(post_init, sender=Feature)
# def model_post_init(sender, **kwargs):
#     print 'invoked'
#     print 'moltype is:', kwargs['instance'].sequence.moltype 
# #     if os.path.isfile(settings.READ_ONLY_FILE):
# #         raise ReadOnlyException('Model in read only mode, cannot save')
#     
# 
# class ReadOnlyException(Exception):
#     pass 