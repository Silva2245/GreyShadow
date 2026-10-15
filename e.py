import os
import sys
from subprocess import *
from argparse import *
from threading import *

def home():
    try:
        t1 = Thread(target=Tunnel1, daemon=True)
        t2 = Thread(target=Tunnel2, daemon=True)
        t1.start()
        t2.start()
        t1.join()
        t2.join()        
    except Exception as e:
        print(f'the error in home was {str(e)}')
        
def Tunnel1():
    try:
        p1 = run(['python', 'ServerMessageTunnel1.py'])
        print(p1.stdout.decode())
    except Exception as e:
        print(f'the error was in Tunnel 1 : {str(e)}')

def Tunnel2():
    try:
        p2 = run(['python', 'ServerMessageTunnel2.py'])
        print(p2.stdout.decode())
    except Exception as e:
        print(f'the error in Tunnel 2 was : {str(e)}')

if __name__ == '__main__':
    try:
        home()
    except Exception as e:
        print(f'the error was {str(e)}')