from cloudpy_struct import DirStruct
import sh
import os
import sys


class Agent(object):
    def __init__(self, path):
        self.dir = DirStruct(path)
        self.mods = []
        self.conf = {}
        self.read_mods()
        self.read_conf()
        self.working_dir = self.dir.append("SRC_DIR", self.conf["PWD"])
        self.mainfile = self.dir.append("SRC_DIR", self.conf["EXEC"])

    def read_mods(self):
        with open(self.dir.MODS_FILE, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    items = line.split()
                    if len(items) == 1:
                        self.mods.append(items[0])
                    else:
                        self.mods.append("==".join(items))

    def read_conf(self):
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
        if self.mods:
            sh.pip.install(self.mods, _out=outproc).wait()

    def print_output(self, line):
        sys.stdout.write(line)

    def run(self, clean):
        sh.cd(self.working_dir)
        sh.python(self.mainfile, _out=self.print_output).wait()
        if clean:
            self.clean()

    def clean(self):
        sh.rm("-rf", self.dir.TOP)