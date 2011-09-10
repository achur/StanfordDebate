from django.conf.urls.defaults import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'pages.views.mainpage'),
    url(r'^results/$', 'pages.views.results'),
    url(r'^join/$', 'pages.views.join'),
    url(r'^join/create/$', 'pages.views.joincreate'),
    url(r'^schedule/$', 'pages.views.schedule'),
    url(r'^roster/$', 'pages.views.roster'),
    url(r'^faq/$', 'pages.views.faq'),
    url(r'^links/$', 'pages.views.links'),
    url(r'^resources/$', 'pages.views.resources'),
    url(r'^pages/(?P<slug_name>\S+)/$', 'pages.views.pages')
)

urlpatterns += staticfiles_urlpatterns()