#coding: utf-8
"""AutoSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.conf.urls import handler404, handler500
from django.contrib import admin
from AUTH.views import index

urlpatterns = [
	#默认首页
	url(r'^$',index,name='index'),
	url(r'^auth/', include('AUTH.urls',namespace='auth')),
	#url(r'^',include('Assets.urls')),
	url(r'^salt/', include('Salt.urls',namespace='SALT')),
	url(r'^assets/', include('Assets.urls',namespace='CMD')),
	url(r'^zabbix/',include('ZABBIX.urls',namespace='ZABBIX')),
	url(r'^admin/', admin.site.urls),
]

handler500 = "AutoSystem.views.page_500"
handler404 = "AutoSystem.views.page_404"