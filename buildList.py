
"""
buildListCSV.py is a reusable module that builds a cleaned up, deduped, and
sorted list from the raw output of a Cisco BCI csv file.

file return list

Matt Hannan
12/3/2019
"""


import whichFile
import csv


def fromCSV(column):
    # Import csv file
    with open(whichFile.selectCSV()) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # Build the initial list
        halfDuplexList = []
        for row in csv_reader:
            halfDuplexList.append([t for t in row[column].split()
                                   if t.startswith('Gi')])

    # Flatten the list
    flattenedList = [y for x in halfDuplexList for y in x]

    # Dedup the list
    dedupedList = []
    [dedupedList.append(x) for x in flattenedList if x not in dedupedList]

    # Sort the list
    dedupedList.sort()

    # Give me some counts
    print("\n*** Raw list contains", len(flattenedList), "elements.")
    print("*** Deduped list contains", len(dedupedList), "elements.\n")

    # Return the list
    return dedupedList
