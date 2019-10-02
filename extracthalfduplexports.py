"""
Script: extractHalfDuplexPorts.py
By: Matt Hannan
Date: 10/1/2019

Cisco BCI produces reports in PDF format only. In order to pull actionalbale data from these
reports, I am writing a series of scripts to parse the PDF files and return the needed data.
In the case of this script, I am looking for the ports that are running in half duplex mode
on User Access switches. This condition is due to the switch ports being hard coded to 100/Full,
but the attached phones are expecting Auto/Auto. This script produces a sorted list of these
ports based on the syslog output.
"""

import PyPDF2
import pprint
import os
from tkinter import filedialog, Tk


def whichFile():
    """This function provides an easy GUI for the user to select the
        file to be parsed."""
    # Build the window
    root = Tk().withdraw()  # .withdraw() hides that second blank window
    # This sets to the users home directory
    init_dir = os.path.expanduser("~")
    # Fire up the GUI and get the users selection
    fileSelect = filedialog.askopenfilename(
        initialdir=init_dir,
        title="Select file",
        filetypes=(("PDF files", "*.pdf"), ("All Files","*.*"))
        )
    return fileSelect

# Setup and create object from PDF file
pdfFileObj = open(whichFile(), 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
pages = pdfReader.numPages
print("Reading",pages,"pages from PDF.")

# Create the first list, which is a list of lists
halfDuplexList = []

# Read PDF object
for page in range(pages):
    pageObj = pdfReader.getPage(page)
    halfDuplexList.append([t for t in pageObj.extractText().split() if t.startswith('GigabitEthernet' or 'FastEthernet')])

flattenedList = [y for x in halfDuplexList for y in x]
print("Flattened_list contains",len(flattenedList),"elements.")
dedupedList = []
[dedupedList.append(x) for x in flattenedList if x not in dedupedList]
print("dedupedList contains",len(dedupedList),"elements.")
dedupedList.sort()
pprint.pprint(dedupedList)
