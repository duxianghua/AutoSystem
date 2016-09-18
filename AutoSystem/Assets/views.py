#coding: utf-8
#from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse,Http404
from models import *
import json
import os
import boto3
from .form import *
from Salt.GitLabAPI import *
from Salt.FileManager import *
from Salt.GitAPI import *
# Create your views here.


def get_name(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = HostsFrom()
    return render(request, 'Assets/name.html', locals())

def add_branch(request):
    '''
    添加git banch
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = AddBranchFrom(request.POST)
        if form.is_valid():
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            repo = GitAPI(os.path.join(BASE_DIR,'config'))
            repo.branch(form.cleaned_data['branch_name'])
            return HttpResponseRedirect('/assets/tree')
        else:
            return HttpResponseRedirect('/assets/tree')
    else:
        form = AddBranchFrom(initial={'Create_from':'master'})
    return render(request, 'Forms/add_branch.html', locals())

def add_tag(request):
    '''
    添加git tag
    :param request:
    :return:
    '''
    if request.method == 'POST':
        form = AddTagFrom(request.POST)
        if form.is_valid():
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            repo = GitAPI(os.path.join(BASE_DIR,'config'))
            repo.tags(form.cleaned_data['tag_name'],form.cleaned_data['message'])
            return HttpResponseRedirect('/assets/tree')
        else:
            return HttpResponseRedirect('/assets/tree')
    else:
        form = AddTagFrom(initial={'Create_from':'master'})
    return render(request, 'Forms/add_tag.html', locals())

def autopage(request):
    contact_list = Host.objects.all()
    p = Paginator(contact_list, 12)


@login_required
def index(request):
    return render(request, 'common/base.html')


@login_required
def area(request):
    area_list = Area.objects.all()
    return render(request,'Assets/area_info.html',locals())


@login_required
def host(request,area):
    area_name = area
    print area_name
    host_list = Host.objects.filter(area=area_name)
    return render(request, 'Assets/host_info.html',locals())


@login_required
def get_host_info(request, host="Null"):
    if host == "Null":
        return HttpResponse('URL Error')
    else:
        try:
            host = servers_info.objects.get(host_name=host)
            host.disk_total = host.disk_total * 1024
            host.p_mem = host.p_mem * 1024
            host.v_mem = host.v_mem * 1024
            return render(request,'Assets/tanchuang.html', locals())
        except Exception,e:
            return HttpResponse(e)


@login_required
def get_group_hosts(request):
    group_name = request.GET.get('group')
    import json
    reload(json)
    try:
        hosts = Host.objects.filter(group='').values('host_name', 'salt_key_name')
        for i in group_name.split(','):
            data = Host.objects.filter(group=i).values('host_name', 'salt_key_name')
            hosts1 = data|hosts
        print hosts1
        return HttpResponse(json.dumps(list(hosts)))
    except Exception, e:
        return HttpResponse(e)


@login_required
def aws_instances(request, action):
    if action == "update":
        _areaname = request.GET.get('area')
        if area:
            areaID = Area.objects.filter(area_name = _areaname)
            os.environ["AWS_DEFAULT_REGION"]=areaID[0].area_region
            os.environ["AWS_ACCESS_KEY_ID"]=areaID[0].area_access_key
            os.environ["AWS_SECRET_ACCESS_KEY"]=areaID[0].area_private_key
            instance_area = areaID[0]
            ec2=boto3.resource('ec2')
            data=ec2.instances.all()
            for i in data:
                tags = i.tags[0]['Value']
                type = i.instance_type
                id = i.instance_id
                create_time = i.launch_time
                private_ip = i.private_ip_address
                public_ip = i.public_ip_address
                state = i.state['Name']
                if not public_ip:
                    public_ip="null"
                try:
                    obj = AWS_INSTANCES.objects.get(instance_id=id)
                    obj.instance_area=instance_area
                    obj.instance_tags=tags
                    obj.instance_type=type
                    obj.instance_id=id
                    obj.instance_create_time=create_time
                    obj.instance_private_ip=private_ip
                    obj.instance_public_ip=public_ip
                    obj.instance_state=state
                    obj.save()
                except AWS_INSTANCES.DoesNotExist:
                    AWS_INSTANCES.objects.create(
                        instance_area=instance_area,
                        instance_tags=tags,
                        instance_type=type,
                        instance_id=id,
                        instance_create_time=create_time,
                        instance_private_ip=private_ip,
                        instance_public_ip=public_ip,
                        instance_state=state
                    )
                status = u'实例信息同步完成'
        else:
            status = u'未选择同步区域'
        return HttpResponse(json.dumps(status))
    else:
        instances_list = AWS_INSTANCES.objects.all()
        return render(request,'Assets/instances.html',locals())

def get_project_hosts(request):
    project_name = request.GET.get('project')
    if project_name:
        l = []
        project_log = project.objects.get(project_name=project_name)
        data = project_host.objects.filter(project=project_name)
        for i in data:
            hosts = {}
            hosts['name'] = i.host.host_name
            hosts['id']= i.host.id
            l.append(hosts)
        back_data = {'log':project_log.project_logs_path,'hosts':l}
        return HttpResponse(json.dumps(back_data))
    else:
        return HttpResponse(json.dumps(u"未选择提交项目"))

def tree(request):
    ref = request.GET.get('ref')
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    repo = GitAPI(os.path.join(BASE_DIR,'config'))
    if ref:
        repo.switch_branch(ref)

    branchlist = repo.branch()
    tagslist   = repo.tags()
    return render(request,'Assets/tree.html',locals())

def tree1(request):
    #global status1
    operationcmd = ['delete_node','create_node','rename_node','get_content']
    id = request.GET.get('id')
    ref = request.GET.get('ref')
    operation = request.GET.get('operation')
    filemanager = LocalFileManager()
    if request.method == 'POST':
        data = request.POST.get('data',)
        id   = request.POST.get('id',)
        status,values = filemanager.commint(id,data)
        return HttpResponse(values,status=status)

    if operation in operationcmd:
        type = request.GET.get('type')
        name = request.GET.get('text')
        if operation == 'get_content':
            status,values = filemanager.get_content(id)

        elif operation == 'delete_node':
            status,values = filemanager.delete_node(id)

        elif operation == 'create_node':
            status,values = filemanager.create_node(id,name,type)

        elif operation == 'rename_node':
            status,values = filemanager.rename_node(id,name)

        return HttpResponse(values,status=status)
    else:
        if id != '#' and id and not operation:
            data = filemanager.tree(id)
        else:
            b = filemanager.tree()
            data = [{'id':URLBase64().encode('.'),'icon':'/static/images/folder.png','text':'salt_config','children':b}]

    #if id != '#':
    #    if id.split('::')[0] == 'files':
    #        data = git.raw_blobs(2,path=id.split('::')[1])
    #    elif id.split('::')[0] != 'files':
    #       data = git.get_tree(2,path=id.split('::')[0])
    #if operation:
    #    return HttpResponse(status=400)
    return JsonResponse(data,safe=False)

    #return HttpResponse(data)