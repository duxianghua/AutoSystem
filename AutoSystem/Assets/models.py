from __future__ import unicode_literals
from django.db import models

class Area(models.Model):
	area_name = models.CharField(primary_key='Ture',max_length=20)
	area_url = models.CharField(max_length=100,null='Ture',blank='Ture')
	area_account = models.CharField(max_length=50,null="Ture",blank='Ture')
	area_password = models.CharField(max_length=50,null="Ture",blank='Ture')
	area_access_key =  models.CharField(max_length=100,null="Ture",blank='Ture')
	area_private_key =  models.CharField(max_length=100,null="Ture",blank='Ture')
	area_region = models.CharField(max_length=50,null="Ture",blank='Ture')
	area_description = models.CharField(max_length=200,null="Ture",blank='Ture')
	def __str__(self):
		return self.area_name

class group(models.Model):
	group_name = models.CharField(max_length=20,unique=True)
	group_desc = models.CharField(max_length=200,null="Ture",blank='Ture')
	def __str__(self):
		return self.group_name

class Host(models.Model):
	host_name = models.CharField(max_length=100)
	host_nip = models.CharField(max_length=16,unique=True)
	host_wip = models.CharField(max_length=16,null="Ture",blank='Ture')
	group = models.ForeignKey(group,to_field='group_name')
	area = models.ForeignKey(Area,to_field='area_name')
	salt_key_name = models.CharField(max_length=100,default='UNknow')
	host_status = models.CharField(max_length=16,default='Active')
	host_desc = models.CharField(max_length=200,null="Ture",blank='Ture')
	def __str__(self):
		return self.host_name


class servers_info(models.Model):
	host_name = models.CharField(max_length=100,null="Ture",blank='Ture')
	host_ip = models.ForeignKey(Host,to_field='host_nip')
	p_mem = models.IntegerField()
	v_mem = models.IntegerField()
	cpu_models = models.CharField(max_length=48)
	cpu_count = models.IntegerField()
	system_type = models.CharField(max_length=20)
	disk_total = models.IntegerField()
	kernel_version = models.CharField(max_length=50)
	update_time = models.DateTimeField('last update time')
	def __str__(self):
		return self.host_name

class AWS_INSTANCES(models.Model):
	instance_area = models.ForeignKey(Area,to_field='area_name')
	instance_tags = models.CharField(max_length=100,null="Ture",blank='Ture')
	instance_type = models.CharField(max_length=48)
	instance_id = models.CharField(max_length=48)
	instance_private_ip = models.CharField(max_length=48)
	instance_public_ip = models.CharField(max_length=48)
	instance_state = models.CharField(max_length=48)
	instance_create_time = models.DateTimeField('instance create time')
	def __str__(self):
		return self.instance_id
class project(models.Model):
	project_name = models.CharField(max_length=100,unique="True")
	sevice_filter_re = models.CharField(max_length=100)
	project_desc = models.CharField(max_length=200,null="Ture",blank='Ture')
	project_logs_path = models.CharField(max_length=1000,null="Ture",blank='Ture')
	code_update_cmd = models.CharField(max_length=1000,null="Ture",blank='Ture')
	def __str__(self):
		return self.project_name

class project_host(models.Model):
	project = models.ForeignKey(project,to_field="project_name")
	host = models.ForeignKey(Host)