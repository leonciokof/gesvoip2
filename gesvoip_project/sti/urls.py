from django.conf.urls import patterns, url

urlpatterns = patterns(
    'sti.views',
    url(r'^cpanel_sti/$', 'cpanel_sti', name='cpanel_sti'),
    url(r'^sti_locales/$', 'sti_locales', name='sti_locales'),
    url(r'^sti_locales2/$', 'sti_locales2', name='sti_locales2'),
    url(r'^sti_locales3/(?P<pk>\d+)/$', 'sti_locales3', name='sti_locales3'),
    url(r'^sti_informe_locales/$',
        'sti_informe_locales', name='sti_informe_locales'),
    url(r'^sti_informe_locales2/(?P<year>\d+)/(?P<month>\d+)/$',
        'sti_informe_locales2', name='sti_informe_locales2'),
    url(r'^sti_lineas/$', 'sti_lineas', name='sti_lineas'),
    url(r'^sti_lineas2/$', 'sti_lineas2', name='sti_lineas2'),
    url(r'^sti_lineas3/(?P<pk>\d+)/$', 'sti_lineas3', name='sti_lineas3'),
    url(r'^sti_lineas4/(?P<pk>\d+)/$', 'sti_lineas4', name='sti_lineas4'),
    url(r'^sti_informe_lineas/$',
        'sti_informe_lineas', name='sti_informe_lineas'),
    url(r'^sti_informe_lineas2/(?P<year>\d+)/(?P<month>\d+)/$',
        'sti_informe_lineas2', name='sti_informe_lineas2'),
)
