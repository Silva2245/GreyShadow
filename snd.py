import os
import sys
from socket import *

try:
    f = open('m.py', 'rb')
    fd = f.read()
    f.close()
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    ep = ('192.168.100.25', 55)
    s.connect(ep)
    s.send(fd)
    s.close()
    print('sent...')
except Exception as e:
    print('the error was : ' + str(e))