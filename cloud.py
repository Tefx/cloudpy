#!/usr/bin/env python

import sh
from sys import argv,stdout
import argparse


package_prog = sh.python.bake("./cloudpy_package.py")
sync_prog = sh.python.bake("./cloudpy_sync.py")
run_prog = sh.python.bake("./cloudpy_run.py")
clean_prog = sh.python.bake("./cloudpy_clean.py")

parser = argparse.ArgumentParser(description='package a python script.')
parser.add_argument("script", help="Script name to be packed")
parser.add_argument("-m", "--mods", action='store_true')
parser.add_argument("-f", "--files", action='store_true')
parser.add_argument("-n", "--name", action='store')
parser.add_argument("-N", "--noisy", action='store_true')
parser.add_argument("-c", "--clean", action='store_true')

args = parser.parse_args(argv[1:])

package_args = []
run_args = []

if args.mods:
    package_args.append("-m")
if args.files:
    package_args.append("-f")
if args.name:
    package_args.append("-n")
    package_args.append("test")

if args.noisy:
    run_args.append("-n")
if not args.name or args.clean:
    run_args.append("-c")

def print_line(line):
    stdout.write(line)

name = package_prog([args.script]+package_args).strip()
sync_prog(name)
run_prog(run_args+[name], _out=print_line).wait()
if not args.name:
    clean_prog(name)