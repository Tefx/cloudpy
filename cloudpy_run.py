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
parser.add_argument("-n", "--noisy", action='store_true')
parser.add_argument("-c", "--clean", action='store_true')
args = parser.parse_args(argv[1:])

if args.host:
    host = args.host
else:
    host = config.host

eval_cmd = config.host_sep.join([config.host_bin, eval_prog])
target = config.host_sep.join([config.depository, args.package])

if not args.noisy:
    eval_cmd += " -q"
if args.clean:
    eval_cmd += " -c"

ENDLINE = "Connection to %s closed." % host.split("@")[1]

def print_line(line):
    if line.strip() == ENDLINE:
        return
    sys.stdout.write(line)

sh.ssh("-t", host, "python", eval_cmd, target, _out=print_line, _tty_in=True).wait()



