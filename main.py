import os
import sys
from socket import *
import asyncio
from rsa import *
from Crypto.Cipher import AES
from base64 import *
from hashlib import *
from colorama import *

class Connector:
    def __init__(self, role : str, IpAddress : str, Port : int):
        self.r = role
        self.ip = IpAddress
        self.port = Port
        if self.r == '1':
            self.ServerConnect()
        elif self.r == '2':
            self.ClientConnect()
        else:
            print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL)
        
    def ServerConnect(self):
        try:
            print()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL)
    
    def ClientConnect(self):
        try:
            print()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL)

class PlayGround:
    def __init__(self):
        self.n = None
        
    def home(self):
        print(Fore.WHITE + Style.DIM + '*** Welcome to GreyShadow ***' + Style.RESET_ALL)
        print('1. Server')
        print('2. Client')
        role = str(input(Fore.CYAN + Style.DIM + 'What Is Your Role (Server/Client) ? '))
        
if __name__ == '__main__':
    try:
        pg = PlayGround()
        pg.home()
    except Exception as e:
        print(Fore.RED +Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL)