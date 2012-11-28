#!/usr/bin/env python

from setuptools import setup

setup(name='cloudpy',
      version='0.1.2',
      description='Run Python Scripts in virtual environment on an remote host',
      author='Zhu Zhaomeng',
      author_email='zhaomeng.zhu@gmail.com',
      packages=['cloudpy'],
      install_requires=["sh>=1.07"],
      url="https://github.com/Tefx/cloudpy",
      entry_points=dict(console_scripts=[
                          'cloudpy=cloudpy.cloudpy_main:main',
                          'cloudpy-eval=cloudpy.cloudpy_main:eval']),
      classifiers=[
          "Development Status :: 3 - Alpha",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
          "Topic :: Utilities",
      ]
     )