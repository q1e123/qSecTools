#!/usr/bin/env python3

import socket
import threading
import sys

LOCAL_HOST = "127.0.0.1"

open_ports = []
closed_ports = []

def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        open_ports.append(port_number)
    except:
        closed_ports.append(port_number)

def scan_ports(host_ip, delay,interval):

    threads = []
    NUMBER_OF_THREADS = 10000

    if interval <6:
        for i in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=TCP_connect, args=(host_ip, i+interval*NUMBER_OF_THREADS, delay, output))
            threads.append(t)
    else:

        NUMBER_OF_THREADS = 5536
        for i in range(NUMBER_OF_THREADS):
            t = threading.Thread(target=TCP_connect, args=(host_ip, i+interval*10000, delay, output))
            threads.append(t)

    for i in range(NUMBER_OF_THREADS):
        threads[i].start()

    for i in range(NUMBER_OF_THREADS):
        threads[i].join()

def error_message():
    print("USAGE: ./port_scanner {IP} {DELAY} ")
    print("IP : The IPv4 address of the host. If not provided it will use the local host")
    print("DELAY: The amount of time that will take until a socket is killed. If not provided it will use 10s")

def check_IP(ip_addr):
    try:
        socket.inet_aton(ip_addr)
        return True
    except socket.error:
        return False

def check_delay(delay):
    try:
        val = int(delay)
        if val   0
        return True
    except ValueError:
        return False

def main():
    host_ip = LOCAL_HOST
    delay = 10

    if len(sys.argv) >3:
        error_message()
        quit()
    elif len(sys.argv) == 3:
        if not (check_IP(sys.argv[1]) and check_delay(sys.argv[2])):
            error_message()
            quit()
    elif len(sys.argv) == 2:
        if not check_IP(sys.argv[1]) and not check_delay(sys.argv[1]):
            error_message()
            quit()
        elif check_IP(sys.argv[1]):
            host_ip = sys.argv[1]
        else:
            delay=sys.argv[1]

    report = open(host_ip,"w+")

    for i in range (0,7):
        scan_ports(host_ip, delay,i)
    open_ports.sort()
    closed_ports.sort()
    closed_ports.remove(0)
    report.write("OPEN PORTS\n")
    for port in open_ports:
        report.write(str(port)+"\n")

    report.write("-"*12+"\n")
    report.write("CLOSED PORTS\n")
    for port in closed_ports:
        report.write(str(port)+"\n")

main()
