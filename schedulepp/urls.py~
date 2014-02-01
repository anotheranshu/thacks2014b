from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from sorude import views


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'sorude.views.home', name='home'),
    # url(r'^sorude/', include('sorude.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
    url(r'^facebook_login/', views.fb_auth, name='fb_auth'),
)
