import httplib
import json
import time

class GitAPI:
    def __init__(self, host, port, token,url=""):
        self.host = host
        self.port = port
        self.token = token
        if url:
            self.url = url
        else:
            self.url = "/api/v3"
    def GET(self, url):
        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('GET', url, '', {'PRIVATE-TOKEN': self.token})
        res = conn.getresponse()
        status = res.status
        content = res.read()
        conn.close()
        return status, content
    def PUT(self,url):
        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('PUT', url, '', {'PRIVATE-TOKEN': self.token})
        res = conn.getresponse()
        status = res.status
        content = res.read()
        conn.close()
        return status, content
    def DELETE(self,url):
        conn = httplib.HTTPConnection(self.host, self.port)
        conn.request('DELETE', url, '', {'PRIVATE-TOKEN': self.token})
        res = conn.getresponse()
        status = res.status
        content = res.read()
        conn.close()
        return status,content
    def files(self, file_name):
        url = '/api/v3/projects/2/repository/files?ref=master&file_path={0}' .format(file_name)
        status, content = self.GET(url)
        if status == 200:
            return content
        else:
            print status
    def tree(self, projectsid, ref, path=''):
        if path:
            url = '/api/v3/projects/{0}/repository/tree?path={1}&ref_name={2}' .format(projectsid, path,ref)
        else:
            url = '/api/v3/projects/{0}/repository/tree?ref_name={1}' .format(projectsid,ref)
        status,content = self.GET(url)
        if status == 200:
            return content
        else:
            print status
    def commits(self, projectsid, commitsid=''):
        if commitsid:
            url = '{0}/projects/{1}/repository/commits/{2}' .format(self.url,projectsid,commitsid)
        else:
            url = '{0}/projects/{1}/repository/commits' .format(self.url,projectsid)
        status,content = self.GET(url)
        if status == 200:
            return content
        else:
            print status
    def get_tree(self,projectsid,ref='master',path=''):
        content = self.tree(projectsid,ref,path)
        content = json.loads(content)
        if not path:
            folder = [{'icon':'/static/images/folder.png','children':True,'text':i['name'],'id':i['name']+'::'} for i in content if i['type']=='tree']
            files = [{'icon':'glyphicon glyphicon-file','text':i['name'],'id':i['name']+'::'+i['id'][:10],'type':'file'} for i in content if i['type']=='blob']
        else:
            folder = [{'icon':'/static/images/folder.png','children':True,'text':i['name'],'id':path+'/'+i['name']+'::'} for i in content if i['type']=='tree']
            files = [{'icon':'glyphicon glyphicon-file','text':i['name'],'id':path+'/'+i['name']+'::'+i['id'][:10],'type':'file'} for i in content if i['type']=='blob']
        return folder+files
    def raw_blobs(self,projectsid,fileid):
        url = '{0}/projects/{1}/repository/raw_blobs/{2}' .format(self.url,projectsid,fileid)
        status,content = self.GET(url)
        if status == 200:
            return content
        else:
            print status
    def del_file(self,projectid,file_path,branch_name,message):
        if projectid and file_path and branch_name and message:
            url = self.url + '/projects/{0}/repository/files?file_path={1}&branch_name={2}&commit_message={3}' .format(projectid,file_path,branch_name,message)
            status,content = self.DELETE(url)
            return status,content
        else:
            print 'error'