# coding: utf-8
import os
import git
# git modules neeed install Gitpython you can 'pip install Gitpython'

class GitAPIError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class GitAPI:
    def __init__(self, repo_path):
        # noinspection PySingleQuotedDocstring
        '''
                    根据给定的git仓库路径初始化仓库信息。
                :param repo_path:
                :return:
                '''
        self.repo_path = repo_path
        if os.path.exists(self.repo_path):
            try:
                self.repo = git.Repo(self.repo_path)
            except git.exc.InvalidGitRepositoryError:
                self.repo = git.Repo.init(self.repo_path)
        else:
            self.repo = git.Repo.init(self.repo_path)
        if self.repo.heads:
            pass
        else:
            if os.path.exists(os.path.join(self.repo_path, 'README.TXT')):
                pass
            else:
                with open(os.path.join(self.repo_path, 'README.TXT'), 'w') as f:
                    f.close()
            index = self.repo.index
            index.add(['README.TXT'])
            index.commit('Create Readme File')

    def branch(self, branch_name=None,):
        _heads = self.repo.heads
        branch_list = []
        if _heads:
            for i in _heads:
                branch_list.append(i.name)

        if branch_name:
            if branch_name in branch_list:
                raise GitAPIError("A branch named '{0}' already exists." .format(branch_name))
            else:
                try:
                    self.repo.create_head(branch_name)
                except Exception as e:
                    raise GitAPIError(e)
        branch_list.remove(self.repo.head.ref.name)
        branch_list.insert(0, "*{0}" .format(self.repo.head.ref.name))
        return branch_list

    def switch_branch(self, name):
        # noinspection PySingleQuotedDocstring
        '''
                input branch name switch to branch of name
                :param name: master
                :return: Not return
                '''
        try:
            for i in self.repo.refs:
                if i.name == name:
                    git.refs.head.Head(self.repo, 'refs/heads/%s' %(name)).checkout(force=True)
        except Exception as e:
            raise GitAPIError(e)

    def tags(self, name=None, message=None):
        tags_list = []
        for i in self.repo.tags:
            tags_list.append(i.name)

        if name:
            if name in tags_list:
                raise GitAPIError("A tag named '{0}' already exists." .format(name))
            else:
                try:
                    self.repo.create_tag(name, message=message)
                    tags_list.append(name)
                except Exception as e:
                    raise GitAPIError(e)
        return tags_list

    def commit(self, path, message=None):
        abs_path = os.path.join(self.repo.working_dir, path)
        if os.path.exists(abs_path):
            index = self.repo.index
            index.add([path])
            if message:
                index.commit(message)
            else:
                index.commit('Create New File')
        else:
            raise OSError('File Not Exists of %s' %(abs_path))
    def remove(self,path,message):
        index = self.repo.index
        index.remove([path])
        if message:
            index.commit(message)