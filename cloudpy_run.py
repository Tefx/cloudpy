#!/usr/bin/env python

import sh
from cloudpy_config import Config
import sys
import argparse
from sys import argv


config = Config()
eval_prog = "cloudpy_eval.py"

parser = argparse.ArgumentParser(description='Run cloudpy package remotely.')
parser.add_argument("-H", "--host", action='store')
parser.add_argument("package", help="Cloudpy package name")
args = parser.parse_args(argv[1:])

if args.host:
    host = args.host
else:
    host = config.host

eval_cmd = config.host_sep.join([config.host_bin, eval_prog])
target = config.host_sep.join([config.depository, args.package])

def print_line(line):
    sys.stdout.write(line)
    sys.stdout.flush()

sh.ssh("-t", host, "python", eval_cmd, target, _out=print_line, _tty_in=True).wait()



