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
        self.p = Port
        self.ConnectionOpen = False
        self.AllPorts = [x for x in range(1, 65536)]
        self.AllAddresses = self.GenerateAddress()
        if self.r == '1':
            self.ServerConnect()
        elif self.r == '2':
            self.ClientConnect()
        else:
            print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL)
            
    def GenerateAddress(self):
        try:
            nums = [str(x) for x in range(0, 256)]
            for n1 in nums:
                for n2 in nums:
                    for n3 in nums:
                        for n4 in nums:
                            res = n1 + '.' + n2 + '.' + n3 + '.' + n4
                            return res
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL)
        
    def ServerConnect(self):
        try:
            s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            s.bind((self.ip, self.p))
            s.listen(10)
            print(Fore.MAGENTA + Style.DIM + 'Server Is Listening For Connections...' + Style.RESET_ALL)
            c, a = s.accept()
            self.ConnectionOpen = True
            print(Fore.GREEN + Style.BRIGHT + f'Connection Established With {self.ip} : {self.p}' + Style.RESET_ALL)
            return c
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL)
    
    def ClientConnect(self):
        try:
            c = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c.connect((self.ip, self.p))
            print(Fore.GREEN + Style.BRIGHT + f'Connection Established With {self.ip} : {self.p}' + Style.RESET_ALL)
            self.ConnectionOpen = True
            return c
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