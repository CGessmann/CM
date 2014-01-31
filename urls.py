from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.views.generic import TemplateView
import settings
from cm.models import Configuration, UserProfile, Paper
from cm.utils.my_views import *

from cm.views import *
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
	
	url(r'', include('social_auth.urls')),

    ###################################################
    # Confmaster starts here
    url(r'^$', TemplateView.as_view(template_name='cm/home.html'), name="start"),
    url(r'^configuration/$', MyListView.as_view(model=Configuration), name='configuration'),
    url(r'^chair/person/list/$', MyListView.as_view(model=UserProfile),
        name='personList'),
    url(r'^chair/person/edit/(?P<pk>[0-9]+)/$', PersonView.as_view(),
        name='editPerson'),
    # url(r'^chair/person/add/$', 'cm.views.person_view'),
    url(r'^chair/person/add/$', PersonView.as_view(pk=None, title='Add Person'),
        name='addPerson'),
    url(r'    ^chair/paper/edit/(?P<paperID>[0-9]+)/$', 'cm.views.paper_view',
        name='editPaper'),
    url(r'^author/paper/add/$', PaperView.as_view(pk=None), name='add_paper'),
    url(r'^chair/paper/list/$', MyListView.as_view(model=Paper),
        name='paperList'),
    url(r'^author/paper/delete/(?P<pk>[0-9]+)/?$', PaperDelete.as_view(),
        name='deletePaper'),
    url(r'^$', TemplateView.as_view(template_name='cm/home.html'), name="start"),


    # Login etc.
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'cm/login.html'},
        name='login'),
    url(r'^accounts/logout$', 'django.contrib.auth.views.logout_then_login',
        name='logout'),
    url(r'^accounts/password/reset/$', 'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/accounts/password/reset/done/',
         'template_name': 'registration/password_reset_form.html'},
        name='passwordForgotten'),
    url(r'^accounts/password/reset/done/$', 'django.contrib.auth.views.password_reset_done'),
    url(r'^accounts/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/accounts/password/done/'},
        name="password_reset_confirm"),
    url(r'^accounts/password/done/$', 'cm.views.password_reset_done'),
    url(r'^accounts/su/(?P<pk>[0-9]+)?/$', 'cm.views.su',
        name='su'),
    url(r'^accounts/su/$', 'cm.views.su',
        name='su'),
    url(r'^accounts/person/delete/(?P<pk>[0-9]+)/?$', UserProfileDelete.as_view(),
        name='deletePerson'),

    # Ajax
    url(r'^typeahead/affiliation1$', 'cm.views.get_affiliation'),

)

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))