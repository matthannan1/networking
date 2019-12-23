from netmiko import ConnectHandler
from netmiko import redispatch
from time import sleep


def on(jumpserver, ip_addr, rsa_pwd):
    # Connect to jump box
    net_connect = ConnectHandler(**jumpserver)
    # Connect to the target device
    ssh_command = "ssh " + ip_addr                       # for TACACS account
    # ssh_command = "ssh " + local_user + "@" + ip_addr  # for local account
    net_connect.write_channel(ssh_command)
    print(net_connect.find_prompt())
    sleep(10)
    net_connect.write_channel(rsa_pwd+"\n")
    net_connect.read_channel()
    redispatch(net_connect, device_type='cisco_ios')
    return net_connect


def off(net_connect):
    redispatch(net_connect, device_type='terminal_server')
