# -*- coding: utf-8 -*-
"""
Solar utilities based on `SOLPOS
<http://rredc.nrel.gov/solar/codesandalgorithms/solpos/>`_ and `SPECTRL2
<http://rredc.nrel.gov/solar/models/spectral/>`_ from
`NREL RREDC Solar Resource Models and Tools
<http://www.nrel.gov/rredc/models_tools.html>`_

2013 SunPower Corp.
Confidential & Proprietary
Do Not Distribute

.. document private functions
.. autofunction:: _int2bits
"""

import ctypes
import math
import os
import sys

from solar_utils_exceptions import SOLPOS_Error
from solar_utils_exceptions import SPECTRL2_Error

_DIRNAME = os.path.dirname(__file__)
if sys.platform == 'win32':
    PLATFORM = sys.platform
    SOLPOSAM = 'solposAM.dll'
    SPECTRL2 = 'spectrl2.dll'
elif sys.platform.startswith('linux'):
    PLATFORM = 'linux'
    SOLPOSAM = 'libsolposAM.so'
    SPECTRL2 = 'libspectrl2.so'
elif sys.platform.startswith('darwin'):
    PLATFORM = 'darwin'
    SOLPOSAM = 'libsolposAM.dylib'
    SPECTRL2 = 'libspectrl2.dylib'

SOLPOSAMDLL = os.path.join(_DIRNAME, PLATFORM, SOLPOSAM)
SPECTRL2DLL = os.path.join(_DIRNAME, PLATFORM, SPECTRL2)


def _int2bits(x):
    """
    Convert integer to bits.

    :param x: integer to convert
    :returns: log(x, 2)
    """
    return int(math.log(x, 2))


def solposAM(location, datetime, weather):
    """
    Calculate solar position and air mass by calling functions exported by
    :data:`SOLPOSAMDLL`.

    :param location: [longitude, latitude, UTC-timezone]
    :type location: list of floats
    :param datetime: [year, month, day, hour, minute, second]
    :type datetime: list of ints
    :param weather: [ambient-pressure (mB), ambient-temperature (C)]
    :type weather: list of floats
    :returns: angles, airmass
    :rtype: float
    :raises: :exc:`~solar_utils.solar_utils_exceptions.SOLPOS_Error`
    """
    # load the DLL
    solposAMdll = ctypes.cdll.LoadLibrary(SOLPOSAMDLL)
    solposAM = solposAMdll.solposAM
    # cast Python types as ctypes
    _location = (ctypes.c_float * 3)(*location)
    _datetime = (ctypes.c_int * 6)(*datetime)
    _weather = (ctypes.c_float * 2)(*weather)
    # allocate space for results
    angles = (ctypes.c_float * 2)()
    airmass = (ctypes.c_float * 2)()
    settings = (ctypes.c_int * 2)()
    orientation = (ctypes.c_float * 2)()
    shadowband = (ctypes.c_float * 3)()
    # call DLL
    code = solposAM(_location, _datetime, _weather, angles, airmass, settings,
                    orientation, shadowband)
    # return results if successful, otherwise raise SOLPOS_Error
    if code == 0:
        return angles, airmass
    else:
        # convert code to bits
        _code = _int2bits(code)
        data = {'location': location,
                'datetime': datetime,
                'weather': weather,
                'angles': angles,
                'airmass': airmass,
                'settings': settings,
                'orientation': orientation,
                'shadowband': shadowband}
        raise SOLPOS_Error(_code, data)


def spectrl2(units, location, datetime, weather, orientation,
             atmosphericConditions, albedo):
    """
    Calculate solar spectrum by calling functions exported by
    :data:`SPECTRL2DLL`.

    :param units: set ``units`` = 1 for W/m\ :sup:`2`/micron
    :type units: int
    :param location: longitude, latitude and UTC-timezone
    :type location: list of floats
    :param datetime: year, month, day, hour, minute and second
    :type datetime: list of ints
    :param weather: ambient-pressure [mB] and ambient-temperature [C]
    :type weather: list of floats
    :param orientation: tilt and aspect [degrees]
    :type orientation: list of floats
    :param atmosphericConditions: alpha, assym, ozone, tau500 and watvap
    :type atmosphericConditions: list of floats
    :param albedo: 6 wavelengths and 6 reflectivities
    :type albedo: list of lists of floats
    :returns: specdif, specdir, specetr, specglo and specx
    :rtype: float
    :raises: :exc:`~solar_utils.solar_utils_exceptions.SPECTRL2_Error`,
        :exc:`~solar_utils.solar_utils_exceptions.SOLPOS_Error`

    .. seealso::
        :func:`solposAM`

    **Examples:**

    >>> units = 1
    >>> location = [33.65, -84.43, -5.0]
    >>> datetime = [1999, 7, 22, 9, 45, 37]
    >>> weather = [1006.0, 27.0]
    >>> orientation = [33.65, 135.0]
    >>> atmosphericConditions = [1.14, 0.65, -1.0, 0.2, 1.36]
    >>> albedo = [0.3, 0.7, 0.8, 1.3, 2.5, 4.0] + ([0.2] * 6)
    >>> (specdif, specdir, specetr, specglo,
         specx) = spectrl2(units, location, datetime, weather, orientation,
                           atmosphericConditions, albedo)
    """
    # requires 'solpos.dll'
    # load the DLL
    ctypes.cdll.LoadLibrary(SOLPOSAMDLL)
    spectrl2DLL = ctypes.cdll.LoadLibrary(SPECTRL2DLL)
    spectrl2 = spectrl2DLL.spectrl2
    # cast Python types as ctypes
    _location = (ctypes.c_float * 3)(*location)
    _datetime = (ctypes.c_int * 6)(*datetime)
    _weather = (ctypes.c_float * 2)(*weather)
    _orientation = (ctypes.c_float * 2)(*orientation)
    _atmosphericConditions = (ctypes.c_float * 5)(*atmosphericConditions)
    _albedo = (ctypes.c_float * 12)(*albedo)
    # allocate space for results
    specdif = (ctypes.c_float * 122)()
    specdir = (ctypes.c_float * 122)()
    specetr = (ctypes.c_float * 122)()
    specglo = (ctypes.c_float * 122)()
    specx = (ctypes.c_float * 122)()
    angles = (ctypes.c_float * 2)()
    airmass = (ctypes.c_float * 2)()
    settings = (ctypes.c_int * 2)()
    shadowband = (ctypes.c_float * 3)()
    # call DLL
    code = spectrl2(units, _location, _datetime, _weather, _orientation,
                    _atmosphericConditions, _albedo, specdif, specdir, specetr,
                    specglo, specx, angles, airmass, settings, shadowband)
    # return results if successful, otherwise raise exception
    if code == 0:
        return specdif, specdir, specetr, specglo, specx
    elif code < 0:
        data = {'units': units,
                'tau500': atmosphericConditions[3],
                'watvap': atmosphericConditions[4],
                'assym': atmosphericConditions[1]}
        raise SPECTRL2_Error(code, data)
    else:
        # convert code to bits
        _code = _int2bits(code)
        data = {'location': location,
                'datetime': datetime,
                'weather': weather,
                'angles': angles,
                'airmass': airmass,
                'settings': settings,
                'orientation': orientation,
                'shadowband': shadowband}
        raise SOLPOS_Error(_code, data)
