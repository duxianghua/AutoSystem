#coding: utf-8
from __future__ import unicode_literals
from django.db import models

# Create your models here.

class area(models.Model):
    area_name = models.CharField(max_length=20,unique="True",verbose_name='area')
    area_account = models.CharField(max_length=50,null="Ture",blank='Ture')
    area_password = models.CharField(max_length=50,null="Ture",blank='Ture')
    area_access_key =  models.CharField(max_length=100,null="Ture",blank='Ture')
    area_private_key =  models.CharField(max_length=100,null="Ture",blank='Ture')
    area_region = models.CharField(max_length=50,null="Ture",blank='Ture')
    area_desc = models.TextField(max_length=200,null="Ture",blank='Ture')
    def __str__(self):
        return self.area_name
    class Meta:
        verbose_name = u'AWS_区域'
        verbose_name_plural = u'区域列表'

class ec2_instances(models.Model):
    ec2_area = models.ForeignKey(area)
    ec2_tags = models.CharField(max_length=100,null="Ture",blank='Ture')
    ec2_type = models.CharField(max_length=48)
    ec2_id = models.CharField(max_length=48)
    ec2_private_ip = models.CharField(max_length=48)
    ec2_public_ip = models.CharField(max_length=48)
    ec2_state = models.CharField(max_length=48)
    ec2_create_time = models.DateTimeField(verbose_name='instance create time')
    def __str__(self):
        return self.ec2_tags
    class Meta:
        verbose_name = 'AWS_EC2_Instance'
        verbose_name_plural = 'EC2_Instance_list'

class hosts(models.Model):
    host_name = models.CharField(max_length=50,unique=True)
    display_name = models.CharField(max_length=50,null="Ture",blank='Ture')
    host_ip = models.CharField(max_length=16,unique=True)
    host_available = models.IntegerField(default=1)
    host_area = models.ForeignKey(area)
    def __str__(self):
        return self.host_name
    class Meta:
        verbose_name = u'主机'
        verbose_name_plural = u'主机列表'

class app_category(models.Model):
    app_category_name = models.CharField(max_length=50,unique=True)
    app_category_desc = models.TextField(max_length=400,null="Ture",blank='Ture')
    def __str__(self):
        return self.app_category_name
    class Meta:
        verbose_name = u'应用分组'
        verbose_name_plural = u'分组列表'

class projects(models.Model):
    project_name = models.CharField(max_length=50,unique=True)
    project_desc = models.TextField(max_length=400,null="Ture",blank='Ture')
    def __str__(self):
        return self.projects_name
    class Meta:
        verbose_name = u'项目分组'
        verbose_name_plural = u'项目列表'

class project_hosts(models.Model):
    project_id = models.ForeignKey(projects)
    host_id = models.ForeignKey(hosts)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.project_id.project_name
    class Meta:
        verbose_name = u'项目 Map 主机'
        verbose_name_plural = u'项目 Map 主机'

class app_cate_hosts(models.Model):
    app_category_id = models.ForeignKey(app_category)
    host_id = models.OneToOneField(hosts,unique=True)
    status = models.IntegerField(default=1)
    def __str__(self):
        return self.app_category_id.app_category_name
    class Meta:
        verbose_name = u'应用类型 Map 主机'
        verbose_name_plural = u'应用类型 Map 主机'


