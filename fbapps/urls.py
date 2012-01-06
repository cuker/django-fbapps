from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('fbapps.views',
    url(r'^flat-tab/(?P<slug>[\w\d\-]+)/$', 'flat_tab_view', name='flat-tab'),
    url(r'^generic-tab/(?P<pk>\d+)/$', 'generic_tab_view', name='generic-tab'),
)

