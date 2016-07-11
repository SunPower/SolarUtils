.. image:: https://travis-ci.org/SunPower/SolarUtils.svg?branch=master
    :target: https://travis-ci.org/SunPower/SolarUtils

SolarUtils is set of Python wrappers around the publicly available
`NREL <http://www.nrel.gov/>`_
`SOLPOS <http://rredc.nrel.gov/solar/codesandalgorithms/solpos/>`_ and
`SPECTRL2 <http://rredc.nrel.gov/solar/models/spectral/>`_ C-language computer
programs that calculate solar position and spectral decomposition. Please read
the `NREL disclaimer and license <http://www.nrel.gov/disclaimer.html>`_. Usage
of this software implies acceptance of the terms.

Installation
============
Use ``pip`` to install
`SolarUtils from the PyPI <https://pypi.python.org/pypi/SolarUtils>`_::

    pip install SolarUtils

You can also download a source distribution from PyPI or clone the repository
and use Python ``distutils``::

    python setup.py install

Requirements
============
SolarUtils has no requirements for usage however for installation, testing and
to build the documentaiton you will need the following pacakges:

* NumPy
* PyTest
* Sphinx

Usage
=====
See `SOLPOS Documentation <http://rredc.nrel.gov/solar/codesandalgorithms/solpos/aboutsolpos.html>`_
and
`SPECTRL2 Documentation <http://rredc.nrel.gov/solar/models/spectral/spectrl2/documentation.html>`_
for more detail.

Examples
--------

    >>> from solar_utils import *
    >>> import pandas as pd
    >>> location = [35.56836, -119.2022, -8.0]
    >>> datetime = [2013, 6, 5, 12, 31, 0]
    >>> weather = [1015.62055, 40.0]
    >>> (angles, airmass) = solposAM(location, datetime, weather)
    >>> zenith, azimuth = angles
    >>> zenith
    15.074043273925781
    >>> azimuth
    213.29042053222656]
    >>> am, amp = airmass
    >>> am
    1.0352272987365723
    >>> amp
    1.0379053354263306]

    >>> units = 1
    >>> location = [33.65, -84.43, -5.0]
    >>> datetime = [1999, 7, 22, 9, 45, 37]
    >>> weather = [1006.0, 27.0]
    >>> orientation = [33.65, 135.0]
    >>> atmospheric_conditions = [1.14, 0.65, -1.0, 0.2, 1.36]
    >>> albedo = [0.3, 0.7, 0.8, 1.3, 2.5, 4.0] + ([0.2] * 6)
    >>> specdif, specdir, specetr, specglo, specx = spectrl2(
    ...     units, location, datetime, weather, orientation,
    ...     atmospheric_conditions, albedo
    ... )
    >>> spec = pd.DataFrame(
    ...     {'DIF': specdif, 'DIR': specdir, 'ETR': specetr, 'GLO': specglo},
    ...     index=specx
    ... )
    >>> f = spec.plot()
    >>> f.set_title('Solar Spectrum Example')
    >>> f.set_xlabel('Wavelength, $\lambda [\mu m]$')
    >>> f.set_ylabel('Spectral Irradiance, $I_{\lambda} [W/m^2/\mu m]$')
    >>> f.grid(True)
    >>> f.figure.show()
