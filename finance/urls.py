from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^login/', 'finance.views.login', name='login'),
    url(r'^createUser/', 'finance.users.views.createUser', name='create'),
    url(r'^logout/', 'finance.views.logout', name='logout'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    url(r'^corepage/(?P<foobar>.+)/$','finance.views.corepage',name='corepage'),
    url(r'^budget/(?P<foobar>.+)/$','finance.views.budget',name='budget'),
    url(r'^approve/(?P<foobar>.+)/$', 'finance.views.approve', name='approve'),
    url(r'^reject/(?P<foobar>.+)/$', 'finance.views.reject', name='reject'),
    # url(r'^finance/', include('finance.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
