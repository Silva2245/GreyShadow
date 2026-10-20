import os
import sys
from threading import *
from time import *
from Crypto.Cipher import AES
from hashlib import *
from socket import *
from colorama import *
from psutil import *
import rsa
from argparse import *

class Encryptor:
    def __init__(self):
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
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def AESEncryptLayer(self, data : bytes) -> tuple:
        cd = None
        tag = None
        try:
            aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
            cd, tag = aes.encrypt_and_digest(data)
            return (cd, tag)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESEncryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
            
    def AESDecryptLayer(self, data : bytes, tag : bytes) -> bytes:
        try:
            aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
            return aes.decrypt_and_verify(data, tag)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESDecryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
class ServerEncryptor(Encryptor):
    def __init__(self):
        try:
            super().__init__()
            self.InitHandshakeKeys()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerEncryptor.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def ValidateMinorKey(self, key : str) -> bool:
        try:
            if len(key) == 12:
                print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'The Minor Key is Valid' + Style.RESET_ALL + Fore.RESET)
                return True
            else:
                print(Fore.RED + Style.NORMAL + 'The Minor Key is Invalid Its Length is ' + str(len(key)) + ' Characters'+ Style.RESET_ALL + Fore.RESET)
                return False
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerEncryptor.ValidateMinorKey(): {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def CraftMajorKey(self, key : bytes) -> bytes:
        try:
            h = md5(key)
            c = h.hexdigest()
            return c.encode('utf-8')
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In ServerEncryptor.CraftMajorKey(): {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
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
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerEncryptor.InitHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
    
class ClientEncryptor(Encryptor):
    def __init__(self):
        super().__init__()
    
    def DeployHandshakeKeys(self):
        try:
            self.MinorKey = rsa.decrypt(self.MinorCipher, self.pvk)
            self.MajorKey = rsa.decrypt(self.MajorCipher, self.pvk)
            print(Fore.RED + Style.DIM + 'Minor Key : ' + str(self.MinorKey) + Style.RESET_ALL + Fore.RESET)
            print(Fore.RED + Style.DIM + 'Major Key : ' + str(self.MajorKey) + Style.RESET_ALL + Fore.RESET)
            self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientEncryptor.DeployHandshakeKeys() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
class Connector:
    def __init__(self):
        try:
            self.c : tuple = None
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Connector.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
    
class ServerConnector(Connector):
    def __init__(self):
        super().__init__()
        try:
            self.en : ServerEncryptor = ServerEncryptor()
            self.c = self.ServerConnect()
            print(Fore.LIGHTBLUE_EX + Style.DIM + str(self.c) + Style.RESET_ALL + Fore.RESET)
            self.Handshake()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerConnector.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Handshake(self):
        try:
            self.c[0].send(self.en.MinorCipher)
            self.c[0].send(self.en.MajorCipher)
            recv = self.c[0].recv(6000)
            tag = self.c[0].recv(6000)
            print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Recieved Data : ' + str(recv) + Style.RESET_ALL + Fore.RESET)
            hndshake = self.en.AESDecryptLayer(recv, tag)
            print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Handshake : ' + str(hndshake.decode('utf-8')) + Style.RESET_ALL + Fore.RESET)
            print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Tag : ' + str(tag) + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerConnector.Handshake() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def ServerConnect(self) -> list[socket]:
        try:
            s1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            myip = str(net_if_addrs()['Wi-Fi'][1].address)
            print(Fore.LIGHTBLUE_EX + Style.BRIGHT + 'Your Ip Address is : ' + myip + Style.RESET_ALL + Fore.RESET)
            s1.bind((myip, 111))
            s1.listen(60)
            print(Fore.MAGENTA + Style.DIM + 'Server Is Listening For Connections...' + Style.RESET_ALL + Fore.RESET)
            c1, a1 = s1.accept()
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 1 Connection Established With {str(a1)}' + Style.RESET_ALL + Fore.RESET)
            s2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            ep = (myip, 112)
            s2.bind(ep)
            s2.listen(60)
            c2, a2 = s2.accept()
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 2 Connection Established With {str(a2)}' + Style.RESET_ALL + Fore.RESET)
            s3 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            s3.bind((myip, 113))
            s3.listen(60)
            c3, a3 = s3.accept()
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 3 Connection Established With {str(a3)}' + Style.RESET_ALL + Fore.RESET)
            s4 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            s4.bind((myip, 114))
            s4.listen(60)
            c4, a4 = s4.accept()
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 4 Connection Established With {str(a4)}' + Style.RESET_ALL + Fore.RESET)
            return [c1, c2, c3, c4]
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerConnctor.ServerConnect() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            self.Handshake()
    
class ClientConnector(Connector):
    def __init__(self):
        super().__init__()
        try:
            self.ip = None
            self.p = None
            self.en : ClientEncryptor = ClientEncryptor()
            print(Fore.CYAN + Style.DIM + 'Enter The IP Address Of The Other ' + Style.RESET_ALL + Fore.RESET, end='')
            self.ip = str(input(' > '))
            print(Fore.CYAN + Style.DIM + 'Enter The Port Number ' + Style.RESET_ALL + Fore.RESET, end='')
            self.p = int(input(' > '))
            self.c = self.ClientConnect()
            self.Handshake()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientConnector.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Handshake(self):
        try:
            MinorCipher = self.c[0].recv(6000)
            MajorCipher = self.c[0].recv(6000)
            self.en.MinorCipher = MinorCipher
            self.en.MajorCipher = MajorCipher
            print(Fore.RED + Style.DIM + 'Minor Key Cipher : ' + str(self.en.MinorCipher) + Style.RESET_ALL + Fore.RESET)
            print(Fore.RED + Style.DIM + 'Major Key Cipher : ' + str(self.en.MajorCipher) + Style.RESET_ALL + Fore.RESET)
            self.en.DeployHandshakeKeys()
            msg = 'Welcome To GreyShadow Arena'
            print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Created Message : ' + msg + Style.RESET_ALL + Fore.RESET)
            hndshake = self.en.AESEncryptLayer(str(msg).encode('utf-8'))
            self.c[0].send(hndshake[0])
            self.c[0].send(hndshake[1])
            print(Fore.LIGHTCYAN_EX + Style.NORMAL + 'Handshake : ' + str(hndshake) + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientConnector.Handshake() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
            
    def ClientConnect(self) -> list[socket]:
        try:
            c1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c1.connect((self.ip, self.p))
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 1 Connection Established With {self.ip} : {self.p}' + Style.RESET_ALL + Fore.RESET)
            c2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c2.connect((self.ip, 112))
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 2 Connection Established With {self.ip} : {'112'}' + Style.RESET_ALL + Fore.RESET)
            c3 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c3.connect((self.ip, 113))
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 3 Connection Established With {self.ip} : {'113'}' + Style.RESET_ALL + Fore.RESET)
            c4 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c4.connect((self.ip, 114))
            print(Fore.GREEN + Style.BRIGHT + f'Tunnel LayLine 4 Connection Established With {self.ip} : {'114'}' + Style.RESET_ALL + Fore.RESET)
            return [c1, c2, c3, c4]
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientConnector.ClientConnect() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            self.Handshake()
            
class ChatPool:
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        try:
            self.cipher = encryptor
            self.yn = YourName
            self.on = OtherName
            self.c = connector.c
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.__init__() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def SendTxtMsg(self, message : str, Connection : socket):
        try:
            cipherdata = self.cipher.AESEncryptLayer(message.encode('utf-8'))
            tag = rsa.encrypt(cipherdata[1], self.cipher.puk)
            Connection.send(cipherdata[0])
            Connection.send(tag)
            print(Fore.MAGENTA + Style.NORMAL + self.yn + ' > ' + Style.RESET_ALL + Fore.RESET + message)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
            
    def RecvTxtMsg(self, Connection : socket) -> str:
        try:
            msgdata = Connection.recv(50000)
            ctag = Connection.recv(50000)
            tag = rsa.decrypt(ctag, self.cipher.pvk)
            return self.cipher.AESDecryptLayer(msgdata, tag).decode('utf-8')
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.RecvTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def SendFile(self, FilePath : str, Connection : socket):
        try:
            fileciphername = rsa.encrypt(FilePath.encode('utf-8'), self.cipher.puk)
            Connection.send(fileciphername)
            f = open(FilePath, 'rb')
            filedata = f.read()
            f.close()
            cipherdata : tuple = self.cipher.AESEncryptLayer(filedata)
            Connection.send(cipherdata[0])
            ctag : bytes = rsa.encrypt(cipherdata[1], self.cipher.puk)
            Connection.send(ctag)
            print(Fore.GREEN + Style.BRIGHT + f'File {FilePath} Sent..' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendFile() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass 
            
    def RecvFile(self, Connection : socket):
        try:
            print(Fore.YELLOW + Style.DIM + 'Recieving File...' + Style.RESET_ALL + Fore.RESET)
            fileciphername : bytes = Connection.recv(4000000000)
            filename : str = rsa.decrypt(fileciphername, self.cipher.pvk).decode('utf-8')
            cipherfile : bytes = Connection.recv(4000000000)
            ctag : bytes = Connection.recv(4000000000)
            print(Fore.YELLOW + Style.DIM + 'Data Recieved...' + Style.RESET_ALL + Fore.RESET)
            tag : bytes = rsa.decrypt(ctag, self.cipher.pvk)
            filedata : bytes = self.cipher.AESDecryptLayer(cipherfile, tag)
            f = open(f'Files/{filename}', 'wb')
            f.write(filedata)
            f.close()
            print(Fore.YELLOW + Style.DIM + 'Cipher File Recieved...' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.RecvFile() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
class ServerChatPool(ChatPool):
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        super().__init__(connector, encryptor, YourName, OtherName)
        
    def Pool(self):
        try:
            t1 = Thread(target=self.Tunnel1, daemon=True)
            t2 = Thread(target=self.Tunnel2, daemon=True)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerChatPool.Pool() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Tunnel1(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 1 ...' + Style.RESET_ALL + Fore.RESET)
        try:
            print(Fore.MAGENTA + Style.NORMAL + self.yn  + Style.RESET_ALL + Fore.RESET, end='')
            Msg = str(input(' > '))
            while Msg not in ['bye', 'disc', 'exit']:
                self.SendTxtMsg(Msg, self.c[0])
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerChatPool.Tunnel1() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Tunnel2(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 2 ...' + Style.RESET_ALL + Fore.RESET)
        try:
            Msg = self.RecvTxtMsg(self.c[1])
            while Msg not in ['bye', 'disc', 'exit']:
                print(Fore.YELLOW + Style.DIM + self.on + ' > ' + Style.RESET_ALL + Fore.RESET + Msg)
                Msg = self.RecvTxtMsg(self.c[1])
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerChatPool.Tunnel2() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Tunnel3(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 3 ...' + Style.RESET_ALL, + Fore.RESET)
        try:
            pass
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.Tunnel3() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
            
    def Tunnel4(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 4 ...' + Style.RESET_ALL, + Fore.RESET)
        try:
            pass
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.Tunnel4() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
class ClientChatPool(ChatPool):
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        super().__init__(connector, encryptor, YourName, OtherName)
    
    def Pool(self):
        try:
            t1 = Thread(target=self.Tunnel1, daemon=True)
            t2 = Thread(target=self.Tunnel2, daemon=True)
            t1.start()
            t2.start()
            t1.join()
            t2.join()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientChatPool.Pool() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
    
    def Tunnel1(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 1 ...' + Style.RESET_ALL + Fore.RESET)
        try:
            Msg = self.RecvTxtMsg(self.c[0])
            while Msg not in ['bye', 'disc', 'exit']:
                print(Fore.YELLOW + Style.DIM + self.on + ' > ' + Style.RESET_ALL + Fore.RESET + Msg)
                Msg = self.RecvTxtMsg(self.c[0])
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ClientChatPool.Tunnel1() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
    def Tunnel2(self):
        print(Fore.CYAN + Style.DIM + 'Starting Tunnel 2 ...' + Style.RESET_ALL + Fore.RESET)
        try:
            print(Fore.MAGENTA + Style.NORMAL + self.yn  + Style.RESET_ALL + Fore.RESET, end='')
            Msg = str(input(' > '))
            while Msg not in ['bye', 'disc', 'exit']:
                self.SendTxtMsg(Msg, self.c[1])
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ServerChatPool.Tunnel2() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
        
class PlayGround:
    def __init__(self, yourname : str, othername : str):
        self.YourName = yourname
        self.OtherName = othername
    
    def home(self, role : str):
        try:
            if role in ['1', 'server', 'Server', 's']:
                c = ServerConnector()
                en = c.en
                cp = ServerChatPool(c, en, self.YourName, self.OtherName)
                cp.Pool()
            elif role in ['2', 'client', 'Client', 'c']:
                c = ClientConnector()
                en = c.en
                cp = ClientChatPool(c, en, self.YourName, self.OtherName)
                cp.Pool()
            else:
                print(Fore.RED + Style.DIM + f'{role} is an Invalid Role !' + Fore.RESET + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in PlayGround.home() : {e}' + Style.RESET_ALL + Fore.RESET)
        finally:
            pass
    
p = ArgumentParser()
p.add_argument('-r', type=str, metavar='role whether it was client or server, for server you can type : [1, server, Server, s], for client you can type : [2, client, Client, c]')
p.add_argument('-yn', type=str, metavar='YourName')
p.add_argument('-on', type=str, metavar='OtherName')
a = p.parse_args()
role = str(a.r)
YourName = str(a.yn)
OtherName = str(a.on)

if __name__ == '__main__':
    pg = PlayGround(YourName, OtherName)
    pg.home(role)