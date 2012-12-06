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