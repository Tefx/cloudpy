#!/usr/bin/env python

from setuptools import setup
import platform


requires = ["argparse>=1.2.1"]
console_scripts=['cloudpy=cloudpy.cloudpy_main:main']

if platform.system() != "Windows":
      requires.append("sh>=1.07")
      console_scripts.append('cloudpy-eval=cloudpy.cloudpy_main:eval')

setup(name='cloudpy',
      version='0.3.12',
      description='Run Python Scripts in virtual environment on an remote host',
      author='Zhu Zhaomeng',
      author_email='zhaomeng.zhu@gmail.com',
      packages=['cloudpy'],
      install_requires=requires,
      url="https://github.com/Tefx/cloudpy",
      entry_points=dict(console_scripts=console_scripts),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Topic :: Utilities",
      ]
      )