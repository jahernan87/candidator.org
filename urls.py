from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from elections.views import add_category

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'candidator.views.home', name='home'),
    # url(r'^candidator/', include('candidator.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', include(admin.site.urls)),

    (r'^profiles/', include('profiles.urls')),

    url(r'^elections/', include('elections.urls')),
    url(r'^(?P<my_user>[a-zA-Z0-9-]+)/(?P<election_slug>[a-zA-Z0-9-]+)/medianaranja/$', 'candidator.elections.views.medianaranja1',name='medianaranja1'),
    url(r'^(?P<user>[a-zA-Z0-9-]+)/(?P<election_slug>[-\w]+)/add_category/$',
            add_category,
            name='add_category' ),

    # django-registration urls, maps common registration urls to the ones in django.contrib.auth
    (r'^accounts/', include('registration.urls')),

    (r'^$', direct_to_template, {'template': 'index.html'}),


)
