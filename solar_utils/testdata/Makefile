BUILD_DIR = build
SPECTRL2 = spectest.exe
SOLPOS = stest00.exe
SPECTEST = spectest.txt
STEST00 = stest00.txt

all: clean create_dirs spectrl2 solpos test

clean:
  @echo.
  @echo Cleaning $(BUILD_DIR) ...
  @if exist $(BUILD_DIR) rmdir /S /Q $(BUILD_DIR)

create_dirs:
  @echo.
  @echo Creating $(BUILD_DIR) ...
  @if not exist $(BUILD_DIR) mkdir $(BUILD_DIR)

spectrl2:
  cl /Fo$(BUILD_DIR)\ /Fe$(BUILD_DIR)\$(SPECTRL2) spectest.c spectrl2.c solpos.c

solpos:
  cl /Fo$(BUILD_DIR)\ /Fe$(BUILD_DIR)\$(SOLPOS) stest00.c solpos.c

test:
  @echo.
  @if exist $(BUILD_DIR)\$(SPECTRL2) $(BUILD_DIR)\$(SPECTRL2) > $(SPECTEST)
  @if exist $(SPECTEST) type $(SPECTEST)
  @if exist $(BUILD_DIR)\$(SOLPOS) $(BUILD_DIR)\$(SOLPOS) > $(STEST00)
  @if exist $(STEST00) type $(STEST00)
