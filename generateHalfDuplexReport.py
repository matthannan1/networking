"""
grab voice vlan from list of of half-duplex ports and generate report

import list from returnHalfDuplexPortsCSV.py
create csv file (name from selected list file name)
netmiko it up
loop through list
    sh run int {int} | i voice => "switchport voice vlan 2010"
    sh int status | i {int}    => "Gi1/0/23  [IR-OFF]   Teller  notconnect\
                                   1010     full    100 10/100/1000BaseTX"
    append int, "2010", "full", "100" to csv file

By Matt Hannan
On 12/13/2019

12/23/2019: Fully modularized now.
"""

import buildList
import userInput
import shortenInterfaceName
import enableLogging
import shintstatus
import turnNetmiko
from progress.bar import PixelBar
import os
import csv


# Build the switch port list.
# This calls the tkinter GUI to select the CSV file.
# Then the buildList gets called to clean up and deliver the list.
# The value that is passed is the column number that should searched.
portList = buildList.fromCSV(3)

# Get Linux jumpserver details and other user input
jumpserver = userInput.getJumpServer()
ip_addr = userInput.getTargetIP()
rsa_pwd = userInput.getRSAandToken()

# Enable logging
logger = enableLogging.on()

# Fire up Netmiko
# to make connection to Linux jumpbox
# to make connection to Cisco switch
net_connect = turnNetmiko.on(jumpserver, ip_addr, rsa_pwd)

# Get hostname
hostname = net_connect.find_prompt()[:-1]
print(hostname)

# Get "show interface status" output
intStatus = net_connect.send_command("sh int status")

# Convert output to nested list
intStatusList = shintstatus.listify(intStatus)

# Create the csv filename
filename = hostname + "_half-duplex-ports.csv"
# Check to see if it exists.
# If it does, delete the old one.
if os.path.exists(filename):
    os.remove(filename)
    print("Old report deleted.")

# Open the csv file and start building the sucker.
with open(filename, 'w', newline='') as csv_file:
    fieldnames = ['Port', 'Voice VLAN', 'Duplex', 'Speed']
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(fieldnames)
    # Start the progress bar
    with PixelBar('Processing...') as bar:
        # Loop through list of ports for SHOW
        for port in portList:
            # Get the voice vlan
            vvCommand = "sh run int " + port + " | i voice"
            try:
                voiceVLAN = net_connect.send_command(vvCommand).split()[3]
            except IndexError:
                voiceVLAN = "none"
            # Get the short port name
            shortPort = shortenInterfaceName.shortenInt(port)
            # Do the compare and write the matches to csv file
            for status in intStatusList:
                if shortPort == status[0]:
                    csv_writer.writerow([status[0], voiceVLAN,
                                         status[4], status[5]])
            bar.next()
print("Report complete.")

# Exit the Cisco switch
print(net_connect.send_command_timing('exit'))
# Exit the Linux jumpbox
turnNetmiko.off(net_connect)
print("Session closed.")
net_connect.disconnect()
