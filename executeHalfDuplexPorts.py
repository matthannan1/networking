"""
Script: executeHalfDuplexPortsCSV.py
By: Matt Hannan
Date: 12/16/2019

Cisco BCI can export in CSV format. In order to pull actionable data from this
report, I am writing a series of scripts to parse the files and return the
needed data. In the case of this script, I am looking for the ports that are
running in half duplex mode on User Access switches. This condition is due to
the switch ports being hard-coded to 100/Full, but the attached phones are
expecting Auto/Auto. This script produces a sorted list of these ports based
on the syslog output.

12/23/2019: Fully modularized now.
"""


import buildList
import userInput
import enableLogging
import turnNetmiko


# Build the switch port list.
# This calls the tkinter GUI to select the CSV file.
# Then the buildList gets called to clean up and deliver the list.
# The value that is passed is the column number that should searched.
portList = buildList.fromCSV(0)

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

# Loop through list of ports for SHOW
for port in portList:
    command = "show interface " + port + " stats"
    print(net_connect.send_command(command))
print("Config complete.")

"""
# Loop through list of ports for CONF T
for port in portList:
    interface = "interface " + port
    command_set = [interface, "speed 100", "duplex full"]
    output = net_connect.send_config_set(command_set)
    print(output)
"""

# Save the config
# output = net_connect.send_command_expect('write mem')
# print(output)
print("Config complete.")

# Exit the switch
print(net_connect.send_command_timing('exit'))

# Exit the jump box
turnNetmiko.off(net_connect)
print("Session closed.")
net_connect.disconnect()
