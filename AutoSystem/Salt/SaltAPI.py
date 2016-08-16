#!/bin/env python
#coding=utf-8
import urllib2, urllib, json
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

class Salt_api:
    def __init__(self,url,username,password):
        self.salt_url = url + '/'
        self.salt_username = username
        self.salt_password = password
        status,value = self.SaltLogin()
        if status == 0:
            self.status = status
            self.salt_token_id = value
        elif status == 1:
            self.status = status
            self.error = value
    def SaltLogin(self):
        params = {'eauth': 'pam', 'username': self.salt_username, 'password': self.salt_password}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        headers = {'X-Auth-Token':''}
        url = self.salt_url + '/login'
        req = urllib2.Request(url, obj, headers)
        try:
            opener = urllib2.urlopen(req,timeout=10)
            content = json.loads(opener.read())
            value = content['return'][0]['token']
            status = 0
            return status,value
        except urllib2.URLError,e:
            status = 1
            value = "could not open URL:%s ERROR:" %(url),e
            return status,e
        except KeyError,e:
            status = 1
            value = e
            return status,value
    def PostRequest(self,obj,prefix='/'):
        url = self.salt_url + prefix
        headers = {'X-Auth-Token': self.salt_token_id}
        req = urllib2.Request(url,obj,headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content
    ##################Salt client interfaces##############################
    def SaltRunner(self,fun,client='runner_async',arg=None,**kwargs):
        params = {'client':client,'fun':fun}
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
    def SaltWheel(self,fun,client='wheel_async',arg=None,**kwargs):
        params = {'client':client,'fun':fun}
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
    def SaltLocal(self,tgt,fun,arg=None,client='local',expr_form='glob'):
        if arg:
            params = {'client':client,'fun':fun,'tgt':tgt,'arg':arg,'expr_form':expr_form}
        else:
            params = {'client':client,'fun':fun,'tgt':tgt,'expr_form':expr_form}
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
    #########################################################################
    ##########################salt-key 操作##################################
    def ListKey(self):
        headers = {'X-Auth-Token': self.salt_token_id}
        params = {'client':'wheel','fun':'key.list_all'}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        req = urllib2.Request(self.salt_url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        minions = content['return'][0]['data']['return']['minions']
        minions_pre = content['return'][0]['data']['return']['minions_pre']
        return minions,minions_pre
    def KeyAccept(self,salt_key_id):
        headers = {'X-Auth-Token': self.salt_token_id}
        params = {'client':'wheel','fun':'key.accept','match':salt_key_id}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        req = urllib2.Request(self.salt_url, obj, headers)
        opener = urllib2.urlopen(req)
        content = json.loads(opener.read())
        return content['return'][0]['data']['success']
    def KeyDelete(self,salt_key_id):
        headers = {'X-Auth-Token': self.salt_token_id}
        params = {'client':'wheel','fun':'key.delete','match':salt_key_id}
        encode = urllib.urlencode(params)
        obj = urllib.unquote(encode)
        req = urllib2.Request(self.salt_url, obj, headers)
        opener = urllib2.urlopen(req,timeout=3)
        content = json.loads(opener.read())
        return content['return'][0]['data']['success']
    ##########################################################################
    def Salt_CMD(self,tgt,fun,arg=None,client='local',expr_form='glob'):
        if arg:
            params = {'client':client,'fun':fun,'tgt':tgt,'arg':arg,'expr_form':expr_form}
        else:
            params = {'client':client,'fun':fun,'tgt':tgt,'expr_form':expr_form}
        obj = urllib.urlencode(params)
        res = self.PostRequest(obj)
        return res
    def Salt_Minions(self,minion='None'):
        if minion != 'None':
            url = '/minions/'+minion
        else:
            url = '/minions'
        res = self.PostRequest(None,url)
        return res