from django.conf.urls import url
from Assets.views import *
from django.views.generic import View
from django.views import generic
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

class MyView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, World!')

class DetailView(generic.DetailView):
    model = Host
    template_name = 'assets/name.html'

class IndexView(generic.ListView):
	template_name = 'assets/name.html'
	context_object_name = 'page'

	def get_queryset(self):
		data = Host.objects.all()
		return Paginator(data, 10).page(1)

urlpatterns = [
	url(r'^test$',get_name,name="test"),
	url(r'^tree$', tree, name="tree"),
	url(r'^tree1$', tree1, name="tree1"),
	url(r'^$', area),
	url(r'^name$', get_name),
	url(r'^add_branch', add_branch, name="add_branch"),
	url(r'^add_tag', add_tag, name="add_tag"),
	url(r'^area', area),
	url(r'^host_info/(?P<area>.*)', host, name="host"),
	url(r'^get_host_info/(?P<host>.*)', get_host_info),
	url(r'^get_group_hosts', get_group_hosts),
	url(r'^instances/(?P<action>.*)', aws_instances, name="instances"),
	url(r'^project_host', get_project_hosts),
]