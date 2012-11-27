import uuid
import os

class DirStruct(object):
    struct = {
        "SRC_DIR":"src",
        "CONF_DIR":"conf",
        "MODS_FILE":"mods",
        # "FILES_FILE":"files",
        "CONF_FILE":"conf",
        "ENV_DIR":"env"
    }

    def __init__(self, top):
        self.TOP = os.path.abspath(top)
        self.make_dir()


    def make_dir(self):
        self.SRC_DIR = self.join(self.struct["SRC_DIR"])
        self.CONF_DIR = self.join(self.struct["CONF_DIR"])
        self.MODS_FILE = self.join(self.struct["CONF_DIR"], self.struct["MODS_FILE"])
        # self.FILES_FILE = self.join(self.struct["CONF_DIR"], self.struct["FILES_FILE"])
        self.CONF_FILE = self.join(self.struct["CONF_DIR"], self.struct["CONF_FILE"])
        self.ENV_DIR = self.join(self.struct["ENV_DIR"])

    def join(self, *l):
        return os.sep.join([self.TOP]+list(l))

    def append(self, name, path):
        return os.sep.join([getattr(self, name), path])



if __name__ == '__main__':
    print DirStruct().SRC_DIR
    print DirStruct().append("SRC_DIR", "aaa")