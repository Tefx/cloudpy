#!/usr/bin/env python

import sh
import sys
import argparse
from sys import argv

def run(package, noisy, clean, config):
    ENDLINE = "Connection to %s closed." % config.host.split("@")[1]
    target = config.host_sep.join([config.depository, package])
    eval_prog = "cloudpy-eval"

    if not noisy:
        eval_prog += " -q"
    if clean:
        eval_prog += " -c"

    def print_line(line):
        if line.strip() == ENDLINE:
            return
        sys.stdout.write(line)

    try:
        sh.ssh("-t", config.host, eval_prog, target, _out=print_line, _err=print_line, _tty_in=True).wait()
    except Exception:
        pass