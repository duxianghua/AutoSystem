from django.conf.urls import url
from CMDB.views import *

urlpatterns = [
	url(r'^area',area_views,name='area'),
	url(r'^ec2$',ec2_instance,name='ec2'),
	url(r'^hosts$',hosts_list,name='hosts'),
	url(r'^hosts/add$',add_hosts,name='hosts_add'),
	url(r'^app_category',app_category_views,name='app_category'),
	url(r'^import_hosts',import_hosts,name='import_hosts'),

]