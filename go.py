#!/usr/bin/python

import sys
import socket
import argparse
from subprocess import call
import re

def printWelcomeBanner():
	print """\
\n
############################################
 GO - INTERACTIVE SHELL MANAGEMENT CONSOLE
 Make a selection or use Ctrl+C to exit.
############################################
"""

def parseArgs():
	"""Create the arguments"""
	parser = argparse.ArgumentParser()
	parser.add_argument("-d", "--dest", dest="destination", help="Specify a destination host")
	parser.add_argument("-c", "--config", dest="configuration", help="Specify a configuration file")
	parser.add_argument("-i", "--integer", dest="integer", help="Specify a destionation host by it's integer")
	parser.add_argument("-m", "--menu", dest="menu", action="store_true", help="Print the current configuration and exit.")
	return parser.parse_args()

def readConfig(CONFIG):
	"""Read in the config file"""
	DB = []
	with open(CONFIG, 'r') as f:
		for line in f:
		    DB.append(line.rstrip())
	return DB

def printMenu(DB):
	"""Prints the menu to STDOUT"""
	i = 0

	for item in DB:
		split = DB[i].split(",")
		print str(i + 1) + ") " + split[0]
		i += 1
	print "\n"

def hostnameResolves(hostname):
	"""Checks to see if hostname is DNS resolvable"""
	try:
		socket.gethostbyname(hostname)
		return 1
	except socket.error:
		return 0

def openSSHConnection(currentHost):
	"""Opens a SSH connection to currentHost"""
	host = currentHost[0]
	if not hostnameResolves(host):
		host = currentHost[3]
    
	port = "-p" + currentHost[1]
	username = "-l" + currentHost[2]

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

def main(args):
	# Define global variables
	if args.configuration == None:
	  CONFIG = '/cygdrive/c/Users/EMB004/Documents/repos/go/config.txt'
	else:
	  CONFIG = args.configuration

	# Read in config
	DB = readConfig(CONFIG)

	if args.menu:
		printMenu(DB)
		sys.exit(0)

	# Print Destination
	if args.destination != None:
	  openSSHConnection(searchConfig(DB, args.destination))

	# Connect to host based on config integer value
	if args.integer != None:
		item = int(args.integer) - 1
		openSSHConnection(DB[item].split(","))

	# print the welcome banner
	printWelcomeBanner()

	# print interactive menu
	printMenu(DB)

	# User enters selection. -1 to adjust for index 0
	selection = raw_input("Please enter your selection: ")
    
	selection = int(selection) - 1

	# Open SSH connection and pass user selection
	openSSHConnection(DB[selection].split(","))
    

if __name__ == "__main__":
	try:
		main(parseArgs())
	except KeyboardInterrupt:
		sys.exit(0)
