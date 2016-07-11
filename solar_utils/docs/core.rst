.. _core:

Core
====
.. automodule:: solar_utils.core
.. document private functions

Libraries
---------
Solar Utils depends on two libraries that must be compiled in the same folder as
``core.py``. The library extension depends on the system platform. Windows uses
dynamically linked libraries, ``.dll``, Linux uses shared objects, ``.so`` and
Mac OS X (*aka Darwin*) uses dynamic libraries, ``.dylib``. Also both Linux and
Darwin libraries have ``lib`` prefixed to the library name.

solposAM
++++++++
A library compiled from
`NREL's SOLPOS 2.0 <http://rredc.nrel.gov/solar/codesandalgorithms/solpos/>`_
that exports functions called by :func:`solposAM`.

.. data:: SOLPOSAMDLL

spectrl2
++++++++
A library compiled from
`NREL's SPECTRL2 V.2 <http://rredc.nrel.gov/solar/models/spectral/>`_
that imports :data:`SOLPOSAMDLL` and exports functions called by
:func:`spectrl2`.

.. data:: SPECTRL2DLL

solposAM
--------
.. autofunction:: solposAM

spectrl2
--------
.. autofunction:: spectrl2

_int2bits
---------
.. autofunction:: _int2bits

Used to decipher the return value error codes from SOLPOS and SPECTRL2.
