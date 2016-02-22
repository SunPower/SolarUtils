#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Tests for solar utilities.

Usage
=====
This code uses nose. Enter the following in a CMD shell::

    $ nosetests --verbose

2013 SunPower Corp.
Confidential & Proprietary
Do Not Distribute
"""

import json
import numpy as np
import os
from nose.tools import ok_

from solar_utils import *
from solar_utils.exceptions import SOLPOS_Error, SPECTRL2_Error

_DIRNAME = os.path.dirname(__file__)
TOL = 1E-3

RELDIFF = lambda x, x0: np.abs(x - x0) / x0


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
