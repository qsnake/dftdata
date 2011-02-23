NIST DFT Atomic Reference Data
==============================

NIST publishes the data at:

http://physics.nist.gov/PhysRefData/DFTdata/

and it can be downloaded as text files from:

http://physics.nist.gov/PhysRefData/DFTdata/notation.html#retrieve_files

This forms the first commit of this git repository. To load the data as a
Python dictionary, do::

    ./parse.py

and it will be saved into ``dftdata.json``. Try the ``demo.py`` script for a
simple usage.
