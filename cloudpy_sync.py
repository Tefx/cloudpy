#!/usr/bin/env python

from sys import argv
import argparse
from cloudpy_config import Config
import sh
sync_prog = sh.rsync.bake("-r")

config = Config()

parser = argparse.ArgumentParser(description='Transfer a cloudpy package to remote host.')
parser.add_argument("package", help="Package Top Dir Location")
parser.add_argument("-r", "--remote", action='store')
args = parser.parse_args(argv[1:])

if args.remote:
    desc = args.desc
else:
    desc = "%s:%s" % (config.host, config.depository)

sync_prog(args.package, desc)