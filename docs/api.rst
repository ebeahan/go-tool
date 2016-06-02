.. _api:

API Documentation
=================

.. module:: go

For normal use, all you will have to do to get started is::

    import go

This will import the following:

* The class "class:`ConfigDatabase` and its subclasses
* The :func:`print_welcome_banner` function for printing the welcome banner.
* The :func:`open_ssh_connection` function for generating SSH connections to hosts.
* The :func:`search_config` function for searching the sqlite config database.

Configuration Database Class: ConfigDatabase
--------------------------------------------

.. autoclass:: ConfigDatabase
    :members:

Printing the welcome banner
---------------------------

.. autofunction:: print_welcome_banner()

Opening an SSH connection
-------------------------

.. autofunction:: open_ssh_connection()

Searching through the ConfigDB:

.. autofunction:: search_config()
