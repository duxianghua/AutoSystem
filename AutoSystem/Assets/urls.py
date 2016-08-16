from django.conf.urls import url
from Assets.views import *

urlpatterns = [
	url(r'^$',area),
	url(r'^area',area),
	url(r'^host_info/(?P<area>.*)',host,name="host"),
	url(r'^get_host_info/(?P<host>.*)',get_host_info),
	url(r'^get_group_hosts',get_group_hosts),
	url(r'^instances/(?P<action>.*)',aws_instances,name="instances"),
	url(r'^project_host',get_project_hosts),
]