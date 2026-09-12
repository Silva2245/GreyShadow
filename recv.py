import os
import sys
from socket import *

try:
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    s.bind('192.168.100.21', 55)
    c, a = s.accept()
    fd = c.recv(2000000000)
    f = open('m.py', 'wb')
    f.write(fd)
    f.close()
    s.close()
except Exception as e:
    print('the problem was : ' + str(e))