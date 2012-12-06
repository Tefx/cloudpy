#!/usr/bin/env python

from sys import argv
import argparse
import subprocess
import sys

sync_prog = "rsync"
sync_prog_args = "-rlz"

def sync(package, config):
    desc = "%s:%s" % (config.host, config.depository)
    return subprocess.call([sync_prog, sync_prog_args, package, desc], stdout=sys.stdout, stderr=sys.stderr)