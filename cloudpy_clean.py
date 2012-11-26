#!/usr/bin/env python

import sh
from sys import argv

sh.rm("-rf", argv[1])