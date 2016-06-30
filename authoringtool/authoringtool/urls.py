from django.conf.urls import patterns, include, url
from registration.backends.simple.views import RegistrationView 
from django.contrib import admin
admin.autodiscover()

# Create a new class that redirects the user to the index page, if successful at logging
class MyRegistrationView(RegistrationView):
    def get_success_url(self,request, user):
        return '/sequencelistings/'


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^sequencelistings/', include('sequencelistings.urls', namespace='sequencelistings')),
    url(r'^accounts/register/', MyRegistrationView.as_view(), name='registration_register'),
#     url(r'^accounts/password/change', MyRegistrationView.as_view(), name='auth_password_change'),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    
)
