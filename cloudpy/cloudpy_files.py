import os
import sys
import uuid
import shutil
import subprocess

class DirTree(object):
    def __init__(self, paths=[]):
        self.children = {}
        self.cplen = None
        self.pwd = os.path.abspath(os.getcwd()).split(os.sep)
        for path in paths:
            self.add_path(path.split(os.sep))

    def add_path(self, path):
        self.cplen = None
        child = path[0]
        if child not in self.children:
            if len(path) == 1:
                self.children[child] = None
                return
            else:
                self.children[child] = DirTree()
        self.children[child].add_path(path[1:])

    def get_cplen(self):
        if self.cplen:
            return self.cplen
        common_prefix = []
        if not self.pwd:
            return 0
        while True:
            if self.pwd and len(self.children) == 1 and self.children.keys()[0] == self.pwd[0]:
                self.children = self.children.values()[0].children
                common_prefix.append(self.pwd[0])
                self.pwd = self.pwd[1:]
            else:
                self.cplen = len(os.path.abspath(os.sep.join(common_prefix)))
                self.cplen = self.cplen + 1
                return self.cplen


class Files(object):
    def __init__(self, files):
        self.files = files
        self.pwd = os.getcwd()
        self.dt = DirTree([f.split(os.sep) for f in files], self.pwd)
        self.base = uuid.uuid1().hex

    def build_targz(self):
        self.build()
        subprocess.call(["tar", "-czf", "%s.tar.gz" % self.base, self.base])
        shutil.rmtree(self.base)
        return os.path.abspath("%s.tar.gz" % self.base)



if __name__ == '__main__':
    fs = ['/Users/zzm/Desktop/Piranha/Piranha/project.py', '/Users/zzm/Desktop/Piranha/Piranha/queue.py', '/Users/zzm/Desktop/Piranha/Piranha/structs.py', '/Users/zzm/Desktop/Husky/Husky/__init__.py', '/Users/zzm/Desktop/Husky/Husky/wrap.py', '/Users/zzm/Desktop/Husky/Husky/iterable_husky.py', '/Users/zzm/Desktop/Husky/Husky/dict_husky.py', '/Users/zzm/Desktop/Husky/Husky/function_husky.py', '/Users/zzm/Desktop/Husky/Husky/module_husky.py', '/Users/zzm/Desktop/Husky/Husky/type_husky.py', '/Users/zzm/Desktop/Thinkpol/Thinkpol/__init__.py', '/Users/zzm/Desktop/Thinkpol/Thinkpol/telescreen.py', '/Users/zzm/Desktop/Thinkpol/Thinkpol/miniture.py', '/Users/zzm/Desktop/Thinkpol/Thinkpol/port.py', '/Users/zzm/Desktop/Piranha/Piranha/supervisor.py', '/Users/zzm/Desktop/Thinkpol/Thinkpol/agent.py', '/Users/zzm/Desktop/Piranha/config.py', '/Users/zzm/Desktop/Piranha/Piranha/task.py']
    files = Files(fs, fs[0])
    files.build_targz()
    print files.get_execfile_path()
    print files.get_pwd()