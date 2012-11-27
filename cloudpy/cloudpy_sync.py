#!/usr/bin/env python

from sys import argv
import argparse
from cloudpy_config import Config
import sh


sync_prog = sh.rsync.bake("-r")
config = Config()

def sync(package):
    desc = "%s:%s" % (config.host, config.depository)
    sync_prog(package, desc)
