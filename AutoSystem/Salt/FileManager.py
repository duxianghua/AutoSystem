# coding: utf-8
import base64
import os
import re
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, 'lib'))
import magic
from .GitAPI import *
from time import sleep

class URLBase64:
    def __init__(self):
        pass

    def encode(safe, text):
        e_str = base64.urlsafe_b64encode(text).split('=')[0]
        return e_str

    def decode(safe, code):
        code = code + ((4 - len(code) % 4) * "=")
        d_str = base64.urlsafe_b64decode(str(code))
        return d_str

class LocalFileManager(URLBase64):
    def __init__(self):
        self.path = os.path.join(BASE_DIR,'config')
        self.repo = GitAPI('config')

    def file_type(self,path):
        with magic.Magic(flags=magic.MAGIC_MIME_TYPE) as m:
            return m.id_filename(path)

    def tree(self,pathid='',FilterHide=True):
        l = []
        if pathid:
            path = self.decode(pathid)
        else:
            path = ''
        abspath = os.path.join(self.path, path)
        FileList = os.listdir(abspath)
        if FilterHide:
            FileList = [i for i in FileList if re.match(r'^[^\.]', i)]
        for i in FileList:
            id = self.encode(os.path.join(path,i))
            fullpath = os.path.join(abspath,i)
            if os.path.isdir(fullpath):
                l.append({'text':i, 'id':id, 'type':'folder', 'children':True})
            elif os.path.isfile(fullpath):
                l.append({'text':i, 'id':id, 'type':'file'})
        return l

    def get_content(self, fileid):
        type_list = ['text']
        path = self.decode(fileid)
        abspath = os.path.join(self.path, path)
        if os.path.isfile(abspath):
            _filetype = self.file_type(abspath)
            if _filetype.split('/')[0] in type_list:
                with open(abspath,'r') as f:
                    data = f.read()
                    return 200, data
            elif _filetype == 'inode/x-empty':
                return 200, "This is empty file;"
            else:
                return 200, "这不是一个可编辑的文件,文件类型是'{0}';" .format(_filetype)
        else:
            return 200, "No such file {0}" .format(abspath)


    def create_node(self,fileid,name,type):
        """
        create file or folder
        :param fileid:
        :param name:
        :param type:
        :return:
        """

        path = self.decode(fileid)
        t = os.path.join(self.path, path)
        abspath = os.path.join(t,str(name))
        if os.path.exists(abspath):
            return 400,"File exists '{0}'" .format(name)
        else:
            if type == 'file':
                try:
                    f = open(abspath,'w')
                    f.close()
                    return 200,'success'
                except OSError,e:
                    return 400,e
            elif type == 'folder':
                try:
                    os.mkdir(abspath)
                    return 200,'success'
                except OSError,e:
                    return 400,e
            else:
                return 400,"Type error of '{0}'" .format(type)

    def rename_node(self,fileid,name):
        '''
        rename file or folder.
        :param fileid:
        :param name:
        :return:
        '''
        path = self.decode(fileid)
        srcpath = os.path.join(self.path, path)
        destpath = re.sub(r'[^\/]*$', name,srcpath)
        if os.path.exists(srcpath):
            try:
                os.rename(srcpath,destpath)
                self.repo.commit(destpath)
                return 200, 'success'
            except OSError,e:
                return 400, e
        else:
            return 400, "File Not exists '{0}'" .format(srcpath)

    def delete_node(self,fileid):
        '''
        delete file or folder.
        :param fileid:
        :param type:
        :return:
        '''

        path = self.decode(fileid)
        abspath = os.path.join(self.path, path)
        if os.path.exists(abspath):
            if os.path.isfile(abspath):
                try:
                    os.remove(abspath)
                    self.repo.remove(path,'delete file')
                    return 200, 'success'
                except OSError,e:
                    return 400, e
            elif os.path.isdir(abspath):
                try:
                    os.removedirs(abspath)
                    self.repo.remove(path,'delete dir')
                    return 200, 'success'
                except OSError,e:
                    return 400, e
        else:
            return 400, "File Not exists '{0}'" .format(path)

    def commint(self, fileid, text):
        '''
            write content to file;
        :param text:
        :return:
        '''
        path = self.decode(fileid)
        abspath = os.path.join(self.path, path)
        content = base64.b64decode(text)
        if os.path.exists(abspath):
            with open(abspath,'w') as f:
                f.write(content)
            self.repo.commit(path)
            return 200,'success'
        else:
            return 400,'File not exists'