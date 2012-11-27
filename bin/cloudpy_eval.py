#!/usr/bin/env python
import sys
sys.path.append("../")
from cloudpy import Agent
from sys import argv
import argparse

parser = argparse.ArgumentParser(description='run python script in a virtual environment.')
parser.add_argument("package", help="Package Top Dir Location")
parser.add_argument("-q", "--quiet", action='store_true')
parser.add_argument("-c", "--clean", action='store_true')
args = parser.parse_args(argv[1:])

agent = Agent(args.package)
agent.setup_env(args.quiet)
if not args.quiet:
    print "\n\nOutput:\n"
agent.run(args.clean)
