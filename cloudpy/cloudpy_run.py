#!/usr/bin/env python

import sh
from cloudpy_config import Config
import sys
import argparse
from sys import argv


config = Config()
eval_prog = "cloudpy_eval.py"
ENDLINE = "Connection to %s closed." % config.host.split("@")[1]

def print_line(line):
    if line.strip() == ENDLINE:
        return
    sys.stdout.write(line)

def run(package, noisy, clean):
    eval_cmd = config.host_sep.join([config.host_bin, eval_prog])
    target = config.host_sep.join([config.depository, package])

    if not noisy:
        eval_cmd += " -q"
    if clean:
        eval_cmd += " -c"

    sh.ssh("-t", config.host, "python", eval_cmd, target, _out=print_line, _tty_in=True).wait()
