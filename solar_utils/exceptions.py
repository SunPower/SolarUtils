# -*- coding: utf-8 -*-
"""
Exceptions for solar utilities.

2013 SunPower Corp.
"""


class SolarUtilsException(Exception):
    """
    Base exception class for solar_utils.
    """
    pass


class SOLPOS_Error(SolarUtilsException):
    """
    SOLPOS Errors
    """
    S_CODE = ['S_YEAR_ERROR',
              'S_MONTH_ERROR',
              'S_DAY_ERROR',
              'S_DOY_ERROR',
              'S_HOUR_ERROR',
              'S_MINUTE_ERROR',
              'S_SECOND_ERROR',
              'S_TZONE_ERROR',
              'S_INTRVL_ERROR',
              'S_LAT_ERROR',
              'S_LON_ERROR',
              'S_TEMP_ERROR',
              'S_PRESS_ERROR',
              'S_TILT_ERROR',
              'S_ASPECT_ERROR',
              'S_SBWID_ERROR',
              'S_SBRAD_ERROR',
              'S_SBSKY_ERROR']

    def __init__(self, code, data):
        self.args = SOLPOS_Error.S_CODE[code], data
        self.message = str(self)

    def __str__(self):
        if self.args[0] == 'S_YEAR_ERROR':
            errmsg = "S_decode ==> Please fix the year: %d [1950-2050]\n"
            message = errmsg % self.args[1]['datetime'][0]
        if self.args[0] == 'S_MONTH_ERROR':
            errmsg = "S_decode ==> Please fix the month: %d\n"
            message = errmsg % self.args[1]['datetime'][1]
        if self.args[0] == 'S_DAY_ERROR':
            errmsg = "S_decode ==> Please fix the day-of-month: %d\n"
            message = errmsg % self.args[1]['datetime'][2]
        if self.args[0] == 'S_HOUR_ERROR':
            errmsg = "S_decode ==> Please fix the hour: %d\n"
            message = errmsg % self.args[1]['datetime'][3]
        if self.args[0] == 'S_MINUTE_ERROR':
            errmsg = "S_decode ==> Please fix the minute: %d\n"
            message = errmsg % self.args[1]['datetime'][4]
        if self.args[0] == 'S_SECOND_ERROR':
            errmsg = "S_decode ==> Please fix the second: %d\n"
            message = errmsg % self.args[1]['datetime'][5]
        if self.args[0] == 'S_DOY_ERROR':
            errmsg = "S_decode ==> Please fix the day-of-year: %d\n"
            message = errmsg % self.args[1]['settings'][0]
        if self.args[0] == 'S_INTRVL_ERROR':
            errmsg = "S_decode ==> Please fix the interval: %d\n"
            message = errmsg % self.args[1]['settings'][1]
        if self.args[0] == 'S_LAT_ERROR':
            errmsg = "S_decode ==> Please fix the latitude: %f\n"
            message = errmsg % self.args[1]['location'][0]
        if self.args[0] == 'S_LON_ERROR':
            errmsg = "S_decode ==> Please fix the longitude: %f\n"
            message = errmsg % self.args[1]['location'][1]
        if self.args[0] == 'S_TZONE_ERROR':
            errmsg = "S_decode ==> Please fix the time zone: %f\n"
            message = errmsg % self.args[1]['location'][2]
        if self.args[0] == 'S_PRESS_ERROR':
            errmsg = "S_decode ==> Please fix the pressure: %f\n"
            message = errmsg % self.args[1]['weather'][0]
        if self.args[0] == 'S_TEMP_ERROR':
            errmsg = "S_decode ==> Please fix the temperature: %f\n"
            message = errmsg % self.args[1]['weather'][1]
        if self.args[0] == 'S_TILT_ERROR':
            errmsg = "S_decode ==> Please fix the tilt: %f\n"
            message = errmsg % self.args[1]['orientation'][0]
        if self.args[0] == 'S_ASPECT_ERROR':
            errmsg = "S_decode ==> Please fix the aspect: %f\n"
            message = errmsg % self.args[1]['orientation'][1]
        if self.args[0] == 'S_SBWID_ERROR':
            errmsg = "S_decode ==> Please fix the shadowband width: %f\n"
            message = errmsg % self.args[1]['shadowband'][0]
        if self.args[0] == 'S_SBRAD_ERROR':
            errmsg = "S_decode ==> Please fix the shadowband radius: %f\n"
            message = errmsg % self.args[1]['shadowband'][1]
        if self.args[0] == 'S_SBSKY_ERROR':
            errmsg = "S_decode ==> Please fix the shadowband sky factor: %f\n"
            message = errmsg % self.args[1]['shadowband'][2]
        return message


class SPECTRL2_Error(SolarUtilsException):
    """
    SPECTRL2 Errors
    """
    def __init__(self, code, data):
        self.args = code, data
        self.message = str(self)

    def __str__(self):
        if self.args[0] == -1:
            errmsg = "*** S_spectral2 -> units should be 1 to 3, not %d\n"
            message = errmsg % self.args[1]['units']
        if self.args[0] == -2:
            errmsg = "*** S_spectral2 -> tau500 should not be %f\n"
            message = errmsg % self.args[1]['tau500']
        if self.args[0] == -3:
            errmsg = "*** S_spectral2 -> watvap should not be %f\n"
            message = errmsg % self.args[1]['watvap']
        if self.args[0] == -4:
            errmsg = "*** S_spectral2 -> assym should not be %f\n"
            message = errmsg % self.args[1]['assym']
        return message
