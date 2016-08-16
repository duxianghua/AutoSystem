from django.conf.urls import url
from ZABBIX.views import *

urlpatterns = [
	url(r'^$',get_zabbix_host),
    url(r'^graph',get_graph),
]