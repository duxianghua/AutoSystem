#coding: utf-8
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from models import *
import json
import os
import boto3

# Create your views here.

@login_required
def index(request):
    return render(request,'common/base.html')

@login_required
def area(request):
    area_list=Area.objects.all()
    return render(request,'Assets/area_info.html',locals())

@login_required
def host(request,area):
    area_name = area
    print area_name
    host_list = Host.objects.filter(area=area_name)
    return render(request,'Assets/host_info.html',locals())

@login_required
def get_host_info(request,host="Null"):
    if host == "Null":
        return HttpResponse('URL Error')
    else:
        try:
            host = servers_info.objects.get(host_name=host)
            host.disk_total = host.disk_total * 1024
            host.p_mem = host.p_mem * 1024
            host.v_mem = host.v_mem * 1024
            return render(request,'Assets/tanchuang.html',locals())
        except Exception,e:
            return HttpResponse(e)

@login_required
def get_group_hosts(request):
    group_name = request.GET.get('group')
    import json
    reload(json)
    try:
        hosts = Host.objects.filter(group='').values('host_name','salt_key_name')
        for i in group_name.split(','):
            data=Host.objects.filter(group=i).values('host_name','salt_key_name')
            hosts=data|hosts
        print hosts
        return HttpResponse(json.dumps(list(hosts)))
    except Exception,e:
        return HttpResponse(e)

@login_required
def aws_instances(request,action):
    if action == "update":
        area = request.GET.get('area')
        if area:
            areaID = Area.objects.filter(area_name=area)
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
    project = request.GET.get('project')
    if project:
        hosts = {}
        data = project_host.objects.filter(project=project)
        for i in data:
            hosts[i.host.host_name]={"id":i.host.id}
            #hosts.append({i.host.host_name})
        print hosts
        return HttpResponse(json.dumps(hosts))
    else:
        return HttpResponse(json.dumps(u"未选择提交项目"))
