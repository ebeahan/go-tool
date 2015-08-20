#!/usr/bin/python

import sys
import socket
import argparse
from subprocess import call
import os
import sqlite3

class configDatabase:

    def __init__(self, dbName=None):
        if dbName == None:
            dbhome = '%s/.go' % (os.path.expanduser('~'))
            self.dbname = '%s/.configdb' % (dbhome)
        else:
            self.dbname = dbName
        self.dbh = self._sqllite3_connect()

    def _sqllite3_connect(self):
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

    def _insert_config_entries(self, hostname, port, username, ip):
        if not hostname and port and username and ip:
            raise Exception('[*] Error: Missing required parameter')
        print "Adding entry: ", hostname, port, username, ip
        cur = self.dbh.cursor()
        sql = """ \
        INSERT INTO config (
            hostname, port, username, ip
        )
        VALUES ( ?, ?, ?, ? )
        """

        try:
            params = [
                hostname, port, username, ip
            ]
            cur.execute(sql, params)
        except:
            raise Exception('[*] Error: SQL INSERT failed')
        self.dbh.commit()

    def _remove_config_entires(self, hostname):
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
        if not hostname:
            raise Exception('[*] Error: missing required parameters')
        print "[*] Looking up entry for", hostname
        cur = self.dbh.cursor()
        sql = """\
        SELECT * FROM config WHERE hostname = ?
        """
        try:
            cur.execute(sql, (hostname,))
        except:
            raise Exception('[*] Error: failed to complete SQL query')
        return cur.fetchall()

    def _lookup_config_entries_by_id(self, id):
        if id < 0 or id == 0:
            raise Exception('[*] Error: invalid ID number')
        print "[*] Looking up ID #", id
        cur = self.dbh.cursor()
        sql = """\
        SELECT * FROM config WHERE id = ?
        """
        try:
            cur.execute(sql, (id,))
        except:
            raise Exception('[*] Error: failed to complete SQL query')
        return cur.fetchall()

    def updateWithConfig(self, config):
        with open(config, 'r') as f:
            configData = f.read()
        recs = 0
        errs = 0
        for line in configData.split('\n'):
            if not line:
                continue
            try:
                hostname, port, username, ip = line.split(',')
                # print hostname, port, username, ip
                self._insert_config_entries(hostname, port, username, ip)
                recs += 1
            except:
                errs += 1
                continue
        print '[*] Inserted %d records' % (recs)
        if errs > 0:
            raise Exception('[*] Errors on insert %d' % (errs))

    def updateNewEntry(self, hostname, port, username, ip):
        self._insert_config_entries(hostname, port, username, ip)

    def removeEntry(self, hostname):
        self._remove_config_entires(hostname)

    def lookupEntry(self, hostname):
        return self._lookup_config_entries(hostname)

    def lookupId(self, id):
        return self._lookup_config_entries_by_id(id)

    def printConfigDb(self):
        cur = self.dbh.cursor()
        i = 0 # Counter
        sql = """\
        SELECT * FROM config
        """
        cur.execute(sql)
        for row in cur.fetchall():
            print str(row[0]) + ") " + row[1]
        print "\n"

def printWelcomeBanner():
    print ('\n'
           '\n'
           '############################################\n'
           ' GO - INTERACTIVE SHELL MANAGEMENT CONSOLE\n'
           ' Make a selection or use Ctrl+C to exit.\n'
           '############################################\n')

def parseArgs():
    """Create the arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--dest", dest="destination", help="Specify a destination host")
    parser.add_argument("-e", "--entry", dest="entry", action="store_true", help="Enter DB entry mode")
    parser.add_argument("-r", "--remove", dest="remove", action="store_true", help="Delete DB records")
    parser.add_argument("-c", "--config", dest="configuration", help="Specify a configuration file")
    parser.add_argument("-i", "--integer", dest="integer", help="Specify a destination host by it's integer")
    parser.add_argument("-m", "--menu", dest="menu", action="store_true", help="Print the current configuration \
                        and exit.")
    parser.add_argument("-db", "--database", dest="database", help="Specify a configuration \
                         sqllite3 database file.")
    return parser.parse_args()

def hostnameResolves(hostname):
    """Checks to see if hostname is DNS resolvable"""
    try:
        socket.gethostbyname(hostname)
        return 1
    except socket.error:
        return 0

def openSSHConnection(currentHost):
    """Opens a SSH connection to currentHost"""
    host = currentHost[1]
    if not hostnameResolves(host):
        host = currentHost[4]
    
    port = "-p" + str(currentHost[2])
    username = "-l" + currentHost[3]

    # make system call
    try:
        call(["ssh", username, host, port])
    except KeyboardInterrupt:
        sys.exit(0)

def searchConfig(DB, dest):
    i = 0
    for item in DB:
        if dest in item:
            return DB[i].split(",")
        else:
            i += 1
    print "Specified host not listed in the configuration"
    print "The program will now exit gracefully"
    sys.exit(0)

def entryMode(configdb):
    repeat = True
    print "Entering entry mode...."
    print "Please enter a hostname, port, username, and IP address for each entry."
    while repeat:
        hostname = raw_input("Hostname? ")
        port = raw_input("Port? ")
        username = raw_input("Username? ")
        ipaddress = raw_input("IP address? ")
        print "Adding entry ", hostname, port, username, ipaddress
        configdb.updateNewEntry(hostname, port, username, ipaddress)
        repeatPrompt = raw_input("Continue? [Y/n] ")
        if repeatPrompt != "Y":
            repeat = False

def removeMode(configdb):
    repeat = True
    print "Entering removal mode..."
    print "Please enter the hostname of the record you want to delete."
    while repeat:
        hostname = raw_input("> ")
        configdb.removeEntry(hostname)
        repeatPrompt = raw_input("Continue [Y/n] ")
        if repeatPrompt != "Y":
            repeat = False

def main(args):

    if args.database == None:
        sqlDB = configDatabase()
    else:
        sqlDB = configDatabase(args.database)

    # for testing
    #host = raw_input("hostname> ")
    #configLookup(sqlDB, host)

    if args.entry:
        entryMode(sqlDB)

    if args.remove:
        removeMode(sqlDB)

    if args.configuration != None:
        txtConfig = args.configuration
        sqlDB.updateWithConfig(txtConfig)
        sys.exit(0)

    if args.menu:
        printWelcomeBanner()
        sqlDB.printConfigDb()
        sys.exit(0)

    # Print Destination
    if args.destination != None:
      entry = sqlDB.lookupEntry(args.destination)[0]
      print "[*] Attempting to connect to", entry[1], "on port", str(entry[2]), "using username", entry[3], "..."
      openSSHConnection(entry)
      sys.exit(0)

    # Connect to host based on config integer value
    if args.integer != None:
        entry = sqlDB.lookupId(args.integer)[0]
        print "[*] Attempting to connect to", entry[1], "on port", str(entry[2]), "using username", entry[3], "..."
        openSSHConnection(entry)
        sys.exit(0)

    # print the welcome banner
    printWelcomeBanner()

    # print interactive menu
    sqlDB.printConfigDb()

    # User enters selection. -1 to adjust for index 0
    selection = raw_input("Please enter your selection: ")


    # Open SSH connection and pass user selection
    entry = sqlDB.lookupId(selection)[0]
    print "[*] Attempting to connect to", entry[1], "on port", str(entry[2]), "using username", entry[3], "..."
    openSSHConnection(entry)
    sys.exit(0)
    

if __name__ == "__main__":
    try:
        main(parseArgs())
    except KeyboardInterrupt:
        sys.exit(0)