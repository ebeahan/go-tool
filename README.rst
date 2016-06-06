GO 0.1
==========

|travis|

Users a menu driven interface to open SSH sessions.

Basic Usage
------------

.. code::

    $ go.py

This will print all entries in the current configdb database and prompt for an entry.

Config Database
----------------

.. code::

    $ go.py -db /path/to/configdb-file

The configuration database saves a database file in $HOME/.go by default. A
specific sqlite database can be specified with the ``-db`` argument.

.. |travis| image:: https://travis-ci.org/ebeahan/go.svg?branch=master
.. _travis https://travis-ci.org/ebeahan/go
