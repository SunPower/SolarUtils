"""
SolarUtils Package Setup
Copyright (c) 2016 SunPower Corp.
Confidential & Proprietary
Do Not Distribute
"""

import sys
import os
import shutil
from distutils import unixccompiler
try:
    from setuptools import setup, distutils, Extension
except ImportError:
    sys.exit('setuptools was not detected - please install setuptools and pip')
from solar_utils import (
    __version__ as VERSION, __name__ as NAME, __author__ as AUTHOR,
    __email__ as EMAIL, __url__ as URL
)
from solar_utils.tests import test_cdlls
import logging

logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger('SETUP')

README = 'README.rst'
try:
    with open(os.path.join(os.path.dirname(__file__), README), 'r') as readme:
        README = readme.read()
except IOError:
    README = ''

# set platform constants
CCFLAGS, RPATH, INSTALL_NAME, LDFLAGS, MACROS = None, None, None, None, None
PYVERSION = sys.version_info
PLATFORM = sys.platform
if PLATFORM == 'win32':
    LIB_FILE = '%s.dll'
    MACROS = [('WIN32', None)]
    if PYVERSION.major >= 3 and PYVERSION.minor >= 5:
        LDFLAGS = ['/DLL']
elif PLATFORM == 'darwin':
    LIB_FILE = 'lib%s.dylib'
    RPATH = "-Wl,-rpath,@loader_path/"
    INSTALL_NAME = "@rpath/" + LIB_FILE
    CCFLAGS = LDFLAGS = ['-fPIC']
elif PLATFORM in ['linux', 'linux2']:
    PLATFORM = 'linux'
    LIB_FILE = 'lib%s.so'
    RPATH = "-Wl,-rpath,${ORIGIN}"
    CCFLAGS = LDFLAGS = ['-fPIC']
else:
    sys.exit('Platform "%s" is unknown or unsupported.' % PLATFORM)


def make_ldflags(ldflags=LDFLAGS, rpath=RPATH):
    """
    Make LDFLAGS with rpath, install_name and lib_name.
    """
    if ldflags and rpath:
        ldflags.extend([rpath])
    elif rpath:
        ldflags = [rpath]
    return ldflags


def make_install_name(lib_name, install_name=INSTALL_NAME):
    """
    Make INSTALL_NAME with and lib_name.
    """
    if install_name:
        return ['-install_name', install_name % lib_name]
    else:
        return None


def dylib_monkeypatch(self):
    """
    Monkey patch :class:`distutils.UnixCCompiler` for darwin so libraries use
    '.dylib' instead of '.so'.

    """
    def link_dylib_lib(self, objects, output_libname, output_dir=None,
                       libraries=None, library_dirs=None,
                       runtime_library_dirs=None, export_symbols=None,
                       debug=0, extra_preargs=None, extra_postargs=None,
                       build_temp=None, target_lang=None):
        """implementation of link_shared_lib"""
        self.link("shared_library", objects,
                  self.library_filename(output_libname, lib_type='dylib'),
                  output_dir,
                  libraries, library_dirs, runtime_library_dirs,
                  export_symbols, debug,
                  extra_preargs, extra_postargs, build_temp, target_lang)
    self.link_so = self.link_shared_lib
    self.link_shared_lib = link_dylib_lib
    return self


# use dummy to get correct platform metadata
PKG_DATA = ['NREL_DISCLAIMERS-COPYRIGHTS-LICENSES.txt']
DUMMY = Extension('%s.dummy' % NAME, sources=[os.path.join(NAME, 'dummy.c')])
SRC_DIR = os.path.join(NAME, 'src')
BUILD_DIR = os.path.join(NAME, 'build')
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
SOLPOSAM_LIB_PATH = os.path.join(NAME, SOLPOSAM_LIB_FILE)
SPECTRL2_LIB_PATH = os.path.join(NAME, SPECTRL2_LIB_FILE)
LIB_FILES_EXIST = all([
    os.path.exists(SOLPOSAM_LIB_PATH),
    os.path.exists(SPECTRL2_LIB_PATH)
])

# run clean or build libraries if they don't exist
if 'clean' in sys.argv:
    try:
        os.remove(SOLPOSAM_LIB_PATH)
        os.remove(SPECTRL2_LIB_PATH)
    except OSError as err:
        sys.stderr.write('%s\n' % err)
elif 'sdist' in sys.argv:
    for plat in ('win32', 'linux', 'darwin'):
        PKG_DATA.append('%s.mk' % plat)
    PKG_DATA.append(os.path.join('src', '*.*'))
    PKG_DATA.append(os.path.join('src', 'orig', 'solpos', '*.*'))
    PKG_DATA.append(os.path.join('src', 'orig', 'spectrl2', '*.*'))
elif not LIB_FILES_EXIST:
    # clean build directory
    if os.path.exists(BUILD_DIR):
        shutil.rmtree(BUILD_DIR)  # delete entire directory tree
    os.mkdir(BUILD_DIR)  # make build directory
    # compile NREL source code
    if PLATFORM == 'darwin':
        CCOMPILER = unixccompiler.UnixCCompiler
        OSXCCOMPILER = dylib_monkeypatch(CCOMPILER)
        CC = OSXCCOMPILER(verbose=3)
    else:
        CC = distutils.ccompiler.new_compiler()  # initialize compiler object
    CC.add_include_dir(SRC_DIR)  # set includes directory
    # compile solpos and solposAM objects into build directory
    OBJS = CC.compile([SOLPOS, SOLPOSAM], output_dir=BUILD_DIR,
                      extra_preargs=CCFLAGS, macros=MACROS)
    # link objects and make shared library in build directory
    CC.link_shared_lib(OBJS, SOLPOSAM_LIB, output_dir=BUILD_DIR,
                       extra_preargs=make_ldflags(),
                       extra_postargs=make_install_name(SOLPOSAM_LIB))
    # compile spectrl2 objects into build directory
    OBJS = CC.compile([SPECTRL2, SPECTRL2_2, SOLPOS], output_dir=BUILD_DIR,
                      extra_preargs=CCFLAGS, macros=MACROS)
    CC.add_library(SOLPOSAM_LIB)  # set linked libraries
    CC.add_library_dir(BUILD_DIR)  # set library directories
    # link objects and make shared library in build directory
    CC.link_shared_lib(OBJS, SPECTRL2_LIB, output_dir=BUILD_DIR,
                       extra_preargs=make_ldflags(),
                       extra_postargs=make_install_name(SPECTRL2_LIB))
    # copy files from build to library folder
    shutil.copy(os.path.join(BUILD_DIR, SOLPOSAM_LIB_FILE), NAME)
    shutil.copy(os.path.join(BUILD_DIR, SPECTRL2_LIB_FILE), NAME)
    # test libraries
    test_cdlls.test_solposAM()
    test_cdlls.test_spectrl2()
    LIB_FILES_EXIST = True
if LIB_FILES_EXIST and 'sdist' not in sys.argv:
    PKG_DATA += [SOLPOSAM_LIB_FILE, SPECTRL2_LIB_FILE]

setup(
    name='SolarUtils',
    version=VERSION,
    description='Python wrappers around NREL SOLPOS and SPECTRL2',
    long_description=README,
    author=AUTHOR,
    author_email=EMAIL,
    url=URL,
    license='BSD 3-Clause',
    platforms=['win32', 'linux', 'linux2', 'darwin'],
    packages=[NAME, TESTS],
    package_data={NAME: PKG_DATA, TESTS: TEST_DATA},
    ext_modules=[DUMMY]
)
