#coding: utf-8
from Assets.models import Area
from django.db import models

class Salt_info(models.Model):
    salt_api_name = models.CharField(max_length=16,null="Ture")
    salt_api_url = models.CharField(max_length=100)
    salt_api_account = models.CharField(max_length=16)
    salt_api_password = models.CharField(max_length=16)
    Area_name = models.ForeignKey(Area)
    description = models.CharField(max_length=200,null="Ture",blank='Ture')
    def __unicode__(self):
        return  self.salt_api_name
    class Meta:
        verbose_name = u'Salt_info帐号信息'
        verbose_name_plural = u'Salt API登录信息'

class Module(models.Model):
    client = models.CharField(max_length=20,default='execution',verbose_name=u'Salt模块类型')
    name = models.CharField(max_length=20,verbose_name=u'Salt模块名称')
    def __unicode__(self):
        return self.name
    class Meta:
        verbose_name = u'Salt模块'
        verbose_name_plural = u'Salt模块列表'
        unique_together = ("client", "name")

class Command(models.Model):
    cmd = models.CharField(max_length=100,verbose_name=u'Salt命令')
    doc = models.TextField(max_length=1000,blank=True,verbose_name=u'帮助文档')
    module = models.ForeignKey(Module,verbose_name=u'所属模块')
    def __unicode__(self):
        return  self.cmd
    class Meta:
        verbose_name = u'Salt命令'
        verbose_name_plural = u'Salt命令列表'
