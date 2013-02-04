import pkg_resources
from distutils import sysconfig
import sys
import os
import ast
import types


BuiltinType = 0
StandardType = 1
SiteType = 2
UserDefineType = 3

PYPI_SERVER = "http://pypi.python.org/pypi"

PATH_STD = [
            sysconfig.get_python_lib(standard_lib=True, prefix=os.path.realpath(sys.prefix)),
            sysconfig.get_python_lib(standard_lib=True)
           ]
PATH_SITE = [
                sysconfig.get_python_lib(standard_lib=False),
            ]
BUILTIN_NAMES = sys.builtin_module_names


class Distribution(object):
    def __init__(self, name_or_file, is_file=False):
        if is_file:
            self.path = os.path.abspath(name_or_file)
            self._dir, name = os.path.split(name_or_file)
            self.imported_name, self._ext = os.path.splitext(name)
        else:
            self.imported_name = name_or_file

    def parse_deps(self, filename):
        deps = []
        sys.path.append(self._dir)
        with open(filename, "r") as f:
            ast_tree = ast.parse(f.read())
        for node in ast_tree.body:
            if isinstance(node, ast.ImportFrom):
                deps.append(Distribution(node.module))
            elif isinstance(node, ast.Import):
                for name in node.names:
                    deps.append(Distribution(name.name))
        del sys.path[-1]
        return deps

    def __getattr__(self, name):
        get_func = "get_%s" % name
        self.__dict__[name] = self.__class__.__dict__.get(get_func, lambda x:None)(self)
        return self.__dict__[name]

    def get_path(self):
        if self._module:
            return self._module.__file__
        else:
            pass
            # for p in sys.path:
            #     name = self.imported_name.replace(".", os.path.sep)
            #     path = os.path.join(p, name)
            #     if os.path.exists(path):
            #         return path

    def get_type(self):
        if not self.path:
            return SiteType
        elif any(map(self.path.startswith, PATH_STD)):
            return StandardType
        elif any(map(self.path.startswith, PATH_SITE)):
            return SiteType
        else:
            return UserDefineType

    def get__module(self):
        try:
            return __import__(self.imported_name, {}, {})
        except ImportError:
            return None

    def get_deps(self):
        if self.type != UserDefineType:
            return None
        if not self.path:
            return None
        if "." not in self.imported_name:
            return self.parse_deps(self.path)
        elif "." in self.imported_name:
            pass

    def get_version(self):
        if self.type != SiteType:
            return None
        if self._module:
            pass
        else:
            pass

    def __repr__(self):
        return self.imported_name


if __name__ == '__main__':
    tf = "../../Piranha/Piranha/project.py"
    dist = Distribution(tf, True)
    print dist.imported_name
    print dist.file
    print dist.type
    print dist.deps


