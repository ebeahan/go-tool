#!/usr/bin/python
# -*- coding: utf-8 -*-
""" Title: go.py
    Author: Eric Beahan

    Stores a sqllite database of host entries that allows the user to connect
    quickly using a menu-driven interface, destination hostname, or integer ID
    values for each entry in the config db.

    Sample usage:
    > go.py
    - Prints all entries in the current configdb and prompts user for an entry.

    > go.py -m
    - Prints the configuration entries and exits

    > go.py -db
    - Allows user to manually specify a configdb file to load. Default location
     is ~/.go/.configdb

    > go.py -d <hostname>
    - User supplies a hostname of a device. Go automatically opens an SSH
      connection to this host. The supplied hostname must already exist in
      the config database.

    > go.py -i <integer value>
    - If the user knows the integer ID value for a config DB entry, he/she can
      use that as a short-hand shortcut for opening a connection. For example,
      if host.example.com is entry #3 in the config db:
      > go.py -i 3

    > go.py -c <config file>
    - Allows a user to specify a CSV file with the following format to be
      inserted into the the config DB in bulk:

      # hostname, port, username, ipaddress

    > go.py -e
    - Places the user into DB entry mode where they can manually entry
      additional host entries.

    > go.py -r
    - Places the user into a DB maintenance mode where they can manually remove
      entries from the DB.

"""

import sys
import socket
import argparse
from subprocess import call
import os
import sqlite3


class ConfigDatabase(object):
    """ Defines an instance of the GO configuration database
    """

    def __init__(self, dbname=None):
        """ init
        :param dbname: sqlite database
        :return: n/a
        """
        if dbname is None:
            dbhome = '%s/.go' % (os.path.expanduser('~'))
            self.dbname = '%s/.configdb' % dbhome
        else:
            self.dbname = dbname
        self.dbh = self._sqllite3_connect()

    def _sqllite3_connect(self):
        """ Connects to sqlite database
        :return: database handler for sqlite db
        """
        dbh = sqlite3.connect(self.dbname)
        dbh.text_factory = str
        cur = dbh.cursor()
        sql = """ \
        CREATE TABLE IF NOT EXISTS config
        (
            id INTEGER PRIMARY KEY, hostname TEXT, port INT,
            username TEXT, ip TEXT
        )
        """
        cur.execute(sql)
        dbh.commit()
        return dbh

    def _insert_config_entries(self, hostname, port, username, ipaddress):
        """ Insert entries into db

        :param hostname: str
        :param port: int
        :param username: str
        :param ip: str
        :return: n/a
        """
        if not hostname and port and username and ipaddress:
            raise Exception('[*] Error: Missing required parameter')
        print "Adding entry: ", hostname, port, username, ipaddress
        cur = self.dbh.cursor()
        sql = """ \
        INSERT INTO config (
            hostname, port, username, ip
        )
        VALUES ( ?, ?, ?, ? )
        """
        try:
            params = [
                hostname, port, username, ipaddress
            ]
            cur.execute(sql, params)
        except:
            raise Exception('[*] Error: SQL INSERT failed')
        self.dbh.commit()

    def _remove_config_entires(self, hostname):
        """ Remove entries from db
        :param hostname: str
        :return: n/a
        """
        if not hostname:
            raise Exception('[*] Error: missing required parameter')
        print "Removing entry for", hostname
        cur = self.dbh.cursor()
        sql = """\
        DELETE FROM config WHERE hostname = ?
        """
        try:
            cur.execute(sql, (hostname,))
        except:
            raise Exception('[*] Error: missing required parameter')
        self.dbh.commit()

    def _lookup_config_entries(self, hostname):
        """ Lookup entries in db by hostname
        :param hostname: str
        :return: list of results
        """
        if not hostname:
            raise Exception('[*] Error: missing required parameters')
        print "[*] Looking up entry for", hostname
        cur = self.dbh.cursor()
        sql = """\
        SELECT * FROM config WHERE hostname LIKE ?
        """
        # Create a wildcard search string
        hostnamewild = '%' + hostname + '%'
        try:
            cur.execute(sql, (hostnamewild,))
        except:
            raise Exception('[*] Error: failed to complete SQL query')
        return cur.fetchall()

    def _lookup_config_entries_by_id(self, integer):
        """ Lookup config entries by id
        :param integer: int
        :return: list of results
        """
        if integer < 0 or integer == 0:
            raise Exception('[*] Error: invalid ID number')
        print "[*] Looking up ID #", integer
        cur = self.dbh.cursor()
        sql = """\
        SELECT * FROM config WHERE id = ?
        """
        try:
            cur.execute(sql, (integer,))
        except:
            raise Exception('[*] Error: failed to complete SQL query')
        return cur.fetchall()

    def update_with_config(self, config):
        """ Bulk load from config csv file
        :param config: str
        :return: none
        """
        with open(config, 'r') as file:
            config_data = file.read()
        recs = 0
        errs = 0
        for line in config_data.split('\n'):
            if not line:
                continue
            try:
                hostname, port, username, ipaddress = line.split(',')
                # print hostname, port, username, ip
                self._insert_config_entries(hostname, port,
                                            username, ipaddress)
                recs += 1
            except:
                errs += 1
                continue
        print '[*] Inserted %d records' % recs
        if errs > 0:
            raise Exception('[*] Errors on insert %d' % errs)

    def update_new_entry(self, hostname, port, username, ip):
        """ Public method for updating new entries
        :param hostname: str
        :param port: int
        :param username: str
        :param ip: str
        :return: none
        """
        self._insert_config_entries(hostname, port, username, ip)

    def remove_entry(self, hostname):
        """ Public method for removing entries
        :param hostname: str
        :return: none
        """
        self._remove_config_entires(hostname)

    def lookup_entry(self, hostname):
        """ Public method for looking up entries
        :param hostname: str
        :return: list of results
        """
        return self._lookup_config_entries(hostname)

    def lookup_id(self, integer):
        """ Public method for lookup up by ID
        :param integer: int
        :return: list of results
        """
        return self._lookup_config_entries_by_id(integer)

    def print_config_db(self):
        """ Print the contents of the DB as a menu
        :return: none
        """
        cur = self.dbh.cursor()
        sql = """\
        SELECT * FROM config
        """
        cur.execute(sql)
        for row in cur.fetchall():
            print str(row[0]) + ") " + row[1]
        print "\n"


def print_welcome_banner():
    """ Prints welcome banner
    :return: none
    """
    print ('\n'
           '\n'
           '############################################\n'
           ' GO - INTERACTIVE SHELL MANAGEMENT CONSOLE\n'
           ' Make a selection or use Ctrl+C to exit.\n'
           '############################################\n')


def parse_args():
    """Create the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dest", dest="destination",
                        help="Specify a destination host")
    parser.add_argument("-e", "--entry", dest="entry", action="store_true",
                        help="Enter DB entry mode")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true",
                        help="Delete DB records")
    parser.add_argument("-c", "--config", dest="configuration",
                        help="Specify a configuration file")
    parser.add_argument("-i", "--integer", dest="integer",
                        help="Specify a destination host by it's integer")
    parser.add_argument("-m", "--menu", dest="menu", action="store_true",
                        help="Print the current configuration and exit.")
    parser.add_argument("-db", "--database", dest="database",
                        help="Specify a configuration sqllite3 database file.")
    return parser.parse_args()


def hostname_resolves(hostname):
    """Checks to see if hostname is DNS resolvable"""
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0


def open_ssh_connection(current_host):
    """Opens a SSH connection to currentHost"""
    host = current_host[1]
    if not hostname_resolves(host):
        host = current_host[4]
    port = "-p" + str(current_host[2])
    username = "-l" + current_host[3]

    # make system call
    try:
        call(["ssh", username, host, port])
    except KeyboardInterrupt:
        sys.exit(0)


def search_config(configdb, dest):
    """
    :param db: ConfigDatabase class
    :param dest: str format
    :return: none
    """
    i = 0
    for item in configdb:
        if dest in item:
            return configdb[i].split(",")
        else:
            i += 1
    print "Specified host not listed in the configuration"
    print "The program will now exit gracefully"
    sys.exit(0)


def entry_mode(configdb):
    """
    :param configdb: ConfigDatabase class
    :return: none
    """
    repeat = True
    print "Entering entry mode...."
    print "Please enter a hostname, port, username, and IP address for \
           each entry."
    while repeat:
        hostname = raw_input("Hostname? ")
        port = raw_input("Port? ")
        username = raw_input("Username? ")
        ipaddress = raw_input("IP address? ")
        print "Adding entry ", hostname, port, username, ipaddress
        configdb.update_new_entry(hostname, port, username, ipaddress)
        repeat_prompt = raw_input("Continue? [Y/n] ")
        if repeat_prompt != "Y":
            repeat = False


def remove_mode(configdb):
    """
    :param configdb: ConfigDatabase class
    :return: none
    """
    repeat = True
    print "Entering removal mode..."
    print "Please enter the hostname of the record you want to delete."
    while repeat:
        hostname = raw_input("> ")
        configdb.remove_entry(hostname)
        repeat_prompt = raw_input("Continue [Y/n] ")
        if repeat_prompt != "Y":
            repeat = False


def main(args):
    """ Main function call
    :param args: ParseArgs() object
    :return: None
    """

    if args.database is None:
        sqldb = ConfigDatabase()
    else:
        sqldb = ConfigDatabase(args.database)

    if args.entry:
        entry_mode(sqldb)

    if args.remove:
        remove_mode(sqldb)

    if args.configuration is not None:
        txt_config = args.configuration
        sqldb.update_with_config(txt_config)
        sys.exit(0)

    if args.menu:
        print_welcome_banner()
        sqldb.print_config_db()
        sys.exit(0)

    # Print Destination
    if args.destination is not None:
        entry = sqldb.lookup_entry(args.destination)[0]
        print "[*] Attempting to connect to", entry[1], "on port", \
            str(entry[2]), "using username", entry[3], "..."
        open_ssh_connection(entry)
        sys.exit(0)

    # Connect to host based on config integer value
    if args.integer is not None:
        entry = sqldb.lookup_id(args.integer)[0]
        print "[*] Attempting to connect to", entry[1], "on port", \
            str(entry[2]), "using username", entry[3], "..."
        open_ssh_connection(entry)
        sys.exit(0)

    # print the welcome banner
    print_welcome_banner()

    # print interactive menu
    sqldb.print_config_db()

    # User enters selection. -1 to adjust for index 0
    selection = raw_input("Please enter your selection: ")

    # Open SSH connection and pass user selection
    entry = sqldb.lookup_id(selection)[0]
    print "[*] Attempting to connect to", entry[1], "on port", \
        str(entry[2]), "using username", entry[3], "..."
    open_ssh_connection(entry)
    sys.exit(0)

if __name__ == "__main__":
    try:
        main(parse_args())
    except KeyboardInterrupt:
        sys.exit(0)
