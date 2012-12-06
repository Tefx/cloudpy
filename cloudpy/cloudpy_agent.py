from cloudpy_struct import DirStruct
import sh
import os
import sys
import pkg_resources


class Agent(object):
    def __init__(self, path):
        self.dir = DirStruct(path)
        self.read_conf()

    def read_mods(self):
        self.mods = []
        with open(self.dir.MODS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    items = line.split()
                    if len(items) == 1:
                        require_str = items[0]
                    else:
                        require_str = "==".join(items)
                    working_set = pkg_resources.WorkingSet()
                    require = pkg_resources.Requirement.parse(require_str)
                    try:
                        if not working_set.find(require):
                            self.mods.append(require_str)
                    except Exception:
                        self.mods.append(require_str)
        working_dir = os.path.sep.join(self.conf["PWD"].split())
        self.working_dir = self.dir.append("SRC_DIR", working_dir)
        mainfile = os.path.sep.join(self.conf["EXEC"].split())
        self.mainfile = self.dir.append("SRC_DIR", mainfile)

    def read_conf(self):
        self.conf = {}
        with open(self.dir.CONF_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    attr, value = line.split("=")
                    self.conf[attr.strip()] = value.strip()


    def setup_env(self, quiet=False):
        if quiet:
            outproc = lambda x:None
        else:
            outproc = self.print_output
        env_dir = self.dir.ENV_DIR
        if not os.path.exists(env_dir):
            sh.virtualenv("--system-site-packages", env_dir, _out=outproc).wait()
        activate_this = self.dir.append("ENV_DIR",'bin/activate_this.py')
        execfile(activate_this, dict(__file__=activate_this))
        self.read_mods()
        if self.mods:
            sh.pip.install(self.mods, _out=outproc).wait()

    def print_output(self, line):
        sys.stdout.write(line)

    def run(self, clean):
        sh.cd(self.working_dir)
        try:
            sh.python(self.mainfile, _out=self.print_output, _err=self.print_output).wait()
        except Exception:
            pass
        if clean:
            self.clean()

    def clean(self):
        sh.rm("-rf", self.dir.TOP)