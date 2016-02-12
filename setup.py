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
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

PLATFORM = sys.platform
if PLATFORM == 'win32':
    SRC_DIR = 'win32'
elif PLATFORM == 'darwin':
    SRC_DIR = 'darwin'
elif PLATFORM == 'linux2':
    SRC_DIR = 'linux'
else:
    sys.exit('unknown platform - expected "win32", "darwin" or "linux2"')

PKG_DATA = [os.path.join(SRC_DIR, '*.*'), os.path.join(SRC_DIR, 'src', '*.*')]
LIB_DIR = os.path.join(NAME, SRC_DIR)
SRC_DIR = os.path.join(LIB_DIR, 'src')
logger.debug(PKG_DATA)
TESTS = '%s.tests' % NAME
TEST_DATA = ['test_spectrl2_data.json']
SOLPOS = 'solpos.c'
SOLPOSAM = 'solposAM.c'
SOLPOSAM_LIB = 'solposAM'
SPECTRL2 = 'spectrl2.c'
SPECTRL2_2 = 'spectrl2_2.c'
SPECTRL2_LIB = 'spectrl2'
SOLPOS = os.path.join(SRC_DIR, SOLPOS)
SOLPOSAM = os.path.join(SRC_DIR, SOLPOSAM)
SPECTRL2 = os.path.join(SRC_DIR, SPECTRL2)
SPECTRL2_2 = os.path.join(SRC_DIR, SPECTRL2_2)
LIB_FILES = ['%s.dll', '%s.lib', '%s.exp', 'lib%s.so', 'lib%s.dylib', 'lib%s.a']
if 'clean' in sys.argv or 'distclean' in sys.argv:
    for lib_file in LIB_FILES:
        try:
            os.remove(os.path.join(LIB_DIR, lib_file % SOLPOSAM_LIB))
        except OSError as err:
            sys.stderr.write(err.message)
        try:
            os.remove(os.path.join(LIB_DIR, lib_file % SPECTRL2_LIB))
        except OSError as err:
            sys.stderr.write(err.message)
else:
    # compile NREL source code
    CC = distutils.ccompiler.new_compiler()  # initialize compiler object
    CC.set_include_dirs([SRC_DIR])  # set includes directory
    OBJS = CC.compile([SOLPOS, SOLPOSAM])  # compile solpos and solposAM objects
    # link objects and make shared library in library directory
    CC.link_shared_lib(OBJS, SOLPOSAM_LIB, output_dir=LIB_DIR)
    OBJS = CC.compile([SPECTRL2, SPECTRL2_2, SOLPOS])  # compile spectrl2 objects
    CC.set_libraries([SOLPOSAM_LIB])  # set linked libraries
    CC.set_library_dirs([LIB_DIR])  # set library directories
    # link objects and make shared library in library directory
    CC.link_shared_lib(OBJS, SPECTRL2_LIB, output_dir=LIB_DIR)

setup(name=NAME,
      version=VERSION,
      packages=[NAME, TESTS],
      package_data={NAME: PKG_DATA, TESTS: TEST_DATA},
      description='Python wrapper around NREL SOLPOS and SPECTRL2')
