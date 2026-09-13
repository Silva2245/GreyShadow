import os
import sys
from socket import *

try:
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    ep = ('192.168.100.21', 55)
    s.bind(ep)
    s.listen(60)
    c, a = s.accept()
    fd = c.recv(2000000000000)
    f = open('m.py', 'wb')
    f.write(fd)
    f.close()
    s.close()
    print('file recived..')
except Exception as e:
    print('the problem was : ' + str(e))