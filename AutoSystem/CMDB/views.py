#coding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from CMDB.models import *
from CMDB.AWS_API import aws_api
import json
import time
from django.contrib.auth.decorators import login_required
from django.core.serializers import serialize,deserialize

# Create your views here.
# ec2 instance manager
@login_required
def ec2_instance(request):
    action = request.GET.get('action')
    if action == "update":
        areaid = request.GET.get('areaid')
        try:
            ec2 = aws_api(areaid)
            c = ec2.get_aws_instances()
            status = {'status':'ok','value':c}
        except Exception,e:
            a=str(e)
            status = {'status':'error','value':a}
        return HttpResponse(json.dumps(status))
    elif action == "get_ec2":
        areaid = request.GET.get('areaid')
        instances_list = ec2_instances.objects.filter(ec2_area=area.objects.get(pk=areaid))
        return render(request,'CMDB/ec2_instances_table.html',locals())
    else:
        instances_list = ec2_instances.objects.filter(ec2_area=area.objects.all()[0])
        area_list = area.objects.all()
        return render(request,'CMDB/ec2.html',locals())

@login_required
def hosts_list(request):
    action = request.GET.get("action")
    areaid = request.GET.get('areaid')
    if action == "select":
        hosts_list = hosts.objects.filter(host_area=area.objects.get(pk=areaid))
        return render(request,'CMDB/hosts_table.html',locals())
    else:
        area_list = area.objects.all()
        hosts_list = hosts.objects.all()
        return render(request,'CMDB/hosts.html',locals())

@login_required
def add_hosts(request):
    if request.method =='GET':
        area_list=area.objects.all()
        app_cate_list = app_category.objects.all()
        return render(request,'CMDB/add_host.html',locals())
    elif request.method =='POST':
        host_name = request.POST.get('hostname')
        host_ip = request.POST.get('ipaddress')
        host_available = request.POST.get('enabled')
        area_id = request.POST.get('area')
        app_cate = request.POST.get('app_cate')
        if host_name and host_ip and area_id and app_cate:
            if host_available == 'on':
                host_available = 1
            else:
                host_available = 0
            try:
                hosts.objects.create(
                    host_name = host_name,
                    host_ip = host_ip,
                    host_area = area.objects.get(pk=area_id),
                    host_available = host_available,
                    )
                rev = {'status':'ok','val':'null'}
            except Exception,e:
                rev = {'status':'error','val':e.__str__()}
        else:
            rev = {'status':'error','val':'有参数为空'}
        return HttpResponse(json.dumps(rev))

@login_required
def import_hosts(request):
    action = request.GET.get("action")
    area_id = request.GET.get("areaid")
    if action == "import":
        ec2_list = ec2_instances.objects.filter(ec2_area = area.objects.get(pk=area_id))
        for i in ec2_list:
            try:
                if i.ec2_state == "running":
                    available = 1
                else:
                    available = 0
                obj = hosts.objects.get(host_ip=i.ec2_private_ip)
                obj.host_name=i.ec2_tags
                obj.display_name=i.ec2_tags
                obj.host_available=available
                obj.host_area=i.ec2_area
                obj.save()
            except hosts.DoesNotExist,e:
                if i.ec2_state == "running":
                    available = 1
                else:
                    available = 0
                hosts.objects.create(
                    host_name=i.ec2_tags,
                    display_name=i.ec2_tags,
                    host_available=available,
                    host_area=i.ec2_area,
                    host_ip = i.ec2_private_ip,
                )
        rev = {'status':'ok','val':'null'}
    return HttpResponse(json.dumps(rev))

@login_required
def app_category_views(request):
    user = request.user
    if request.method =='GET':
        action = request.GET.get('action')
        if action == 'add':
            return render(request,'CMDB/add_app_category.html')
        if action == 'edit':
            CateId = request.GET.get('id')
            hosts_list = hosts.objects.exclude(id__in=app_cate_hosts.objects.filter().values('host_id'))
            data = app_category.objects.get(pk=CateId)
            ExistHosts =data.app_cate_hosts_set.all()
            return render(request,'CMDB/AppCate_edit.html',locals())
        else:
            AppCateList = app_category.objects.all()
            hosts_list = hosts.objects.all()
            HostCounts = {}
            for i in AppCateList:
                HostCounts[i.app_category_name]=i.app_cate_hosts_set.count()
            return render(request,'CMDB/AppCategoryList.html',locals())
    elif request.method =='POST':
        cate_name = request.POST.get('app_cate_name',)
        cate_desc = request.POST.get('app_cate_desc',)
        id = request.POST.get('id',)
        action = request.POST.get('action',)
        hostid = request.POST.getlist('hostid_lift',)
        if action == 'delete':
            try:
                app_category.objects.get(pk=id).delete()
                rev = {'status':'ok','val':'null'}
            except Exception,e:
                rev = {'status':'error','val':e.__str__()}
        elif id and cate_name:
            obj = app_category.objects.get(pk=id)
            obj.app_category_name=cate_name
            obj.app_category_desc=cate_desc
            obj.save()
            rev = {'status':'ok','val':'null'}
            if hostid:
                NewHostID = map(int,hostid)
                OldHostID = [i.host_id_id for i in app_cate_hosts.objects.filter(app_category_id=id)]
                try:
                    app_cate_hosts.objects.filter(host_id__in=set(OldHostID)-set(NewHostID)).delete()
                except Exception,e:
                    print e
                for i in set(NewHostID)-set(OldHostID):
                    try:
                        app_cate_hosts.objects.create(
                            app_category_id=app_category.objects.get(pk=id),
                            host_id = hosts.objects.get(pk=i)
                        )
                    except Exception:
                        pass
        elif cate_name:
            try:
                app_category.objects.create(app_category_name=cate_name,app_category_desc=cate_desc)
                rev = {'status':'ok','val':'null'}
            except Exception,e:
                rev = {'status':'error','val':e.__str__()}
        else:
            rev = {'status':'error','val':'is null'}
        return HttpResponse(json.dumps(rev))

@login_required
def area_views(request):
    user = request.user
    print user
    if request.method =='GET':
        action = request.GET.get('action')
        if action == 'add':
            return render(request,'CMDB/add_app_category.html')
        elif action == 'del':
            return render(request,'CMDB/add_app_category.html')
        elif action == 'edit':
            areaid = request.GET.get('id')
            AreaInfo = area.objects.get(pk=areaid)
            #return JsonResponse(serialize('json',data), safe=False)
            #return HttpResponse(serialize('json',data),content_type="application/json")
            return render(request,"CMDB/area_edit.html",locals())
        else:
            area_list = area.objects.all()
            area_count={}
            for i in area_list:
                area_count[i.area_name]=i.ec2_instances_set.count()
            return render(request,"CMDB/area.html",locals())
    elif request.method =='POST':
        area_name = request.POST.get('area_name',)
        area_account = request.POST.get('area_account',)
        area_password = request.POST.get('area_password',)
        area_access_key = request.POST.get('area_access_key',)
        area_private_key = request.POST.get('area_private_key',)
        area_region = request.POST.get('area_region',)
        area_desc = request.POST.get('area_desc',)
        if area_name:
            try:
                area.objects.create(
                    area_name=area_name,
                    area_account=area_account,
                    area_password=area_password,
                    area_access_key=area_access_key,
                    area_private_key=area_private_key,
                    area_region=area_region,
                    area_desc=area_desc,
                )
                rev = {'status':'ok','val':'null'}
            except Exception,e:
                obj=area.objects.get(area_name=area_name)
                obj.area_account=area_account
                obj.area_password=area_password
                obj.area_access_key=area_access_key
                obj.area_private_key=area_private_key
                obj.area_region=area_region
                obj.area_desc=area_desc
                obj.save()
                rev = {'status':'ok','val':'null'}
                #rev = {'status':'error','val':e.__str__()}
        else:
            rev = {'status':'ok','val':u'参数为空'}
        return HttpResponse(json.dumps(rev))

