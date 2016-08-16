from django.conf.urls import url,include
from django.contrib import admin
from AUTH.views import *

urlpatterns = [
	url(r'^$',index,name='index'),
    url(r'login',login,name='login'),
    #url(r'^login/$', 'django.contrib.auth.views.login',{'template_name': 'AUTH/login.html'}),
    url(r'logout',logout,name='logout'),
]