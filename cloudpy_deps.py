import ast
import os
import sys
from distutils import sysconfig
import pkg_resources
import xmlrpclib
import sh
from cloudpy_files import DirTree


PIP_URL = "http://pypi.python.org/pypi"

class DepsFinder(object):
    def __init__(self, filename, guess_mods=True, guess_files=False):
        self.mainfile = os.path.abspath(filename)
        self.needed_files = [self.mainfile]
        self.mods = {}
        self.unknown_mods = []
        self.guessed_mods = {}
        self.suggested_mods = {}
        self.std_path = sysconfig.get_python_lib(standard_lib=True)
        self.third_path = sysconfig.get_python_lib(standard_lib=False)
        self.guess_mods = guess_mods
        self.guess_files = guess_files
        if guess_mods:
            self.xmlclient = xmlrpclib.ServerProxy(PIP_URL)
            self.installed_mods = self.list_installed()
        self.cal_deps(self.mainfile)

    def cal_deps(self, filename):
        if self.guess_files:
            self.guess_used_files(filename)
        for m in self.parse_imports(filename):
            from_path = getattr(m, "__file__", "")
            if from_path.startswith(self.third_path):
                if m.__name__ not in self.mods:
                    try:
                        v = pkg_resources.get_distribution(m.__name__).version
                        self.mods[m.__name__] = v
                    except pkg_resources.DistributionNotFound:
                        pass
                        self.guess_mod(m.__name__)
            elif not from_path.startswith(self.std_path):
                if from_path:
                    f = self.pyc2py(from_path)
                    if f not in self.needed_files:
                        self.needed_files.append(f)
                        self.cal_deps(f)
        self.cplen =  DirTree(self.needed_files).get_cplen()

    def parse_imports(self, filename):
        f_dir = os.path.split(filename)[0]
        sys.path.append(f_dir)
        mods = []
        with open(filename, "r") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                mods.append(__import__(node.module))
            elif isinstance(node, ast.Import):
                for name in node.names:
                    mods.append(__import__(name.name))
        del sys.path[-1]
        return mods


    def pyc2py(self, filename):
        path = os.path.abspath(filename)
        path = os.path.splitext(path)[0]+".py"
        if os.path.exists(path):
            return path

    def list_installed(self):
        output = sh.pip.freeze().split()
        return {k:v for k,v in [line.strip().split("==") for line in output]}

    def guess_mod(self, name):
        if self.guess_mods:
            result = self.xmlclient.search({"summary":name})
            result.extend(self.xmlclient.search({"name":name}))
            result = {x["name"]:self.installed_mods[x["name"]] \
                        for x in result if x["name"] in self.installed_mods}
        else:
            result = []
        if len(result) == 0:
            if name not in self.unknown_mods:
                self.unknown_mods.append(name)
        elif len(result) == 1:
            self.guessed_mods.update(result)
        else:
            self.suggested_mods[name] = result

    def write2file_mods(self, mods_file):
        with open(mods_file, "w") as f:
            for k,v in self.mods.iteritems():
                f.write("%s\t%s\n" % (k, v))
            if self.guess_mods:
                if len(self.guessed_mods):
                    f.write("\n\n#### These modules are guessed, modify them if needed.\n")
                for k,v in self.guessed_mods.iteritems():
                    f.write("%s\t%s\n" % (k,v))
                if len(self.suggested_mods):
                    f.write("\n\n#### These modules can't be guessed out, but we have some suggestions. \n")
                for k,v in self.suggested_mods.iteritems():
                    f.write('## For modules named "%s":\n' % k)
                    for k0, v0 in v.iteritems():
                        f.write('# %s\t%s\n' % (k0, v0))
            if len(self.unknown_mods):
                f.write("\n\n#### These modules can't be handled automatically!\n")
            for item in self.unknown_mods:
                f.write("# %s\n" % item)

    def find_var(self, tree, name):
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for n in node.targets:
                    if n.id == name:
                        try:
                            return ast.literal_eval(node.value)
                        except:
                            pass

    def guess_used_files(self, filename):
        with open(filename, "r") as f:
            tree = ast.parse(f.read())
        for node in ast.walk(tree):
            path = None
            if isinstance(node, ast.Call):
                if not hasattr(node.func, "id"):
                    continue
                if node.func.id == "apply" and node.args[0].id == "open":
                    path = node.args[1].elts[0].s
                elif node.func.id == "open":
                    if isinstance(node.args[0], ast.Str):
                        path = node.args[0].s
                    elif isinstance(node.args[0], ast.Name):
                        path = self.find_var(tree, node.args[0].id)
            if not path:
                continue
            path = os.path.abspath(path)
            if path not in self.needed_files:
                self.needed_files.append(path)


if __name__ == '__main__':
    tf = "../Piranha/Piranha/project.py"
    # tf = "../Corellia/Corellia/worker.py"
    mf = DepsFinder(tf, False)
    # mf.guess_mod("name")
    # mf.guess_mod("json")
    # print mf.mods
    # print mf.unknown_mods
    # print mf.guessed_mods
    # print mf.suggested_mods
    # print mf.needed_files
    mf.write2file_mods("mods")
    mf.write2file_files("files")
    mf.append_config("conf")


