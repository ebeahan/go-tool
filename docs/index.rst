.. go documentation master file, created by
   sphinx-quickstart on Wed Jun  1 15:01:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to go's documentation!
==============================

This project serves as handy command-line utility for jumping to different systems
via SSH.

Basic Usage
----------
.. code-block:: text

    $ go.py

This will print all entries in the current configdb and prompt for a selection.

Config Database
-----------

.. code-block:: text

    $ go.py -db /path/to/configdb

If no option is specified with the -db or --database argument, one is created by
default in $HOME/.go/.configdb. A specific sqlite database can be specified with
the -db or --database argument.

Contents:

.. toctree::
   :maxdepth: 2



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

