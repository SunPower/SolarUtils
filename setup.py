# Copyright (c) 2014 SunPower Corp.
# Mark Mikofski
# 2016-02-10

import sys
import os
import shutil
try:
    from setuptools import setup, distutils, Extension
except ImportError:
    sys.exit('setuptools was not detected - please install setuptools and pip')
from solar_utils import __version__ as VERSION, __name__ as NAME
from solar_utils.tests import test_cdlls

# set platform constants
CCFLAGS, RPATH, INSTALL_NAME = None, None, None
PLATFORM = sys.platform
if PLATFORM == 'win32':
    LIB_FILE = '%s.dll'
elif PLATFORM == 'darwin':
    LIB_FILE = 'lib%s.dylib'
    RPATH = "-Wl,-rpath,@loader_path/"
    INSTALL_NAME = "-install_name @rpath/" + LIB_FILE
    CCFLAGS = ['-fPIC']
elif PLATFORM == 'linux2':
    LIB_FILE = 'lib%s.so'
    RPATH = "-Wl,-rpath=${ORIGIN}"
    CCFLAGS = ['-fPIC']
else:
    sys.exit('unknown platform - expected "win32", "darwin" or "linux2"')


def make_ldflags(lib_name, rpath=RPATH, install_name=INSTALL_NAME):
    """
    Make LDFLAGS with rpath, install_name and lib_name.
    """
    ldflags = None
    if rpath:
        ldflags = [rpath]
        if install_name:
            ldflags.append(install_name % lib_name)
    return ldflags


# use dummy to get correct platform metadata
PKG_DATA = []
DUMMY = Extension('%s.dummy' % NAME, sources=[os.path.join(NAME, 'dummy.c')])
LIB_DIR = os.path.join(NAME, PLATFORM)
SRC_DIR = os.path.join(LIB_DIR, 'src')
BUILD_DIR = os.path.join(LIB_DIR, 'build')
TESTS = '%s.tests' % NAME
TEST_DATA = ['test_spectrl2_data.json']
SOLPOS = 'solpos.c'
SOLPOSAM = 'solposAM.c'
SOLPOSAM_LIB = 'solposAM'
SOLPOSAM_LIB_FILE = LIB_FILE % SOLPOSAM_LIB
SPECTRL2 = 'spectrl2.c'
SPECTRL2_2 = 'spectrl2_2.c'
SPECTRL2_LIB = 'spectrl2'
SPECTRL2_LIB_FILE = LIB_FILE % SPECTRL2_LIB
SOLPOS = os.path.join(SRC_DIR, SOLPOS)
SOLPOSAM = os.path.join(SRC_DIR, SOLPOSAM)
SPECTRL2 = os.path.join(SRC_DIR, SPECTRL2)
SPECTRL2_2 = os.path.join(SRC_DIR, SPECTRL2_2)
LIB_FILES_EXIST = all([
    os.path.exists(os.path.join(LIB_DIR, SOLPOSAM_LIB_FILE)),
    os.path.exists(os.path.join(LIB_DIR, SPECTRL2_LIB_FILE))
])

# run clean or build libraries if they don't exist
if 'clean' in sys.argv:
    try:
        os.remove(os.path.join(LIB_DIR, SOLPOSAM_LIB_FILE))
        os.remove(os.path.join(LIB_DIR, SPECTRL2_LIB_FILE))
    except OSError as err:
        sys.stderr.write('%s\n' % err)
elif 'sdist' in sys.argv:
    for plat in ('win32', 'linux2', 'darwin'):
        PKG_DATA.append(os.path.join(plat, '*.*'))
        PKG_DATA.append(os.path.join(plat, 'Makefile'))
        PKG_DATA.append(os.path.join(plat, 'src', '*.*'))
elif not LIB_FILES_EXIST:
    PKG_DATA = [os.path.join(PLATFORM, '*.*'),
                os.path.join(PLATFORM, 'Makefile'),
                os.path.join(PLATFORM, 'src', '*.*')]
    # clean build directory
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)  # delete entire directory tree
    os.mkdir(BUILD_DIR)  # make build directory
    # compile NREL source code
    CC = distutils.ccompiler.new_compiler()  # initialize compiler object
    CC.set_include_dirs([SRC_DIR])  # set includes directory
    # compile solpos and solposAM objects into build directory
    OBJS = CC.compile([SOLPOS, SOLPOSAM], output_dir=BUILD_DIR,
                      extra_preargs=CCFLAGS)
    # link objects and make shared library in build directory
    CC.link_shared_lib(OBJS, SOLPOSAM_LIB, output_dir=BUILD_DIR,
                       extra_preargs=make_ldflags(SOLPOSAM_LIB))
    # compile spectrl2 objects into build directory
    OBJS = CC.compile([SPECTRL2, SPECTRL2_2, SOLPOS], output_dir=BUILD_DIR,
                      extra_preargs=CCFLAGS)
    CC.set_libraries([SOLPOSAM_LIB])  # set linked libraries
    CC.set_library_dirs([BUILD_DIR])  # set library directories
    # link objects and make shared library in build directory
    CC.link_shared_lib(OBJS, SPECTRL2_LIB, output_dir=BUILD_DIR,
                       extra_preargs=make_ldflags(SPECTRL2_LIB))
    # copy files from build to library folder
    shutil.copy(os.path.join(BUILD_DIR, SOLPOSAM_LIB_FILE), LIB_DIR)
    shutil.copy(os.path.join(BUILD_DIR, SPECTRL2_LIB_FILE), LIB_DIR)
    # test libraries
    test_cdlls.test_solposAM()
    test_cdlls.test_spectrl2()

setup(name=NAME,
      version=VERSION,
      packages=[NAME, TESTS],
      package_data={NAME: PKG_DATA, TESTS: TEST_DATA},
      description='Python wrapper around NREL SOLPOS and SPECTRL2',
      ext_modules=[DUMMY])
