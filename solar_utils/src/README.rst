Installation
============
1. run configure.cmd
2. run nmake

Usage
=====
1. Import `ctypes` package from Python Standard Reference Library::
    >>> import ctypes

2. Load the dll::
    >>> solposAMdll = ctypes.cdll.LoadLibrary('solposAM.dll')

3. Load the function::
    >>> solposAM = solposAMdll.solposAM

4. Cast inputs and outputs as ctypes. For arrays, use ctype array constructor
call in Python::
    >>> location = (ctypes.c_double * 3)(35.56836, -119.2022, -8.0)
    >>> weather = (ctypes.c_double * 2)(1015.62055, 40.0)
    >>> datetime = (ctypes.c_double * 6)(2013.0, 6.0, 5.0, 12.0, 31.0, 0.0)
    >>> angles = (ctypes.c_double * 2)()

5. now call the function, it always returns an int, even if the return type is
void.
    >>> code = solposAM(location, datetime, weather, angles, airmass)
    0

6. extract the values just like regular python values.
    >>> angles[0]
    15.074043273925781
    >>> angles[1]
    213.29042053222656
    >>> location[0]
    35.56836
    location[1]
    >>> -119.2022

7. Standard error is displayed in the console
    >>> datetime = (ctypes.c_double * 6)(2051.0, 6.0, 5.0, 12.0, 31.0, 0.0)
    >>> solposAM(location, datetime, weather, angles)
    S_decode ==> Please fix the year: 2051 [1950-2050]
    >>> 1

Notes
=====
* Don't touch original source solpos.c, solpos00.h, spectrl2_2.c and
  spectrl2_2.h.
* Use solpos00.c and spectest.c as examples.
* Add dllexport by defining a macro:

    #define DllExport   __declspec( dllexport ) /* macro for exporting functions

* Begin function with DllExport
* Make function return long.
* Declare outputs as pointers in the input args.
* Declare all inputs as input args.

    DllExport long retval solposAM(double *location, double *datetime,
                                   double *weather, double *angles,
                                   double *airmass)

* Use pointers for arrays.
* Avoid structures.
