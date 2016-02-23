#define macros
SOLPOSAM = solposAM.dll
SOLPOSAM_LIB = solposAM.lib
SPECTRL2 = spectrl2.dll
SPECTEST = spectest.exe
STEST00 = stest00.exe

SRC_DIR = src
BUILD_DIR = build

SOLPOSAM_SRC = \
	$(SRC_DIR)\solposAM.c \
	$(SRC_DIR)\solpos.c

SPECTRL2_SRC = \
	$(SRC_DIR)\spectrl2.c \
	$(SRC_DIR)\spectrl2_2.c \
	$(SRC_DIR)\solpos.c

SPECTEST_SRC = \
	$(SRC_DIR)\spectest.c \
	$(SRC_DIR)\spectrl2_2.c \
	$(SRC_DIR)\solpos.c

STEST00_SRC = \
	$(SRC_DIR)\stest00.c \
	$(SRC_DIR)\solpos.c

SOLPOSAM_LOG = $(BUILD_DIR)\solposAM.log
SPECTRL2_LOG = $(BUILD_DIR)\spectrl2.log

all: uninstall clean solposAM spectrl2 install test

clean:
	@echo.
	@echo Cleaning $(BUILD_DIR) ...
	@if exist $(BUILD_DIR) rmdir /S /Q $(BUILD_DIR)

create_dirs:
	@echo.
	@echo Creating $(BUILD_DIR) ...
	@if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)

solposAM: create_dirs
	@echo.
	@echo Compiling $(SOLPOSAM) ...
	cl /LD /Wall /showIncludes /DWIN32 /Ox /MD /GS- /Fo$(BUILD_DIR)\ \
		/Fe$(BUILD_DIR)\$(SOLPOSAM) $(SOLPOSAM_SRC) > $(SOLPOSAM_LOG) 2>&1

spectrl2: create_dirs
	@echo.
	@echo Compiling $(SPECTRL2) ...
	@if not exist $(BUILD_DIR)\$(SOLPOSAM_LIB) \
		echo *** Missing $(BUILD_DIR)\$(SOLPOSAM_LIB) ***
	cl /LD /Wall /showIncludes /DWIN32 /Ox /MD /GS- /Fo$(BUILD_DIR)\ \
		/Fe$(BUILD_DIR)\$(SPECTRL2) $(SPECTRL2_SRC) \
		/link $(BUILD_DIR)\$(SOLPOSAM_LIB) > $(SPECTRL2_LOG) 2>&1

install:
	@echo.
	@echo Installing ...
	copy $(BUILD_DIR)\*.dll .\

uninstall:
	@echo.
	@echo Uninstalling $(SOLPOSAM) ...
	@if exist $(SOLPOSAM) del $(SOLPOSAM)
	@echo Uninstalling $(SPECTRL2) ...
	@if exist $(SPECTRL2) del $(SPECTRL2)

spectest:
	cl /Fo$(BUILD_DIR)\ /Fe$(BUILD_DIR)\$(SPECTEST)  \
		$(SPECTEST_SRC) >> $(SPECTRL2_LOG) 2>&1

stest00:
	cl /Fo$(BUILD_DIR)\ /Fe$(BUILD_DIR)\$(STEST00) \
		$(STEST00_SRC) >> $(SOLPOSAM_LOG) 2>&1

test: spectest stest00
	@echo.
	@echo Testing ...
	@if exist $(BUILD_DIR)\$(SPECTEST) $(BUILD_DIR)\$(SPECTEST) >> $(SPECTRL2_LOG) 2>&1
	@if exist $(BUILD_DIR)\$(STEST00) $(BUILD_DIR)\$(STEST00) >> $(SOLPOSAM_LOG) 2>&1
