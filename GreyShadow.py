import os
import sys
import threading
from concurrent.futures import ThreadPoolExecutor as Exec
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
            self.MinorKey : bytes = None
            self.MajorKey : bytes = None
            self.MinorCipher = None
            self.MajorCipher = None
            self.AesCipher = None
            self.r = Role
            if self.r == '1':
                self.InitHandshakeKeys()
            elif self.r == '2':
                print()
            else:
                print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
    
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
            finally:
                sys.exit(0)
    
    def CraftMajorKey(self, key : bytes):
            try:
                h = md5(key)
                c = h.hexdigest()
                return c.encode('utf-8')
            except Exception as e:
                print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.CraftMajorKey(): {e}' + Style.RESET_ALL + Fore.RESET)
            finally:
                sys.exit(0)
        
    def InitHandshakeKeys(self):
        try:
            print(Fore.CYAN + Style.DIM + 'Enter The Major Key ' + Style.RESET_ALL + Fore.RESET, end='')
            MajorKey = str(input(' > ')).encode('utf-8')
            print(Fore.CYAN + Style.DIM + 'Enter The Minor Key ' + Style.RESET_ALL + Fore.RESET, end='')
            self.MinorKey = str(input(' > ')).encode('utf-8')
            vmn = self.ValidateMinorKey(self.MinorKey)
            self.MajorKey = self.CraftMajorKey(MajorKey)
            if vmn == True:
                print(Fore.GREEN + Style.BRIGHT + 'The Keys Are Valid' + Style.RESET_ALL + Fore.RESET)
                self.MinorCipher = rsa.encrypt(self.MinorKey, self.puk)
                self.MajorCipher = rsa.encrypt(self.MajorKey, self.puk)
                print(Fore.RED + Style.DIM + 'Minor Key Cipher : ' + str(self.MinorCipher) + Style.RESET_ALL + Fore.RESET)
                print(Fore.RED + Style.DIM + 'Major Key Cipher : ' + str(self.MajorCipher) + Style.RESET_ALL + Fore.RESET)
                self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
                print(Fore.LIGHTGREEN_EX + Style.DIM + 'AES Verfication : ' + str(self.AesCipher) + Fore.RESET + Style.RESET_ALL)
            else:
                print(Fore.RED + Style.NORMAL + 'The Keys Are Invalid' + Style.RESET_ALL + Fore.RESET)
                sys.exit(0)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.InitHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
    
    def DeployHandshakeKeys(self):
        try:
            self.MinorKey = rsa.decrypt(self.MinorCipher, self.pvk)
            self.MajorKey = rsa.decrypt(self.MajorCipher, self.pvk)
            print(Fore.RED + Style.DIM + 'Minor Key : ' + str(self.MinorKey) + Style.RESET_ALL + Fore.RESET)
            print(Fore.RED + Style.DIM + 'Major Key : ' + str(self.MajorKey) + Style.RESET_ALL + Fore.RESET)
            self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.DeployHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
    
    def AESEncryptLayer(self, data : bytes):
        cd = None
        tag = None
        aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
        try:
            cd, tag = aes.encrypt_and_digest(data)
            return (cd, tag)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESEncryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
            
    def AESDecryptLayer(self, data : bytes, tag : bytes):
        try:
            aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
            return aes.decrypt_and_verify(data, tag)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESDecryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
        
class Connector:
    def __init__(self, Role : str):
        try:
            self.r = Role
            self.ip = None
            self.p = None
            self.c = None
            self.en : Encryptor = None
            self.ConnectionOpen = False
            if self.r == '1':
                self.en = Encryptor(self.r)
                self.c = self.ServerConnect()
                if self.ConnectionOpen == True:
                    self.Handshake()
            elif self.r == '2':
                self.en = Encryptor(self.r)
                print(Fore.CYAN + Style.DIM + 'Enter The IP Address Of The Other ' + Style.RESET_ALL + Fore.RESET, end='')
                self.ip = str(input(' > '))
                print(Fore.CYAN + Style.DIM + 'Enter The Port Number ' + Style.RESET_ALL + Fore.RESET, end='')
                self.p = int(input(' > '))
                self.c = self.ClientConnect()
                if self.ConnectionOpen == True:
                    self.Handshake()
            else:
                print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Connector.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
        
    def Handshake(self):
        try:
            if self.r == '1':
                if self.ConnectionOpen == True:
                    self.c.send(self.en.MinorCipher)
                    self.c.send(self.en.MajorCipher)
                    recv = self.c.recv(6000)
                    tag = self.c.recv(6000)
                    print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Recieved Data : ' + str(recv) + Style.RESET_ALL + Fore.RESET)
                    hndshake = self.en.AESDecryptLayer(recv, tag)
                    print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Handshake : ' + str(hndshake.decode('utf-8')) + Style.RESET_ALL + Fore.RESET)
                    print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Tag : ' + str(tag) + Style.RESET_ALL + Fore.RESET)
                else:
                    print()
            elif self.r == '2':
                if self.ConnectionOpen == True:
                    MinorCipher = self.c.recv(6000)
                    self.en.MinorCipher = MinorCipher
                    print(Fore.RED + Style.DIM + 'Minor Key Cipher : ' + str(self.en.MinorCipher) + Style.RESET_ALL + Fore.RESET)
                    MajorCipher = self.c.recv(6000)
                    self.en.MajorCipher = MajorCipher
                    print(Fore.RED + Style.DIM + 'Major Key Cipher : ' + str(self.en.MajorCipher) + Style.RESET_ALL + Fore.RESET)
                    self.en.DeployHandshakeKeys()
                    msg = 'Welcome To GreyShadow Arena'
                    print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Created Message : ' + msg + Style.RESET_ALL + Fore.RESET)
                    hndshake = self.en.AESEncryptLayer(str(msg).encode('utf-8'))
                    self.c.send(hndshake[0])
                    self.c.send(hndshake[1])
                    print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Handshake : ' + str(hndshake) + Style.RESET_ALL + Fore.RESET)
                else:
                    print()
            else:
                print(Fore.RED + Style.NORMAL + 'Invalid Role Selected' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Connector.Handshake() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
    
    def ServerConnect(self):
        try:
            s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            myip = str(net_if_addrs()['Wi-Fi'][1].address)
            print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'Your Ip Address is : ' + myip + Style.RESET_ALL + Fore.RESET)
            s.bind((myip, 55))
            s.listen(60)
            print(Fore.MAGENTA + Style.DIM + 'Server Is Listening For Connections...' + Style.RESET_ALL + Fore.RESET)
            c, a = s.accept()
            self.ConnectionOpen = True
            print(Fore.GREEN + Style.BRIGHT + f'Connection Established With {self.ip} : {self.p}' + Style.RESET_ALL + Fore.RESET)
            return c
        except Exception as e:
            self.ConnectionOpen = False
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Connctor.ServerConnect() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)
            
    def ClientConnect(self):
        try:
            c = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c.connect((self.ip, self.p))
            print(Fore.GREEN + Style.BRIGHT + f'Connection Established With {self.ip} : {self.p}' + Style.RESET_ALL + Fore.RESET)
            self.ConnectionOpen = True
            return c
        except Exception as e:
            self.ConnectionOpen = False
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Connector.ClientConnect() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            sys.exit(0)

class ChatPool:
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        try:
            self.cipher = encryptor
            self.yn = YourName
            self.on = OtherName
            self.c = connector.c
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def Pool(self):
        try:
            print(Fore.MAGENTA + Style.NORMAL + self.yn  + Style.RESET_ALL + Fore.RESET, end='')
            Msg = str(input(' > '))
            while Msg != 'exit' or Msg != 'disc' or Msg != 'bye':
                snd = threading.Thread(target=self.SendTxtMsg, args=(Msg,))
                rcv = threading.Thread(target=self.RecvTxtMsg)
                snd.run()
                rcv.run()
                snd.join()
                rcv.join()
                print(Fore.MAGENTA + Style.NORMAL + self.yn + Style.RESET_ALL + Fore.RESET, end='')
                Msg = str(input(' > '))
            print(Fore.BLUE + Style.DIM + 'Disconnecting...' + Style.RESET_ALL + Fore.RESET)
            self.c.close()
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.Pool() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
    
    def SendTxtMsg(self, message : str):
        try:
            cipherdata = self.cipher.AESEncryptLayer(message.encode('utf-8'))
            self.c.send(cipherdata[0])
            tag = rsa.encrypt(cipherdata[1], self.cipher.puk)
            self.c.send(tag)
            print(Fore.MAGENTA + Style.NORMAL + self.yn + ' > ' + Style.RESET_ALL + Fore.RESET + message)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def RecvTxtMsg(self):
        try:
            msgdata = self.c.recv(20000)
            ctag = self.c.recv(20000)
            tag = rsa.decrypt(ctag, self.cipher.pvk)
            res = self.cipher.AESDecryptLayer(msgdata, tag)
            print(Fore.YELLOW + Style.DIM + self.on + ' > ' + Style.RESET_ALL + Fore.RESET + res.decode('utf-8'))
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.RecvTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
            
    def SendFile(self, filepath : str):
        try:
            print()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendFile() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
                    
    def RecvFile(self):
        res = (None, None)
        try:
            print()
            return res
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened ChatPool.RecvFile() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass

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
            c = Connector(YourRole)
            e = c.en
            cp = ChatPool(c, e, YourName, OtherName)
            if c.ConnectionOpen == True:
                asyncio.run(cp.Pool())
            else:
                print(Fore.RED + Style.DIM + 'The Connection Was Not Inialized....' + Fore.RESET + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in PlayGround.home() : {e}' + Style.RESET_ALL + Fore.RESET)
            
if __name__ == '__main__':
    pg = PlayGround()
    pg.home()