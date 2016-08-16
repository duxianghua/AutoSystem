from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ZABBIX.ZabbixAPI import *
import ConfigParser

# Create your views here.
@login_required
def get_zabbix_host(request):
    cf = ConfigParser.ConfigParser()
    cf.read("AutoSystem/config.ini")
    graphurl = cf.get("zabbix_server","graphurl")
    try:
        zapi=ZabbixAPI()
        host_list=zapi.HostGet()
        #group_list=zapi.HostGroupGet()
        #template_list=zapi.TemplateGet()
    except Exception as e:
        error=str(e)
    return render(request, 'ZABBIX/zabbix.html', locals())

@login_required
def get_graph(request):
    hostid=request.GET.get('hostid','')
    try:
        zapi=ZabbixAPI()
        host_list=zapi.HostGet()
        if hostid:
            graph_list=zapi.GraphGet(hostid=hostid)
        else:
            hostid=host_list[0]['hostid']
            graph_list=zapi.GraphGet(hostid=hostid)
    except Exception as e:
        error=str(e)
    return render(request, 'ZABBIX/zabbix.html', locals())

