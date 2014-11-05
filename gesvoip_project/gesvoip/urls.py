from django.conf.urls import patterns, url

urlpatterns = patterns(
    'gesvoip.views',
    url(r'^$', 'index', name='index'),
    url(r'^new_cdr/$', 'new_cdr', name='new_cdr'),
    url(r'^new_rate/$', 'new_rate', name='new_rate'),
    url(r'^incoming_list/$', 'incoming_list', name='incoming_list'),
    url(r'^invoice_list/$', 'invoice_list', name='invoice_list'),
    url(r'^company_list/$', 'company_list', name='company_list'),
    url(r'^company_create/$', 'company_create', name='company_create'),
    url(r'^company_update/(?P<pk>\w+)/$',
        'company_update', name='company_update'),
    url(r'^invoice_datail/(?P<pk>\w+)/$',
        'invoice_datail', name='invoice_datail'),
    url(r'^holiday_list/$', 'holiday_list', name='holiday_list'),
    url(r'^holiday_create/$', 'holiday_create', name='holiday_create'),
    url(r'^holiday_update/(?P<pk>\w+)/$',
        'holiday_update', name='holiday_update'),
    url(r'^numeration_list/(?P<pk>\w+)/$',
        'numeration_list', name='numeration_list'),
    url(r'^incoming_valid_list/(?P<pk>\w+)/$',
        'incoming_valid_list', name='incoming_valid_list'),
    url(r'^line_list/$', 'line_list', name='line_list'),
    url(r'^line_create/$', 'line_create', name='line_create'),
    url(r'^line_update/(?P<pk>\w+)/$', 'line_update', name='line_update'),
    url(r'^line_range/$', 'line_range', name='line_range'),
    url(r'^localcenter_list/$',
        'localcenter_list', name='localcenter_list'),
    url(r'^localcenter_create/$',
        'localcenter_create', name='localcenter_create'),
    url(r'^localcenter_update/(?P<pk>\w+)/$',
        'localcenter_update', name='localcenter_update'),
    url(r'^localcenter_report/$',
        'localcenter_report', name='localcenter_report'),
    url(r'^line_service_report/$',
        'line_service_report', name='line_service_report'),
    url(r'^line_subscriber_report/$',
        'line_subscriber_report', name='line_subscriber_report'),
    url(r'^ccaa_list/$', 'ccaa_list', name='ccaa_list'),
    url(r'^ccaa_create/$', 'ccaa_create', name='ccaa_create'),
    url(r'^ccaa_update/(?P<pk>\w+)/$', 'ccaa_update', name='ccaa_update'),
    url(r'^ccaa_report/$', 'ccaa_report', name='ccaa_report'),
    url(r'^cdr_list/$', 'cdr_list', name='cdr_list'),
    url(r'^local_traffic_report/(?P<pk>\w+)/$',
        'local_traffic_report', name='local_traffic_report'),
    url(r'^voip_local_traffic_report/(?P<pk>\w+)/$',
        'voip_local_traffic_report', name='voip_local_traffic_report'),
    url(r'^mobile_traffic_report/(?P<pk>\w+)/$',
        'mobile_traffic_report', name='mobile_traffic_report'),
    url(r'^voip_mobile_traffic_report/(?P<pk>\w+)/$',
        'voip_mobile_traffic_report', name='voip_mobile_traffic_report'),
    url(r'^national_traffic_report/(?P<pk>\w+)/$',
        'national_traffic_report', name='national_traffic_report'),
    url(r'^load/$', 'load', name='load'),
)
