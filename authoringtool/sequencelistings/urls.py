'''
Created on Apr 12, 2015

@author: ad
'''
from django.conf.urls import patterns, url

from sequencelistings import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^add_sequencelisting/$', views.add_sequencelisting, name='add_sequencelisting'),
#     ex: /sequencelistings/5/
    url(r'^sl(?P<pk>\d+)/$', views.detail, name='detail'),
#     url(r'^(?P<pk>\d+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^sl(?P<pk>\d+)/add_title/$', views.add_title, name='add_title'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/$', views.sequence, name='sequence'),
#     url(r'^sl(?P<pk>\d+)/advanced/$', views.advanced, name='advanced'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/add_multiple_feature/$', views.add_multiple_feature, name='add_multiple_feature'),
    url(r'^sl(?P<pk>\d+)/add_seq/$', views.add_sequence, name='add_seq'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/add_feature/$', views.add_feature, name='add_feature'),
#     url(r'^sl\d+/seq\d+/f(?P<fpk>\d+)/edit_feature/$', views.edit_feature, name='edit_feature'),
#     url(r'^(?P<pk>\d+)/add_feature/$', views.add_feature, name='add_feature'),
    url(r'^sl(?P<pk>\d+)/seq(?P<spk>\d+)/f(?P<fpk>\d+)/add_qualifier/$', 
        views.add_qualifier, 
        name='add_qualifier'),
    url(r'^sl(?P<pk>\d+)/xmloutput/$', views.generateXml, name='xmloutput'),
#     url(r'^register/$', views.register, name='register'),
#     url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/$', views.restricted, name='restricted'),
    url(r'^about/$', views.about, name='about'),
#       url(r'^logout/$', views.user_logout, name='logout'),
    
)
