import socket


def print_host_name():
    hostname = socket.gethostname()
    ipaddr = socket.gethostbyname(hostname)
    print("Your Computer Name is:" + hostname)
    print("Your Computer IP Address is:" + ipaddr)
