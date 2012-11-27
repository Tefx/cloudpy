#!/usr/bin/env python

from sys import argv
import argparse
import sh


sync_prog = sh.rsync.bake("-r")

def sync(package, config):
    desc = "%s:%s" % (config.host, config.depository)
    sync_prog(package, desc)
