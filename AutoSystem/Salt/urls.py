from django.conf.urls import url
from Salt.views import *

urlpatterns = [
	url(r'^$',salt_key),
	url(r'^select_area$',select_area,name='select_area'),
	url(r'^salt_key$',salt_key),
	url(r'^salt_key/(?P<area>.*)$',salt_key),
	url(r'^execution$',execution,name='execution'),
	url(r'^modules/(?P<active>.*)$',modules,name='modules'),
	url(r'^update$',update_host_info,name='update'),
	url(r'^get_service$',get_service),
	url(r'^get_services_status',get_service_status),
	url(r'^turn_service',turn_service),
	url(r'^code$',code_manager),
]