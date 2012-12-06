#!/usr/bin/env python

from cloudpy_deps import DepsFinder
from cloudpy_files import DirTree
from cloudpy_struct import DirStruct
import os
import shutil
import uuid


class Package(object):
    def __init__(self, mainfile, name=None, guess_files=False):
        self.mainfile = mainfile
        self.df = DepsFinder(mainfile, guess_files)
        self.dt = DirTree(self.df.needed_files)
        self.files = []
        if name:
            self.name = name
        else:
            self.name = uuid.uuid1().hex
        self.dir = DirStruct(self.name)

    def build(self):
        for f in self.df.needed_files:
            rp = f[self.dt.get_cplen():]
            target = self.dir.append("SRC_DIR", rp)
            # self.files.append(rp)
            path_dir = os.path.split(target)[0]
            if not os.path.exists(path_dir):
                os.makedirs(path_dir)
            shutil.copy2(f, target)
        target_wd = self.dir.append("SRC_DIR", os.getcwd()[self.dt.get_cplen():])
        if not os.path.exists(target_wd):
            os.makedirs(target_wd)
        if not os.path.exists(self.dir.CONF_DIR):
            os.makedirs(self.dir.CONF_DIR)
        self.df.write2file_mods(self.dir.MODS_FILE)
        # self.write2file_files()
        self.write_config()

    def write_config(self):
        with open(self.dir.CONF_FILE, "w") as f:
            pwd = os.getcwd()[self.dt.get_cplen():]
            if not pwd:
                pwd = "."
            pwd = " ".join(pwd.split(os.path.sep))
            f.write("PWD=%s\n" % pwd)
            exec_path = os.path.abspath(self.mainfile)[self.dt.get_cplen():]
            exec_path = " ".join(exec_path.split(os.path.sep))
            f.write("EXEC=%s\n" % exec_path)

def pack(script, name, files):
    p = Package(script, name, files)
    p.build()
    return p.name