#!/usr/bin/env python

import sh
import sys
import argparse
from sys import argv


eval_prog = "cloudpy-eval"

def run(package, noisy, clean, config):
    ENDLINE = "Connection to %s closed." % config.host.split("@")[1]
    target = config.host_sep.join([config.depository, package])

    if not noisy:
        eval_cmd += " -q"
    if clean:
        eval_cmd += " -c"

    def print_line(line):
        if line.strip() == ENDLINE:
            return
        sys.stdout.write(line)

    sh.ssh("-t", config.host, eval_prog, target, _out=print_line, _tty_in=True).wait()