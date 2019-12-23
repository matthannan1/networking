import getpass


# Get the user and switch data
def getJumpServer():
    user = getpass.getuser()
    jump_pass = getpass.getpass("Jumpbox password: ")
    # local_user = input("Switch username: ")  # for local user accounts
    jumpserver = {
                'device_type': 'terminal_server',
                'ip': '70.38.139.106',
                'username': user,
                'password': jump_pass,
                'global_delay_factor': 5
            }
    return jumpserver


def getTargetIP():
    ip_addr = input("IP address of switch: ")
    return ip_addr


def getRSAandToken():
    rsa_pwd = getpass.getpass("PIN + Token: ")
    return rsa_pwd
