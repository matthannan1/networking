#!/usr/bin/python
"""
    Created 02 Dec 2018 by Matt Hannan
    This is a fragile start to a Python2.7.5 build at automating the collection of switch info.
    "show interface status" is a good basic skeleton to build a switch port inventory from.
    At the end, not only do we have a csv file, but also a dictionary, to which additional info 
    can be added, like cdp or vdc info.
""" 


import csv
import subprocess
import pprint
import sys
import os
# import re


UID = raw_input("User ID to use: ")
HOST = raw_input("Switch name: ")
HOST = HOST.replace("\r","")
FILENAME = HOST + ".csv"
COMMAND = "show interface status"

"""
# Test this on Linux
if os.path.exists(FILENAME):
    try:
        os.remove(FILENAME)
    except PermissionError:
        print(FILENAME + " is open.")
        input("Press any key after you close the file.")
"""

if os.path.exists(FILENAME):
    os.remove(FILENAME)

with open(FILENAME, 'a+') as csvfile:
    print
    print COMMAND
    print "Logging into",HOST
    # Create the ssh Process
    sshProcess = subprocess.Popen(["ssh",
                                    "-l",
                                    "%s" % UID, HOST, COMMAND],
                                    shell=False,
                                    stdin=subprocess.PIPE,
                                    stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE)
    # Execute the ssh Process
    sshProcess.stdin.write(COMMAND)

    # make List from output
    raw_result = sshProcess.stdout.readlines()

    # clean the line ends
    raw_result = [x.replace("\r\n","") for x in raw_result]
    #print "Raw result"
    #pprint.pprint(raw_result)
    #wait = raw_input("Press a key")

    # a bunch of fun stuff to remove banner info
    x = None
    result = [x for x in raw_result if not x.startswith("*")]
    x = None
    result1 = [x for x in result if not x.startswith("C")]
    x = None
    result = []
    result2 = [x for x in result1 if not x.startswith("#")]
    result = [x for x in result2 if not x == ""]

    # Test for errors, which seems to be a bit late to the party
    if result == []:
        error = sshProcess.stderr.readlines()
        pprint >>sys.stderr, "ERROR: %s" % error
    else:
        #print "Banner removed, pre-processing"
        #pprint.pprint(result)
        #wait = raw_input("Press a key")

        # Clean up the results (whitespace, commas, etc)
        result = [x.rstrip() for x in result]
        result = [x[:10]+","+x[10:] for x in result]
        result = [x[:30]+","+x[30:] for x in result]
        result = [x[:44]+","+x[44:] for x in result]
        result = [x[:56]+","+x[56:] for x in result]
        result = [x[:65]+","+x[65:] for x in result]
        result = [x[:72]+","+x[72:] for x in result]
        result = [x.rstrip() for x in result]
        result = [x.replace("  ","") for x in result]
        result = [x.replace(" ,",",") for x in result]
        result = [x.replace(", ",",") for x in result]
        #print "Post cleaning"
        #pprint.pprint(result)
        #wait = raw_input("Press a key")

    # Convert List to Dict
    reader = csv.DictReader(result)
    raw_dict = []
    for line in reader:
        raw_dict.append(line)
    #pprint.pprint(raw_dict)

    # Save to file
    csv_columns = ['Port','Name','Status','Vlan','Duplex','Speed','Type']
    writer = csv.DictWriter(csvfile, lineterminator='\n',fieldnames=csv_columns)
    writer.writeheader()
    for data in raw_dict:
        writer.writerow(data)
    print FILENAME + " created."