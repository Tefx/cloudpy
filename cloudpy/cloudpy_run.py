#!/usr/bin/env python

import subprocess
import sys

eval_prog = "cloudpy-eval"


def run(package, noisy, clean, config):
    ENDLINE = "Connection to %s closed." % config.host.split("@")[1]
    target = config.host_sep.join([config.depository, package])

    eval_prog_args = []

    if not noisy:
        eval_prog_args.append("-q")
    if clean:
        eval_prog_args.append("-c")

    p = subprocess.Popen(["ssh", "-t", config.host, eval_prog, " ".join(eval_prog_args), target], 1, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    while True:
        line = p.stdout.readline()
        if not line or line == ENDLINE:
            break
        sys.stdout.write(line)