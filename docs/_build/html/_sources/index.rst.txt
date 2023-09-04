.. quoter documentation master file, created by
   sphinx-quickstart on Mon Aug 28 13:26:18 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the documentation for the quoter-model package
=========================================================

.. toctree::
   :maxdepth: 2

*Table of contents to be added later*

*Please also excuse some docstrings being badly formatted - it is in the TODO!*

See below for the function references inside the `quoter` package (listed as quoter-model on pypi).
The package's repository can be found at https://github.com/jsm8989/quoter/

quoter_model module
-------------------

.. automodule:: quoter.quoter_model
   :members:

real_networks.read_networks module
----------------------------------

.. automodule:: quoter.real_networks.read_networks
   :members:

CrossEntropy module
-------------------
This should not be needed, but is included as a local solution in case of issues with installing the remote package.

.. automodule:: quoter.CrossEntropy
   :members:

Examples using the quoter-model package
---------------------------------------

Possible ways of simulating the quoter model on networks can be found in `quoter.examples``

These are intended to be run from any directory once the package has been installed, and will write results to an `ouput/` directory relative to this one.

After running simulations, summary statistics can be processed using scripts inside `quoter.examples.processing`

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
