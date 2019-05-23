#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for solar utilities.

Usage
=====
This code uses nose. Enter the following in a CMD shell::

    $ nosetests --verbose

2013, 2019 SunPower Corp.
"""

import datetime as pydatetime
import json
import numpy as np
import os
from nose.tools import ok_

from solar_utils import *
from solar_utils.exceptions import SOLPOS_Error, SPECTRL2_Error

_DIRNAME = os.path.dirname(__file__)
TOL = 1E-3

RELDIFF = lambda x, x0: np.abs(x - x0) / x0


def test_get_solpos8760():
    location = [35.56836, -119.2022, -8.0]
    weather = [1015.62055, 40.0]
    x, y = get_solpos8760(location, 2017, weather)
    z = np.array([
        [ 98.96697  , 248.12735  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.86818  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.86365  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85951  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85494  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85041  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.84623  ,  -1.       ,  -1.       ],
        [ 91.8338   , 117.05424  ,  64.716125 ,  64.88354  ],
        [ 81.50037  , 126.166016 ,   6.489029 ,   6.5058155],
        [ 72.399506 , 136.78699  ,   3.2762375,   3.2847128],
        [ 65.06621  , 149.33855  ,   2.3618126,   2.3679223],
        [ 60.21105  , 163.89734  ,   2.0070193,   2.0122113],
        [ 58.47457  , 179.82529  ,   1.9076174,   1.9125524],
        [ 60.13257  , 195.77512  ,   2.002265 ,   2.0074446],
        [ 64.921104 , 210.37862  ,   2.3491564,   2.3552334],
        [ 72.20489  , 222.98093  ,   3.2422662,   3.2506535],
        [ 81.272095 , 233.6459   ,   6.333636 ,   6.3500204],
        [ 91.55735  , 242.79282  ,  64.014565 ,  64.18017  ],
        [ 98.96697  , 248.20842  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.21324  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.21808  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.22249  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.22736  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.23221  ,  -1.       ,  -1.       ]],
        dtype=np.float32)
    assert np.allclose(x[:24], z[:24,:2])
    assert np.allclose(y[:24], z[:24,2:])


def test_get_solposAM():
    location = [35.56836, -119.2022, -8.0]
    weather = [1015.62055, 40.0]
    times = [
        (pydatetime.datetime(2017, 1, 1, 0, 0, 0)
         + pydatetime.timedelta(hours=h)).timetuple()[:6]
        for h in range(1000)]
    x, y = get_solposAM(location, times, weather)
    z = np.array([
        [ 98.96697  , 248.12735  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.86818  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.86365  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85951  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85494  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.85041  ,  -1.       ,  -1.       ],
        [ 98.96697  , 111.84623  ,  -1.       ,  -1.       ],
        [ 91.8338   , 117.05424  ,  64.716125 ,  64.88354  ],
        [ 81.50037  , 126.166016 ,   6.489029 ,   6.5058155],
        [ 72.399506 , 136.78699  ,   3.2762375,   3.2847128],
        [ 65.06621  , 149.33855  ,   2.3618126,   2.3679223],
        [ 60.21105  , 163.89734  ,   2.0070193,   2.0122113],
        [ 58.47457  , 179.82529  ,   1.9076174,   1.9125524],
        [ 60.13257  , 195.77512  ,   2.002265 ,   2.0074446],
        [ 64.921104 , 210.37862  ,   2.3491564,   2.3552334],
        [ 72.20489  , 222.98093  ,   3.2422662,   3.2506535],
        [ 81.272095 , 233.6459   ,   6.333636 ,   6.3500204],
        [ 91.55735  , 242.79282  ,  64.014565 ,  64.18017  ],
        [ 98.96697  , 248.20842  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.21324  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.21808  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.22249  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.22736  ,  -1.       ,  -1.       ],
        [ 98.96697  , 248.23221  ,  -1.       ,  -1.       ]],
        dtype=np.float32)
    assert np.allclose(x[:24], z[:24,:2])
    assert np.allclose(y[:24], z[:24,2:])
    # test LOCATION
    location = [1135.56836, -119.2022, -8.0]
    try:
        x, y = get_solposAM(location, times, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_LAT_ERROR'
    location = [35.56836, -119.2022, -8.0]
    # test DATETIMES
    times = [list(ts) for ts in times]
    times[10][5] = 3248273
    times = [tuple(ts) for ts in times]
    try:
        x, y = get_solposAM(location, times, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_SECOND_ERROR'


def test_solposAM():
    """
    test solposAM.dll
    """
    # test data
    test_data = {'angles': [15.074043273925781, 213.29042053222656],
                 'airmass': [1.0352272987365723, 1.0379053354263306]}
    location = [35.56836, -119.2022, -8.0]
    datetime = [2013, 6, 5, 12, 31, 0]
    weather = [1015.62055, 40.0]
    # call test function
    angles, airmass = solposAM(location, datetime, weather)
    # test OUTPUTS are within TOL
    ok_(RELDIFF(angles[0], test_data['angles'][0]) < TOL)
    ok_(RELDIFF(angles[1], test_data['angles'][1]) < TOL)
    ok_(RELDIFF(airmass[0], test_data['airmass'][0]) < TOL)
    ok_(RELDIFF(airmass[1], test_data['airmass'][1]) < TOL)
    # test errors - YEAR
    datetime = [2051, 6, 5, 12, 31, 0]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_YEAR_ERROR'
    # test MONTH
    datetime = [2013, 13, 5, 12, 31, 0]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_MONTH_ERROR'
    # test DAY
    datetime = [2013, 6, 32, 12, 31, 0]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_DAY_ERROR'
    # test HOUR
    datetime = [2013, 6, 5, 25, 31, 0]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_HOUR_ERROR'
    # test MINUTE
    datetime = [2013, 6, 5, 12, 61, 0]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_MINUTE_ERROR'
    # test SECOND
    datetime = [2013, 6, 5, 12, 31, 61]
    try:
        solposAM(location, datetime, weather)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_SECOND_ERROR'


def test_spectrl2():
    """
    test spectrl2.dll
    """
    # test data
    test_data_jsonfile = 'test_spectrl2_data.json'
    with open(os.path.join(_DIRNAME, test_data_jsonfile), 'r') as filepath:
        test_data = json.load(filepath)
    units = 1
    location = [33.65, -84.43, -5.0]
    datetime = [1999, 7, 22, 9, 45, 37]
    weather = [1006.0, 27.0]
    orientation = [33.65, 135.0]
    atmospheric_conditions = [1.14, 0.65, -1.0, 0.2, 1.36]
    albedo = [0.3, 0.7, 0.8, 1.3, 2.5, 4.0] + ([0.2] * 6)
    # call test function
    (specdif, specdir, specetr, specglo,
     specx) = spectrl2(units, location, datetime, weather, orientation,
                       atmospheric_conditions, albedo)
    # convert OUTPUT to numpy arrays
    _specdif = np.ctypeslib.as_array(specdif)  # use ctypeslib
    _specdir = np.ctypeslib.as_array(specdir)
    _specetr = np.ctypeslib.as_array(specetr)
    _specglo = np.ctypeslib.as_array(specglo)
    _specx = np.ctypeslib.as_array(specx)
    # test OUTPUT are within TOL
    assert np.all(RELDIFF(_specdif, test_data['specdif']) < TOL)
    assert np.all(RELDIFF(_specdir, test_data['specdir']) < TOL)
    assert np.all(RELDIFF(_specetr, test_data['specetr']) < TOL)
    assert np.all(RELDIFF(_specglo, test_data['specglo']) < TOL)
    assert np.all(RELDIFF(_specx, test_data['specx']) < TOL)
    # raise a SPECTRL2_Error - UNITS
    try:
        spectrl2(3, location, datetime, weather, orientation,
                 atmospheric_conditions, albedo)
    except SPECTRL2_Error as err:
        assert err.args[0] == -1
    # raise a SPECTRL2_Error - TAU500
    try:
        spectrl2(units, location, datetime, weather, orientation,
                 [-1.0] * 5, albedo)
    except SPECTRL2_Error as err:
        assert err.args[0] == -2
    # now raise a SOLPOS_Error - YEAR
    datetime = [2051, 6, 5, 12, 31, 0]
    try:
        spectrl2(units, location, datetime, weather, orientation,
                 atmospheric_conditions, albedo)
    except SOLPOS_Error as err:
        assert err.args[0] == 'S_YEAR_ERROR'

if __name__ == '__main__':
    test_spectrl2()
