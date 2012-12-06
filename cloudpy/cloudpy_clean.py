#!/usr/bin/env python

import shutil
from sys import argv

def clean(tmp_dir):
    shutil.rmtree(tmp_dir)