import ast
import os
import sys
import distutils
import pkg_resources
import xmlrpclib
import sh
import types
from cloudpy_files import DirTree
import traceback


PIP_URL = "http://pypi.python.org/pypi"

class DepsFinder(object):
    def __init__(self, filename, guess_files=False):
        self.mainfile = os.path.abspath(filename)
        self.needed_files = [self.mainfile]
        self.mods = {}
        self.unknown_mods = []
        self.guessed_mods = {}
        self.suggested_mods = {}
        self.std_path = distutils.sysconfig.get_python_lib(standard_lib=True, prefix=os.path.realpath(sys.prefix))
        self.std_path2 = distutils.sysconfig.get_python_lib(standard_lib=True)
        self.third_path = distutils.sysconfig.get_python_lib(standard_lib=False)
        self.guess_files = guess_files
        self.cal_deps(self.mainfile)

    def cal_deps(self, filename):
        if self.guess_files:
            self.guess_used_files(filename)
        for m, fs in self.parse_imports(filename).iteritems():
            if fs:
                for f in fs:
                    if f.startswith(self.third_path):
                        if not self.in_mods(m):
                            try:
                                v = pkg_resources.get_distribution(m).version
                                self.mods[m] = v
                            except pkg_resources.DistributionNotFound:
                                self.guess_mod(m.__name__, True)
                    elif not (f.startswith(self.std_path) or f.startswith(self.std_path2)):
                        f = self.pyc2py(f)
                        if f not in self.needed_files:
                            self.needed_files.append(f)
                            self.cal_deps(f)
            else:
                if not self.in_mods(m):
                    self.guess_mod(m, False)
        self.cplen =  DirTree(self.needed_files).get_cplen()

    def in_mods(self, name):
        return name in self.mods or name in self.unknown_mods or name in self.guessed_mods or name in self.suggested_mods


    def search_mod(self, name, prefix):
        res = []
        if not name:
            return res
        p = os.path.join(prefix, name[0])
        if os.path.isdir(p):
            init_file = os.path.join(p, "__init__.py")
            if os.path.exists(init_file):
                res.append(init_file)
            res.extend(self.search_mod(name[1:], p))
        if os.path.exists("%s.py" % p):
            res.append("%s.py" % p)
        return res

    def try_import(self, name):
        try:
            m = __import__(name, {}, {})
            return [m.__file__]
        except ImportError:
            return []

    def parse_imports(self, filename):
        f_dir = os.path.split(filename)[0]
        sys.path.append(f_dir)
        mods = {}
        with open(filename, "r") as f:
            tree = ast.parse(f.read())
        for node in tree.body:
            if isinstance(node, ast.ImportFrom):
                if node.module in sys.builtin_module_names:
                    continue
                mods[node.module] = self.try_import(node.module)
                if not mods[node.module]:
                    for p in sys.path:
                        res = self.search_mod(node.module.split("."), p)
                        if res:
                            break
                    mods[node.module] = res
            elif isinstance(node, ast.Import):
                for name in node.names:
                    if name.name in sys.builtin_module_names:
                        continue
                    mods[name.name] = self.try_import(name.name)
                    if not mods[name.name]:
                        for p in sys.path:
                            res = self.search_mod(name.name.split("."), p)
                            if res:
                                break
                        mods[name.name] = res
        del sys.path[-1]
        return mods


    def pyc2py(self, filename):
        path = os.path.abspath(filename)
        path = os.path.splitext(path)[0]+".py"
        if os.path.exists(path):
            return path

    def list_installed(self):
        output = sh.pip.freeze()
        return {k:v for k,v in [line.strip().split("==") for line in output.split() if "==" in line]}

    def search_pypi(self, name):
        if not hasattr(self, "xmlclient"):
            self.xmlclient = xmlrpclib.ServerProxy(PIP_URL)
        search_result = self.xmlclient.search({"name":name})
        return [x["name"] for x in search_result]

    def guess_mod_installed(self, name):
        if not hasattr(self, "installed_mods"):
            self.installed_mods = self.list_installed()
        search_result = {x:self.installed_mods[x] for x in self.search_pypi(name) if x in self.installed_mods}
        if not search_result:
            if name not in self.unknown_mods:
                self.unknown_mods.append(name)
        elif len(search_result) == 1:
            self.mods.update(search_result)
        elif name in self.installed_mods:
            self.guessed_mods[name] = self.installed_mods[name]
        else:
            self.suggested_mods[name] = search_result

    def guess_mod_not_installed(self, name):
        if not hasattr(self, "installed_mods"):
            self.installed_mods = self.list_installed()
        search_result = {x:None for x in self.search_pypi(name) if x not in self.installed_mods}
        if not search_result:
            if name not in self.unknown_mods:
                self.unknown_mods.append(name)
        elif len(search_result) == 1:
            self.guessed_mods.update(search_result)
        elif name in search_result:
            self.guessed_mods[name] = search_result[name]
        else:
            self.suggested_mods[name] = search_result
        
    def guess_mod(self, name, installed):
        if installed:
            return self.guess_mod_installed(name)
        else:
            return self.guess_mod_not_installed(name)

    def write2file_mods(self, mods_file):
        with open(mods_file, "w") as f:
            for k,v in self.mods.iteritems():
                f.write("%s\t%s\n" % (k, v))
            if len(self.guessed_mods):
                f.write("\n\n#### These modules are guessed, modify them if needed.\n")
            for k,v in self.guessed_mods.iteritems():
                if v:
                    f.write("%s\t%s\n" % (k, v))
                else:
                    f.write("%s\n" % k)
            if len(self.suggested_mods):
                f.write("\n\n#### These modules can't be guessed out, but we have some suggestions. \n")
            for k,v in self.suggested_mods.iteritems():
                f.write('## For modules named "%s":\n' % k)
                for k0, v0 in v.iteritems():
                    if not v0:
                        f.write('# %s\n' % item)
                    else:
                        f.write("# %s\t%s\n" % (k0, v0))
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
    tf = "../../Piranha/Piranha/project.py"
    # tf = "../Corellia/Corellia/worker.py"
    mf = DepsFinder(tf)
    # # mf.guess_mod("name")
    # mf.guess_mod("yajl-py")
    print mf.mods
    print mf.unknown_mods
    print mf.guessed_mods
    print mf.suggested_mods
    # print mf.needed_files
    mf.write2file_mods("test")


