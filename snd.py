import os
import sys
from threading import *
from socket import *

try:
    s1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    s2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    s1.bind(('192.168.100.21', 55))
    s1.listen(60)
    print('waiting...')
    c1, a = s1.accept()
    print(f'connection 1 established with {str(a)}')
    s2.connect(('192.168.100.21', 58))
    print(f'connection 2 established with {str(s2.getsockname())}')
    msg = str(input('enter message : '))
    def snd(msg : bytes):
        c1.send(msg)
        
    def rcv():
        print(s2.recv(20000).decode('utf-8'))
    
    def pool(msg : bytes):
        t1 = Thread(target=snd, args=(msg,))
        t2 = Thread(target=rcv)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
    
    while msg != 'bye':
        pool(msg.encode('utf-8'))
        msg = str(input('enter message : '))
        
except Exception as e:
    print(f'the error was {e}')
finally:
    pass