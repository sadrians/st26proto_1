'''
Created on Apr 12, 2015

@author: ad
'''
from django.conf.urls import patterns, url

from sequencelistings import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_sequencelisting/$', views.add_sequencelisting, name='add_sequencelisting'),
    url(r'^about/$', views.about, name='about'),
    url(r'^download/(?P<fileName>.*)/$', views.download, name='download'),
    url(r'^sl(?P<pk>\d+)/$', views.detail, name='detail'),
    url(r'^sl(?P<pk>\d+)/edit_sequence_data/$', views.edit_sequence_data, name='edit_sequence_data'),
#     inconsistent names url vs function add_seq vs add_sequence!!!!
    url(r'^sl(?P<pk>\d+)/add_seq/$', views.add_sequence, name='add_seq'),
    url(r'^sl(?P<pk>\d+)/add_title/$', views.add_title, name='add_title'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/$', views.sequence, name='sequence'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/add_feature/$', views.add_feature, name='add_feature'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/add_multiple_feature/$', views.add_multiple_feature, name='add_multiple_feature'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/f(?P<fpk>\d+)/add_qualifier/$', 
        views.add_qualifier, 
        name='add_qualifier'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/f(?P<fpk>\d+)/edit_feature/$', views.edit_feature, name='edit_feature'),
    
    url(r'^sl(?P<pk>\d+)/xmloutput/$', views.generateXml, name='xmloutput'),
    
    url(r'^restricted/$', views.restricted, name='restricted'),
    
)
