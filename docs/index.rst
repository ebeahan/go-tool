.. go documentation master file, created by
   sphinx-quickstart on Wed Jun  1 15:01:39 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Go's documentation!
==============================

This project serves as handy command-line utility for jumping to different systems
via SSH. I created **Go** as a utility that I could use day-to-day for managing
the access details of various systems.

Features
----------

- Printing out an interactive menu of added devices
- Automatically opening a shell session with a device using hostname
- Interactive editor mode for adding new entries to the database
- Bulk uploading via a CSV file

Basic Usage
------------
Here's an example of basic usage::

    $ ./go.py
    
    ############################################
     GO - INTERACTIVE SHELL MANAGEMENT CONSOLE
     Make a selection or use Ctrl+C to exit.
    ############################################
        
      1) host1.example.com  
      2) host2.example.com  
      3) host3.example.com


      Please enter your selection: 

This will print all entries in the current configdb and prompt for a selection.

Advanced Usage
--------------

If you want to specify a specific entry instead of using the menu-driven interface,
you can specify an entry in two different ways. First you can use the beginning
portion of any existing entry in the configdb. For example if we had a FQDN of
test1.test.example.com, the following would all be valid options::

    $ go.py -d test1.test.example.com
    $ go.py -d test1.test.example
    $ go.py -d test1.test
    $ go.py -d test1
    
Alternatively, if there's a specific host which you know the database entry you want
to connect, you can specify that with the -i argument::

    $ ./go.py -i 3
    [*] Looking up ID # 3
    [*] Attempting to connect to host3.example.com on port 22 using username ebeahan ...

Contact Information
-------------------

Find my contact information at `my site <https://www.ericbeahan.info>`_.

Config Database
---------------

.. code-block:: text

    $ go.py -db /path/to/configdb

If no option is specified with the -db or --database argument, one is created by
default in $HOME/.go/.configdb. A specific sqlite database can be specified with
the -db or --database argument.

API Documentation
------------------

More information on the API can be found in :ref:`api`.


Contents:

.. toctree::
   :maxdepth: 2

   api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

