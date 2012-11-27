#!/usr/bin/env python

import sh
from sys import argv

def clean(tmp_dir):
    sh.rm("-rf", tmp_dir)