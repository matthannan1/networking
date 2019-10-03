"""

My version of this guy's ssh2-python tutorial.
https://www.youtube.com/watch?v=j0p8ESkZ82E

"""

import socket
import time
import getpass
from ssh2.session import Session


host = "192.168.2.176"
port = 22
user = input("User name: ")
password = getpass.getpass()

# Create socket, then connect
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

# Start the session and perform three-way handshake
session = Session()
session.handshake(sock)
session.userauth_password(user, password)

# Open a communications channel
channel = session.open_session()

# Create the shell and run the commands
channel.shell()
channel.write("conf t\n")
channel.write("int Gi3/0\n")
channel.write("switchport\n")
channel.write("switchport mode access\n")
channel.write("switchport access vlan 2\n")
channel.write("end\n")
channel.write("wr mem\n")
channel.write("sh int status | i Gi3/0\n")
time.sleep(5)

# Read the channel and print the data
size, data = channel.read()
print(data.decode())

# Close the channel
channel.close()
print("Exit status: {0}".format(channel.get_exit_status()))
