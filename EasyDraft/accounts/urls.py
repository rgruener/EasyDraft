from django.contrib.auth.views import login, logout, password_reset, password_reset_done, password_change, password_change_done
from django.conf.urls import patterns, include, url

urlpatterns = patterns('accounts.views',
    url(r'^register/$', 'register'), 
    url(r'^delete/$', 'delete'), 
    url(r'^login/$', login),
    url(r'^logout/$', logout),
    url(r'^password/change/$', password_change), 
    url(r'^password/change/success/$', password_change_done), 
    url(r'^password/reset/$', password_reset), 
    url(r'^password/reset/success/$', password_reset_done), 
    url(r'^email/change/$', 'change_email'),
)
