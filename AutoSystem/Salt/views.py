#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from Salt.SaltAPI import *
from Assets.models import *
from Salt.models import *
import json
from Salt.get_hostinfo import *
import re

@login_required
def salt_key(request,area='null'):
    if area == 'null':
        return render(request, 'SALT/salt_info.html')
    else:
        try:
            Area.objects.get(area_name=area)
            api_info = Salt_info.objects.get(Area_name=area)
            salt = Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
            minions,minions_pre = salt.ListKey()
            context = {'minions':minions,'minions_pre':minions_pre}
            return render(request, 'SALT/salt_info.html', context)
        except Exception,e:
            return HttpResponse(e)

@login_required
def execution(request):
    clients={'1':'execution','2':'execution','3':'wheel','4':'wheel','5':'runner','6':'runner'}
    clientid=request.GET.get('client')
    moduleid=request.GET.get('module')
    if clientid:
        if clients[clientid] == 'execution':
            keyid=request.GET.get('key')
            cmd=request.GET.get('cmd')
            fun=Command.objects.get(pk=moduleid)
            api_info = Salt_info.objects.get(Area_name='staging')
            salt = Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
            if cmd:
                rev=salt.Salt_CMD(tgt=keyid,fun=fun,arg=cmd,expr_form='list')
            else:
                rev=salt.Salt_CMD(tgt=keyid,fun=fun,expr_form='list')
            return HttpResponse(json.dumps(rev['return'][0]))
        elif clients[clientid] == 'runner':
            fun=Command.objects.get(pk=moduleid)
            api_info = Salt_info.objects.get(Area_name='staging')
            salt = Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
            rev = salt.SaltRunner(fun,'runner')
            print fun
            return HttpResponse(json.dumps(rev['return'][0]))
    else:
        group_list = group.objects.order_by('group_name')
        area_list = Area.objects.all().values('area_name')
        return render(request,'SALT/execution.html',locals())

@login_required
def modules(request,active):
    funs=['doc.runner','doc.wheel','doc.execution']
    if active == 'update':
        for fun in funs:
            try:
                api_info = Salt_info.objects.get(pk=1)
                salt = Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
                res = salt.SaltRunner(fun,'runner')
                data = res['return'][0]
                for i in data:
                    Module.objects.get_or_create(client=fun.split('.')[1],name=i.split('.')[0])
                    module = Module.objects.get(client=fun.split('.')[1],name=i.split('.')[0])
                    Command.objects.get_or_create(cmd=i,module=module)
                    command = Command.objects.get(cmd=i,module=module)
                    if not command.doc:
                        command.doc = data[i]
                        command.save()
                status = u'命令收集完成'
            except Exception,e:
                status = e
        return HttpResponse(json.dumps(status))
    elif active == 'doc':
        id = request.GET.get('id')
        doc = Command.objects.get(pk=id).doc
        data = doc.replace("\n","<br>").replace(" ","&nbsp;")
        return HttpResponse(json.dumps(data))
    elif active == 'get':
        clients={'1':'execution','2':'execution','3':'wheel','4':'wheel','5':'runner','6':'runner'}
        client_id=request.GET.get('clientid')
        if client_id in clients:
            module_name=request.GET.get('module')
            if module_name:
                cmd_list = Command.objects.filter(module=Module.objects.get(name=module_name,client=clients[client_id])).values('id','cmd').order_by('cmd')
                return HttpResponse(json.dumps(list(cmd_list)))
            else:
                modules = Module.objects.filter(client=clients[client_id]).values('name').order_by('name')
                return HttpResponse(json.dumps(list(modules)))
        cmd_list=Command.objects.order_by('cmd')
        return render(request,'SALT/modules.html',locals())
    else:
        cmd_list=Command.objects.order_by('cmd')
        return render(request,'SALT/modules.html',locals())


@login_required
def select_area(request):
    area = request.GET.get('area')
    context={}
    if area:
        api_info = Salt_info.objects.filter(Area_name=area)
        if api_info:
            api_info = api_info[0]
            salt=Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
            if salt.status == 0:
                context['data'] = u"SALT登录成功 <br> %s" %(api_info.salt_api_url)
                context['status'] = 0

            else:
                context['data'] = u"SALT登录失败"
                context['status'] = 1
        else:
            context['data'] = u"未能找到SALT接口信息"
            context['status'] = 1
    else:
        context['data'] = u"未选择区域"
        context['status'] = 1
    return HttpResponse(json.dumps(context))

@login_required
def update_host_info(request):
    obj = get_hostinfo('staging')
    obj.update_area_host()
    return HttpResponse("asdfsfs")

def get_service(request):
    hostid=request.GET.get('hostid')
    match=request.GET.get('match')
    service=request.GET.get('service')
    _project=request.GET.get('project')
    service_list = []
    if hostid and _project:
        hostid_list=hostid.split(',')
        api_info = Salt_info.objects.filter(Area_name='Staging')
        if api_info:
            api_info=api_info[0]
            salt=Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
            if salt.status == 0:
                try:
                    for hostid in hostid_list:
                        salt_host_key = Host.objects.get(id=int(hostid)).salt_key_name
                        data = salt.Salt_CMD(fun='service.get_all',tgt=salt_host_key)
                        match_re=project.objects.get(project_name=_project).sevice_filter_re
                        list = data['return'][0]
                        l1 = [ i for i in list[salt_host_key] if re.match(match_re,i) ]
                        if l1:
                            if match:
                                l2 = [ i for i in l1 if re.match(match,i) ]
                                list[salt_host_key]=l2
                            else:
                                list[salt_host_key]=l1
                        service_list.append(list)
                    return render(request, 'Assets/test.html', locals())
                except re.error:
                    return HttpResponse("<h2 style='color:red'>正则错误</h2>")
    else:
        project_list = project.objects.all()
        return render(request, 'Assets/services.html', locals())


def get_service_status(request):
    service=request.GET.get('service')
    host=request.GET.get('host')
    api_info = Salt_info.objects.filter(Area_name='Staging')[0]
    salt=Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
    if service and host:
        data = salt.Salt_CMD(fun='service.status',tgt=host,arg=service)
        return HttpResponse(json.dumps(data['return'][0][host]))


def turn_service(request):
    host=request.GET.get('host')
    action='service.'+request.GET.get('action')
    service=request.GET.get('service')
    api_info = Salt_info.objects.filter(Area_name='Staging')
    if api_info:
        api_info=api_info[0]
        salt=Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
        if salt.status == 0:
            #salt_host_key = Host.objects.get(host_name=host).salt_key_name
            data = salt.Salt_CMD(fun=action.lower(),tgt=host,arg=service)
            return HttpResponse(json.dumps(data['return'][0][host]))

def code_manager(request):
    action = request.GET.get('action')
    project_name = request.GET.get('project')
    cmd_data = project.objects.get(project_name=project_name).code_update_cmd
    if cmd_data:
        cmd = json.loads(cmd_data)[action]
        api_info = Salt_info.objects.filter(Area_name='Staging')[0]
        salt=Salt_api(api_info.salt_api_url,api_info.salt_api_account,api_info.salt_api_password)
        if action == 'pull':
            arg="su -c '"+cmd+"' deploy"
            data = salt.Salt_CMD(fun='cmd.run',tgt='admin-staging.stargt.com.my',arg=arg)
        else:
            data = salt.Salt_CMD(fun='cmd.run',tgt='admin-staging.stargt.com.my',arg=cmd)
        return HttpResponse(json.dumps(data['return'][0]['admin-staging.stargt.com.my']))
    else:
        return HttpResponse(json.dumps('你没请我吃饭,所以此项目暂时无法进行代码管理.'))
