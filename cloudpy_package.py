from cloudpy_deps import DepsFinder
from cloudpy_files import DirTree
from cloudpy_struct import DirStruct
import os
import shutil


class Package(object):
    def __init__(self, mainfile, name=None, guess_mods=True, guess_files=False):
        self.mainfile = mainfile
        self.df = DepsFinder(mainfile, guess_mods, guess_files)
        self.dt = DirTree(self.df.needed_files)
        self.files = []
        self.dir = DirStruct(name)

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

    # def write2file_files(self):
    #     with open(self.dir.FILES_FILE, "w") as f:
    #         for fp in self.files:
    #             f.write("%s\n" % fp)

    def write_config(self):
        with open(self.dir.CONF_FILE, "w") as f:
            pwd = os.getcwd()[self.dt.get_cplen():]
            if not pwd:
                pwd = "./"
            f.write("PWD=%s\n" % pwd)
            exec_path = os.path.abspath(self.mainfile)[self.dt.get_cplen():]
            f.write("EXEC=%s\n" % exec_path)


if __name__ == '__main__':
    from sys import argv
    import argparse

    parser = argparse.ArgumentParser(description='package a python script.')
    parser.add_argument("script", help="Script name to be packed")
    parser.add_argument("-m", "--mods", action='store_true')
    parser.add_argument("-f", "--files", action='store_true')
    parser.add_argument("-n", "--name", action='store')

    args = parser.parse_args(argv[1:])

    p = Package(args.script, args.name, args.mods, args.files)
    p.build()