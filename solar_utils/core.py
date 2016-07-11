# -*- coding: utf-8 -*-
"""
Solar utilities based on `SOLPOS
<http://rredc.nrel.gov/solar/codesandalgorithms/solpos/>`_ and `SPECTRL2
<http://rredc.nrel.gov/solar/models/spectral/>`_ from
`NREL RREDC Solar Resource Models and Tools
<http://www.nrel.gov/rredc/models_tools.html>`_

2013 SunPower Corp.
"""

import ctypes
import math
import os
import sys
from solar_utils.exceptions import SOLPOS_Error, SPECTRL2_Error

_DIRNAME = os.path.dirname(__file__)
PLATFORM = sys.platform
if PLATFORM == 'win32':
    SOLPOSAM = 'solposAM.dll'
    SPECTRL2 = 'spectrl2.dll'
elif PLATFORM in ['linux2', 'linux']:
    PLATFORM = 'linux'
    SOLPOSAM = 'libsolposAM.so'
    SPECTRL2 = 'libspectrl2.so'
elif PLATFORM == 'darwin':
    SOLPOSAM = 'libsolposAM.dylib'
    SPECTRL2 = 'libspectrl2.dylib'
else:
    raise OSError('Platform "%s" is unknown or unsupported.' % PLATFORM)
SOLPOSAMDLL = os.path.join(_DIRNAME, SOLPOSAM)
SPECTRL2DLL = os.path.join(_DIRNAME, SPECTRL2)


def _int2bits(err_code):
    """
    Convert integer to bits.

    :param err_code: integer to convert
    :returns: log(err_code, 2)
    """
    return int(math.log(err_code, 2))


def solposAM(location, datetime, weather):
    """
    Calculate solar position and air mass by calling functions exported by
    :data:`SOLPOSAMDLL`.

    :param location: [latitude, longitude, UTC-timezone]
    :type location: float
    :param datetime: [year, month, day, hour, minute, second]
    :type datetime: int
    :param weather: [ambient-pressure (mB), ambient-temperature (C)]
    :type weather: float
    :returns: angles [degrees], airmass [atm]
    :rtype: float
    :raises: :exc:`~solar_utils.exceptions.SOLPOS_Error`

    Returns the solar zenith and azimuth angles in degrees, as well as the
    relative and absolute (or pressure corrected) air mass.

    **Examples:**

    >>> location = [35.56836, -119.2022, -8.0]
    >>> datetime = [2013, 6, 5, 12, 31, 0]
    >>> weather = [1015.62055, 40.0]
    >>> (angles, airmass) = solposAM(location, datetime, weather)
    >>> list(angles)
    [15.074043273925781, 213.29042053222656]
    >>> list(airmass)
    [1.0352272987365723, 1.0379053354263306]
    """
    # load the DLL
    solposAM_dll = ctypes.cdll.LoadLibrary(SOLPOSAMDLL)
    _solposAM = solposAM_dll.solposAM
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
    err_code = _solposAM(_location, _datetime, _weather, angles, airmass,
                         settings, orientation, shadowband)
    # return results if successful, otherwise raise SOLPOS_Error
    if err_code == 0:
        return angles, airmass
    else:
        # convert err_code to bits
        _code = _int2bits(err_code)
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
             atmospheric_conditions, albedo):
    """
    Calculate solar spectrum by calling functions exported by
    :data:`SPECTRL2DLL`.

    :param units: set ``units`` = 1 for W/m\ :sup:`2`/micron
    :type units: int
    :param location: latitude, longitude and UTC-timezone
    :type location: float
    :param datetime: year, month, day, hour, minute and second
    :type datetime: int
    :param weather: ambient-pressure [mB] and ambient-temperature [C]
    :type weather: float
    :param orientation: tilt and aspect [degrees]
    :type orientation: float
    :param atmospheric_conditions: alpha, assym, ozone, tau500 and watvap
    :type atmospheric_conditions: float
    :param albedo: 6 wavelengths and 6 reflectivities
    :type albedo: float
    :returns: spectral decomposition, x-coordinate
    :rtype: float
    :raises: :exc:`~solar_utils.exceptions.SPECTRL2_Error`,
        :exc:`~solar_utils.exceptions.SOLPOS_Error`

    Returns the diffuse, direct, extraterrestrial and global spectral components
    on the tilted surface in as a function of x-coordinate specified by units.

    =====  ===============================================================
    units  output units
    =====  ===============================================================
    1      irradiance (W/sq m/micron) per wavelength (microns)
    2      photon flux (10.0E+16 /sq cm/s/micron) per wavelength (microns)
    3      photon flux density (10.0E+16 /sq cm/s/eV) per energy (eV)
    =====  ===============================================================

    See
    `NREL SPECTRL2 Documentation <http://rredc.nrel.gov/solar/models/spectral/spectrl2/documentation.html>`_
    for more detail.

    .. seealso::
        :func:`solposAM`

    **Examples:**

    >>> units = 1
    >>> location = [33.65, -84.43, -5.0]
    >>> datetime = [1999, 7, 22, 9, 45, 37]
    >>> weather = [1006.0, 27.0]
    >>> orientation = [33.65, 135.0]
    >>> atmospheric_conditions = [1.14, 0.65, -1.0, 0.2, 1.36]
    >>> albedo = [0.3, 0.7, 0.8, 1.3, 2.5, 4.0] + ([0.2] * 6)
    >>> (specdif, specdir, specetr, specglo,
         specx) = spectrl2(units, location, datetime, weather, orientation,
                           atmospheric_conditions, albedo)
    """
    # load the DLL
    ctypes.cdll.LoadLibrary(SOLPOSAMDLL)  # requires 'solpos.dll'
    spectrl2_dll = ctypes.cdll.LoadLibrary(SPECTRL2DLL)
    _spectrl2 = spectrl2_dll.spectrl2
    # cast Python types as ctypes
    _location = (ctypes.c_float * 3)(*location)
    _datetime = (ctypes.c_int * 6)(*datetime)
    _weather = (ctypes.c_float * 2)(*weather)
    _orientation = (ctypes.c_float * 2)(*orientation)
    _atmospheric_conditions = (ctypes.c_float * 5)(*atmospheric_conditions)
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
    err_code = _spectrl2(
        units, _location, _datetime, _weather, _orientation,
        _atmospheric_conditions, _albedo, specdif, specdir, specetr, specglo,
        specx, angles, airmass, settings, shadowband
    )
    # return results if successful, otherwise raise exception
    if err_code == 0:
        return specdif, specdir, specetr, specglo, specx
    elif err_code < 0:
        data = {'units': units,
                'tau500': atmospheric_conditions[3],
                'watvap': atmospheric_conditions[4],
                'assym': atmospheric_conditions[1]}
        raise SPECTRL2_Error(err_code, data)
    else:
        # convert err_code to bits
        _code = _int2bits(err_code)
        data = {'location': location,
                'datetime': datetime,
                'weather': weather,
                'angles': angles,
                'airmass': airmass,
                'settings': settings,
                'orientation': orientation,
                'shadowband': shadowband}
        raise SOLPOS_Error(_code, data)
