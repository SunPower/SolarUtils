#define macros
SOLPOSAM = libsolposAM.dylib
SOLPOSAM_LIB = solposAM
SPECTRL2 = libspectrl2.dylib
SPECTEST = spectest
STEST00 = stest00

SRC_DIR = src
BUILD_DIR = build

SOLPOSAM_SRC = \
	$(SRC_DIR)/solposAM.c \
	$(SRC_DIR)/solpos.c

SPECTRL2_SRC = \
	$(SRC_DIR)/spectrl2.c \
	$(SRC_DIR)/spectrl2_2.c \
	$(SRC_DIR)/solpos.c

SPECTEST_SRC = \
	$(SRC_DIR)/spectest.c \
	$(SRC_DIR)/spectrl2_2.c \
	$(SRC_DIR)/solpos.c

STEST00_SRC = \
	$(SRC_DIR)/stest00.c \
	$(SRC_DIR)/solpos.c

SOLPOSAM_LOG = $(BUILD_DIR)/solposAM.log
SPECTRL2_LOG = $(BUILD_DIR)/spectrl2.log

all: uninstall clean solposAM spectrl2 install test

clean:
	rm -rf $(BUILD_DIR)

create_dirs:
	mkdir -p $(BUILD_DIR)

solposAM: create_dirs
	cc -Wl,-rpath,@loader_path/ -shared -fPIC -Wall $(SOLPOSAM_SRC) \
		-o $(BUILD_DIR)/$(SOLPOSAM) -install_name @rpath/$(SOLPOSAM)

spectrl2: create_dirs
	cc -L$(BUILD_DIR) -Wl,-rpath,@loader_path/ -shared -fPIC -Wall \
		$(SPECTRL2_SRC) -o $(BUILD_DIR)/$(SPECTRL2) -l$(SOLPOSAM_LIB) \
		-install_name @rpath/$(SPECTRL2)

install:
	install $(BUILD_DIR)/*.dylib ./

uninstall:
	rm -f $(SOLPOSAM) $(SPECTRL2)

spectest:
	cc -fPIC -Wall $(SPECTEST_SRC) -o $(BUILD_DIR)/$(SPECTEST)

stest00:
	cc -fPIC -Wall $(STEST00_SRC) -o $(BUILD_DIR)/$(STEST00)

test: spectest stest00
	$(BUILD_DIR)/$(SPECTEST) >> SPECTRL2_LOG
	$(BUILD_DIR)/$(STEST00) >> SOLPOSAM_LOG

# https://gcc.gnu.org/onlinedocs/gcc/Link-Options.html
# -Wl,option
#	Pass option as an option to the linker. If option contains commas, it is
#	split into multiple options at the commas. You can use this syntax to pass
#	an argument to the option. For example, -Wl,-Map,output.map passes
#	-Map output.map to the linker. When using the GNU linker, you can also get
#	the same effect with -Wl,-Map=output.map.

# https://gcc.gnu.org/onlinedocs/gcc/Darwin-Options.html
# -install_name <path>

# https://developer.apple.com/library/mac/documentation/DeveloperTools/Conceptual/DynamicLibraries/100-Articles/RunpathDependentLibraries.html
# -install_name <path>

# https://developer.apple.com/library/ios/documentation/MacOSX/Conceptual/BPFrameworks/Concepts/FrameworkBinding.html
# otool

# https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/xcode-select.1.html
# install_name_tool

# https://developer.apple.com/library/mac/documentation/Darwin/Reference/ManPages/man1/dyld.1.html
# @loader_path/
#	This variable is replaced with the path to the directory containing the  mach-o  binary  which
#	contains  the load command using @loader_path. Thus, in every binary, @loader_path resolves to
#	a different path, whereas @executable_path always resolves to the same path.  @loader_path  is
#	useful  as the load path for a framework/dylib embedded in a plug-in, if the final file system
#	location of the plugin-in unknown (so absolute paths cannot be used) or if the plug-in is used
#	by  multiple  applications (so @executable_path cannot be used). If the plug-in mach-o file is
#	at  /some/path/Myfilter.plugin/Contents/MacOS/Myfilter  and  a  framework  dylib  file  is  at
#	/some/path/Myfilter.plugin/Contents/Frameworks/Foo.framework/Versions/A/Foo,  then  the frame-work framework
#	work load path could be encoded as @loader_path/../Frameworks/Foo.framework/Versions/A/Foo and
#	the  Myfilter.plugin directory could be moved around in the file system and dyld will still be
#	able to load the embedded framework.
#
# @rpath/
#	Dyld maintains a current stack of paths called the run path list.  When @rpath is  encountered
#	it  is  substituted  with each path in the run path list until a loadable dylib if found.  The
#	run path stack is built from the LC_RPATH load commands in the depencency chain that  lead  to
#	the  current  dylib  load.   You  can add an LC_RPATH load command to an image with the -rpath
#	option  to  ld(1).   You  can  even  add  a  LC_RPATH  load  command  path  that  starts  with
#	@loader_path/,  and  it will push a path on the run path stack that relative to the image con-taining containing
#	taining the LC_RPATH.  The use of @rpath is most useful when  you  have  a  complex  directory
#	structure  of  programs  and  dylibs  which can be installed anywhere, but keep their relative
#	positions.  This scenario could be implemented using @loader_path, but every client of a dylib
#	could  need  a different load path because its relative position in the file system is differ-ent. different.
#	ent. The use of @rpath introduces a level of indirection that simplies  things.   You  pick  a
#	location in your directory structure as an anchor point.  Each dylib then gets an install path
#	that starts with @rpath and is the path to the dylib relative to the anchor point.  Each  main
#	executable  is  linked with -rpath @loader_path/zzz, where zzz is the path from the executable
#	to the anchor point.  At runtime dyld sets it run path to be the anchor point, then each dylib
#	is found relative to the anchor point.
