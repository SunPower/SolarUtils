#define macros
SOLPOSAM = libsolposAM.so
SOLPOSAM_LIB = solposAM
SPECTRL2 = libspectrl2.so
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
	cc -Wl,-rpath='$${ORIGIN}' -shared -fPIC -Wall $(SOLPOSAM_SRC) \
		-o $(BUILD_DIR)/$(SOLPOSAM)

spectrl2: create_dirs
	cc -L$(BUILD_DIR) -Wl,-rpath='$${ORIGIN}' -shared -fPIC -Wall \
		$(SPECTRL2_SRC) -o $(BUILD_DIR)/$(SPECTRL2) -l$(SOLPOSAM_LIB)

install:
	install $(BUILD_DIR)/*.so ./

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
