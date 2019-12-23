import logging
import os


def on():
    if os.path.exists("netmiko-runthrough.log"):
        os.remove("netmiko-runthrough.log")
        print("Old log file deleted.")
    logging.basicConfig(filename="netmiko-runthrough.log",
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S')
    logger = logging.getLogger("netmiko")

    return logger
