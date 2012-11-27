#!/usr/bin/env python

import sys
sys.path.append("../")

import sh
from sys import argv
import argparse

from cloudpy import pack
from cloudpy import sync
from cloudpy import run
from cloudpy import clean
from cloudpy import Config


parser = argparse.ArgumentParser(description='package a python script.')
parser.add_argument("script", help="Script or packed package")

parser.add_argument("-m", "--mods", action='store_true')
parser.add_argument("-f", "--files", action='store_true')
parser.add_argument("-n", "--name", action='store')
parser.add_argument("-N", "--noisy", action='store_true')
parser.add_argument("-c", "--clean", action='store_true')

parser.add_argument("-P", "-pack", action="store_true")
parser.add_argument("-S", "-sync", action="store_true")
parser.add_argument("-R", "-run", action="store_true")
parser.add_argument("-C", "-clean", action="store_true")

args = parser.parse_args(argv[1:])

name = args.script
config = Config()

if not (args.P and args.S and args.R and args.C):
    args.P = True
    args.S = True
    args.R = True
    if not args.name:
        args.C = True

if args.P:
    if args.noisy:
        print "Packing...\n*****************\n"
    name = pack(args.script, args.name, args.mods, args.files)

if args.S:
    if args.noisy:
        print "Syncing...\n*****************\n"
    sync(name, config)

if args.R:
    if args.noisy:
        print "Running...\n*****************\n"
    run(name, args.noisy, args.clean, config)

if args.C:
    if args.noisy:
        print "Cleanning...\n*****************\n"
    clean(name)