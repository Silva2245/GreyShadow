import os
import sys
from colorama import *
from socket import *
import asyncio
import rsa
from Crypto.Cipher import AES
from hashlib import *
from base64 import *
from psutil import *

class Encryptor:
    def __init__(self, Role : str):
        try:
            self.puk = rsa.PublicKey(29450995197188579386169935469233050653169839464673186859906489967249918061175912687532634596436259559642032957875742515395767005859267145086439086255044861837100004778246707371334630969108106225053004586807244752131111975258156307597914768047327921281954887395939264493299298962898130400825676500138486905528821769902238319230054001943380329392016954719603516276113260634872766692830921352425473487488479564486923538522096340886743329843410642132416459013693817193209498245132647385420280382108800959242038268557338391030601461387796687896665518475269281984106306134830789167126281017010471119752278984352037580771277, 
                                         65537)
            self.pvk = rsa.PrivateKey(29450995197188579386169935469233050653169839464673186859906489967249918061175912687532634596436259559642032957875742515395767005859267145086439086255044861837100004778246707371334630969108106225053004586807244752131111975258156307597914768047327921281954887395939264493299298962898130400825676500138486905528821769902238319230054001943380329392016954719603516276113260634872766692830921352425473487488479564486923538522096340886743329843410642132416459013693817193209498245132647385420280382108800959242038268557338391030601461387796687896665518475269281984106306134830789167126281017010471119752278984352037580771277, 
                                          65537, 
                                          18013833307513334349665197265966951012145294791963156208953897139435436705987421395432094701203044092769130920692235141555986941679884382531012973001811622924485264683168248648661367121285190749309164927701225462470478579126271476362512952865483422379853267866298752711878720390416626565869242388990266600038825480109293721267861693905037835669170964239650713989156171832578859305066092013068078641706774503521546829910254171881797880840170793335727246833130021067444458939718669059603297202198563223553535961409700268322978054116881391042858493773130904265944984616721924989807008321649496698533898216674086552240361, 
                                          3131510684435561749335029146792961480908943039024200393287433191941661337750365929687773719441802979158579419882918776284367806184592411915267070288449524447568765249374776792864272053216154192219495842496124331921199557023665073405825846358052451264716327726291660230935296694837506522045457919653126259490987665854623957963439, 
                                          9404724481244095011079094543338680633811399499199871654935060877464592438747421009729942988895246074270558895821435929532706594163819358158240572689271366148414915791710754396922972799264135239827934227018703408983140097636004408531073880792943422983784121756310455935190250140141498520643)
            self.MinorKey = None
            self.MajorKey = None
            self.Tag = None
            self.r = Role
            if self.r == '1':
                self.InitHandshakeKeys()
            elif self.r == '2':
                self.DeployHandshakeKeys()
            else:
                print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def ValidateMinorKey(self, key : str):
            try:
                if len(key) == 12:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'The Minor Key is Valid' + Style.RESET_ALL + Fore.RESET)
                    return True
                else:
                    print(Fore.RED + Style.NORMAL + 'The Minor Key is Invalid Its Length is ' + str(len(key)) + ' Characters'+ Style.RESET_ALL + Fore.RESET)
                    return False
            except Exception as e:
                print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.ValidateMinorKey(): {e}' + Style.RESET_ALL + Fore.RESET)
    
    def ValidateMajorKey(self, key : str):
            try:
                if len(key) == 32:
                    print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'The Major Key is Valid' + Style.RESET_ALL + Fore.RESET)
                    return True
                else:
                    print(Fore.RED + Style.NORMAL + 'The Major Key is Invalid Its Length is ' + str(len(key)) + ' Characters' + Style.RESET_ALL + Fore.RESET)
                    return False
            except Exception as e:
                print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.ValidateMajorKey(): {e}' + Style.RESET_ALL + Fore.RESET)
        
    def InitHandshakeKeys(self):
        try:
            print(Fore.CYAN + Style.DIM + 'Enter The Major Key ' + Style.RESET_ALL + Fore.RESET, end='')
            MajorKey = str(input(' > ')).encode('utf-8')
            print(Fore.CYAN + Style.DIM + 'Enter The Minor Key ' + Style.RESET_ALL + Fore.RESET, end='')
            MinorKey = str(input(' > ')).encode('utf-8')
            vmj = self.ValidateMajorKey(MajorKey)
            vmn = self.ValidateMinorKey(MinorKey)
            if vmj == True and vmn == True:
                print(Fore.GREEN + Style.BRIGHT + 'The Keys Are Valid' + Style.RESET_ALL + Fore.RESET)
                self.MinorKey = rsa.encrypt(MinorKey, self.puk)
                self.MajorKey = rsa.encrypt(MajorKey, self.puk)
                print(Fore.RED + Style.DIM + 'Minor Key : ' + str(self.MinorKey) + Style.RESET_ALL + Fore.RESET)
                print(Fore.RED + Style.DIM + 'Major Key : ' + str(self.MajorKey) + Style.RESET_ALL + Fore.RESET)
            else:
                print(Fore.RED + Style.NORMAL + 'The Keys Are Invalid' + Style.RESET_ALL + Fore.RESET)
                sys.exit(0)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.InitHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def DeployHandshakeKeys(self, MinorCipher : bytes, MajorCipher : bytes):
        try:
            self.MinorKey = str(rsa.decrypt(MinorCipher, self.pvk).decode('utf-8'))
            self.MajorKey = str(rsa.decrypt(MajorCipher, self.pvk).decode('utf-8'))
            print(Fore.RED + Style.DIM + 'Minor Key : ' + str(self.MinorKey) + Style.RESET_ALL + Fore.RESET)
            print(Fore.RED + Style.DIM + 'Major Key : ' + str(self.MajorKey) + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.DeployHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
        

class PlayGround:
    def __init__(self):
        self.n = None
        
    def home(self):
        try:
            print(Fore.WHITE + Style.DIM + '*** Welcome to GreyShadow ***' + Style.RESET_ALL)
            print(Fore.MAGENTA + Style.NORMAL + 'Enter Your Name : ' + Style.RESET_ALL + Fore.RESET, end='')
            YourName = str(input(' > '))
            print(Fore.YELLOW + Style.DIM + 'Enter Other Person Name : ' + Style.RESET_ALL + Fore.RESET, end='')
            OtherName = str(input(' > '))
            print('1. Server')
            print('2. Client')
            print(Fore.LIGHTBLUE_EX + Style.DIM + 'Enter Your Role : ' + Style.RESET_ALL + Fore.RESET, end='')
            YourRole = str(input(' > '))
            e = Encryptor('1')
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in PlayGround.home() : {e}' + Style.RESET_ALL + Fore.RESET)
            
if __name__ == '__main__':
    pg = PlayGround()
    pg.home()