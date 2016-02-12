# Copyright (c) 2014 SunPower Corp.
# Mark Mikofski
# 2016-02-10

import sys
import os
try:
    from setuptools import setup, distutils
except ImportError:
    sys.exit('setuptools was not detected - please install setuptools and pip')
from solar_utils import __version__ as VERSION, __name__ as NAME

PLATFORM = sys.platform
if PLATFORM == 'win32':
    SRCDIR = 'win32'
elif PLATFORM == 'darwin':
    SRCDIR = 'darwin'
elif PLATFORM == 'linux2':
    SRCDIR = 'linux'
else:
    sys.exit('unknown platform - expected "win32", "darwin" or "linux2"')

CC = distutils.ccompiler.new_compiler()
CC.set_include_dirs('path\\to\\srcdir')
CC.compile(['win32\\solposAM.c','win32\\solpos.c'])
CC.link_shared_lib(['win32\\solposAM.obj','win32\\solpos.obj'], 'solposAM')

setup(name = NAME,
      version = VERSION,
      packages = [NAME],
      package_data = {NAME: PKG_DATA},
      description = 'Python wrapper around NREL SOLPOS and SPECTRL2')
