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
from bs4 import *

class Encryptor: #Father (base) class for encryption keys and algorithms
    def __init__(self):
        try:
            self.puk = rsa.PublicKey(24069254571803287360303537010569710573266678688850049975841408920798753355819885562289153473675601217607889143649261333299722589675048923764559191598795156091437512505468871810752514921729239771962279444599204329914559878139871014816930222086612423592622981377428697843885555629764656439950878687537312922293477018308137358470085667168176371508987355625803315419363690693039583765759373712517287107349016435229821399041176767335786418380317189181124142841191968861394204339171848451131806221657051030814305491460135640941839185140962665651142954538680510029607063429996669923762783753144371077073997674472327528923167, 
                                     65537)
            self.pvk = rsa.PrivateKey(24069254571803287360303537010569710573266678688850049975841408920798753355819885562289153473675601217607889143649261333299722589675048923764559191598795156091437512505468871810752514921729239771962279444599204329914559878139871014816930222086612423592622981377428697843885555629764656439950878687537312922293477018308137358470085667168176371508987355625803315419363690693039583765759373712517287107349016435229821399041176767335786418380317189181124142841191968861394204339171848451131806221657051030814305491460135640941839185140962665651142954538680510029607063429996669923762783753144371077073997674472327528923167, 
                                      65537, 
                                      21535880782397317050228712128458691400365972986793385118839195839094223080579249423792264988370898573314448502288005787926857087385067882884935020464191970307548473317487666113961834116533879960756459776185250205255960399381172413107862295999769075591617239192990851166022324741348699039963639439883362852150945696859660597549626994954171869372941009380363321880338655928778365864008717238311062512015508038752610031688750618096027395875497573346999192375355822151616870420240584595704098146536343060861647147404172518836641134109221269899771963912628793192168281262649464571825141451077459678694982971728554544356313, 
                                      3112900746338464314716668795158341406180113341817950194283714889640366198178536591322565001573516097595637879766873698957657933271550150477296623864447136601291902372056268808132810046627246488555615589239333269503759671230414130893949997669979128749493249722975537943159026220815242453455150310129256893116790547279414516291221, 
                                      7732098300954388350276392281385311982157911394063672360633759685507686117241385025897266707813672262583530024789296352026751448113948039234640140336904139477920194150484091232785812394880288898194444959753223195390130147959048393425771326232230525548952440964201396177178494061818021696227)
            self.MinorKey : bytes = None # AES-GCM nonce 12 bytes
            self.MajorKey : bytes = None # AES-GCM key 32 bytes
            self.MinorCipher = None 
            self.MajorCipher = None
            self.AesCipher = None
        except Exception as e:
            print(Red + f'The Following Error Heppened in Encryptor.__init__() : {e}' + Reset)
        finally:
            pass
        
    def AESEncryptLayer(self, data : bytes) -> tuple:
        cd = None
        tag = None
        try:
            if data == None:
                pass
            else:
                aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
                cd, tag = aes.encrypt_and_digest(data)
                return (cd, tag)
        except Exception as e:
            print(Red + f'The Following Error Heppened In Encryptor.AESEncryptLayer() : {e}' + Reset)
        finally:
            pass
            
    def AESDecryptLayer(self, data : bytes, tag : bytes) -> bytes:
        try:
            if data == None or tag == None:
                pass
            else:
                aes = AES.new(self.MajorKey, AES.MODE_GCM, self.MinorKey)
                return aes.decrypt_and_verify(data, tag)
        except Exception as e:
            print(Red + f'The Following Error Heppened In Encryptor.AESDecryptLayer() : {e}' + Reset)
        finally:
            pass
        
    def EncryptFile(self, FileName : str, FileData : bytes) -> list:
        try:
            if FileName == None or FileData == None:
                pass
            else:
                FileNameCipher = rsa.encrypt(FileName.encode('utf-8'), self.puk)
                FileCipher = self.AESEncryptLayer(FileData)
                FileDataCipher = FileCipher[0]
                TagCipher = FileCipher[1]
                return [FileNameCipher, FileDataCipher, TagCipher]
        except Exception as e:
            print(Red + f'The Following Error Heppened in Encryptor.EncryptFile() : {e}' + Reset)
        finally:
            pass
        
    def DecryptFile(self, FileCipherList : list) -> tuple:
        try:
            if FileCipherList == None:
                pass
            elif None in FileCipherList:
                pass
            else:
                FileName = rsa.decrypt(FileCipherList[0], self.pvk).decode('utf-8')
                FileData = self.AESDecryptLayer(FileCipherList[1], FileCipherList[2])
                return (FileName, FileData)
        except Exception as e:
            print(Red + f'The Following Error Heppened in Encryptor.DecryptFile() : {e}' + Reset)
        finally:
            pass
        
class ServerEncryptor(Encryptor):
    def __init__(self):
        try:
            super().__init__()
            self.InitHandshakeKeys()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerEncryptor.__init__() : {e}' + Reset)
        finally:
            pass
        
    def ValidateMinorKey(self, key : str) -> bool:
        try:
            if len(key) == 12:
                print(Blue + 'The Minor Key is Valid' + Reset)
                return True
            else:
                print(Red + 'The Minor Key is Invalid Its Length is ' + str(len(key)) + ' Characters'+ Reset)
                return False
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerEncryptor.ValidateMinorKey(): {e}' + Reset)
        finally:
            pass
        
    def CraftMajorKey(self, key : bytes) -> bytes:
        try:
            h = md5(key)
            c = h.hexdigest()
            return c.encode('utf-8')
        except Exception as e:
            print(Red + f'The Following Error Heppened In ServerEncryptor.CraftMajorKey(): {e}' + Reset)
        finally:
            pass
        
    def InitHandshakeKeys(self):
        try:
            vmn = self.ValidateMinorKey(MinorKey)
            self.MajorKey = self.CraftMajorKey(MajorKey)
            if vmn == True:
                self.MinorKey = MinorKey
                print(Green + 'The Keys Are Valid' + Reset)
                self.MinorCipher = rsa.encrypt(self.MinorKey, self.puk)
                self.MajorCipher = rsa.encrypt(self.MajorKey, self.puk)
                self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
            else:
                print(Red + 'The Keys Are Invalid' + Reset)
                sys.exit(0)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerEncryptor.InitHandshakeKeys() : {e}' + Reset)
        finally:
            pass
    
class ClientEncryptor(Encryptor):
    def __init__(self):
        super().__init__()
    
    def DeployHandshakeKeys(self):
        try:
            self.MinorKey = rsa.decrypt(self.MinorCipher, self.pvk)
            self.MajorKey = rsa.decrypt(self.MajorCipher, self.pvk)
            self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientEncryptor.DeployHandshakeKeys() : {e}' + Reset)
        finally:
            pass
        
class Connector:
    def __init__(self):
        try:
            self.c : list[socket] = None
            self.OtherIP : str = None
        except Exception as e:
            print(Red + f'The Following Error Heppened in Connector.__init__() : {e}' + Reset)
        finally:
            pass
    
class ServerConnector(Connector):
    def __init__(self):
        super().__init__()
        try:
            self.en : ServerEncryptor = ServerEncryptor()
            self.c = self.ServerConnect()
            self.Handshake()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerConnector.__init__() : {e}' + Reset)
        finally:
            pass
        
    def Handshake(self):
        try:
            self.c[0].send(self.en.MinorCipher)
            self.c[0].send(self.en.MajorCipher)
            recv = self.c[0].recv(6000)
            tag = self.c[0].recv(6000)
            hndshake = self.en.AESDecryptLayer(recv, tag)
            print(Cyan + 'Handshake : ' + str(hndshake.decode('utf-8')) + Reset)
        except Exception as e:
            err = "'NoneType' object is not subscriptable"
            if str(e) == err:
                pass
            else:
                print(Red + f'The Following Error Heppened in ServerConnector.Handshake() : {e}' + Reset)
        finally:
            pass
        
    def ServerConnect(self) -> list[socket]:
        try:
            s1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            myip = str(net_if_addrs()['Wi-Fi'][1].address)
            print(Blue + 'Your Ip Address is : ' + myip + Reset)
            s1.bind((myip, p1))
            s1.listen(60)
            print(Magenta + 'Server Is Listening For Connections...' + Reset)
            c1, a1 = s1.accept()
            print(Green + f'Tunnel LayLine 1 Connection Established With {str(a1)}' + Reset)
            s2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            ep = (myip, p2)
            s2.bind(ep)
            s2.listen(60)
            c2, a2 = s2.accept()
            print(Green + f'Tunnel LayLine 2 Connection Established With {str(a2)}' + Reset)
            s3 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            s3.bind((myip, p3))
            s3.listen(60)
            c3, a3 = s3.accept()
            print(Green + f'Tunnel LayLine 3 Connection Established With {str(a3)}' + Reset)
            s4 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            s4.bind((myip, p4))
            s4.listen(60)
            c4, a4 = s4.accept()
            print(Green + f'Tunnel LayLine 4 Connection Established With {str(a4)}' + Reset)
            self.OtherIP = a1[0]
            return [c1, c2, c3, c4]
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerConnctor.ServerConnect() : {e}' + Reset)
        finally:
            self.Handshake()
    
class ClientConnector(Connector):
    def __init__(self):
        super().__init__()
        try:
            self.ip = ip
            self.en : ClientEncryptor = ClientEncryptor()
            self.c = self.ClientConnect()
            self.Handshake()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientConnector.__init__() : {e}' + Reset)
        finally:
            pass
        
    def Handshake(self):
        try:
            MinorCipher = self.c[0].recv(6000)
            MajorCipher = self.c[0].recv(6000)
            self.en.MinorCipher = MinorCipher
            self.en.MajorCipher = MajorCipher
            self.en.DeployHandshakeKeys()
            msg = 'Welcome To GreyShadow Arena'
            print(f'{Cyan} Created Message : {msg} {Reset}')
            hndshake = self.en.AESEncryptLayer(str(msg).encode('utf-8'))
            self.c[0].send(hndshake[0])
            self.c[0].send(hndshake[1])
        except Exception as e:
            err = "'NoneType' object is not subscriptable"
            if str(e) == err:
                pass
            else:
                print(Red + f'The Following Error Heppened in ClientConnector.Handshake() : {e}' + Reset)
        finally:
            pass
            
    def ClientConnect(self) -> list[socket]:
        try:
            c1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c1.connect((self.ip, p1))
            print(Green + f'Tunnel LayLine 1 Connection Established With {self.ip} : {p1}' + Reset)
            c2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c2.connect((self.ip, p2))
            print(Green + f'Tunnel LayLine 2 Connection Established With {self.ip} : {p2}' + Reset)
            c3 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c3.connect((self.ip, p3))
            print(Green + f'Tunnel LayLine 3 Connection Established With {self.ip} : {p3}' + Reset)
            c4 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            c4.connect((self.ip, p4))
            print(Green + f'Tunnel LayLine 4 Connection Established With {self.ip} : {p4}' + Reset)
            self.OtherIP = self.ip
            return [c1, c2, c3, c4]
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientConnector.ClientConnect() : {e}' + Reset)
        finally:
            self.Handshake()
            
class ChatPool:
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        try:
            self.cipher = encryptor
            self.yn = YourName
            self.on = OtherName
            self.c = connector.c
            self.conn = connector
            if SaveConv == True:
                self.InitConversationFile()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.__init__() : {e}' + Reset)
        finally:
            pass
    
    def GetFileData(self, FilePath : str) -> bytes:
        try:
            if filee == None:
                pass
            else:
                f = open(FilePath, 'rb')
                fd : bytes = f.read()
                f.close()
                return fd
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.GetFileData() : {e}' + Reset)
        finally:
            pass
        
    def SaveFileData(self, FileName : str, FileData : bytes):
        try:
            os.chdir('Files')
            f = open(FileName, 'wb')
            f.write(FileData)
            f.close()
            os.chdir('..')
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.SaveFileData() : {e}' + Red)
        finally:
            pass
    
    def SendTxtMsg(self, message : str, Connection : socket):
        try:
            cipherdata = self.cipher.AESEncryptLayer(message.encode('utf-8'))
            tag = rsa.encrypt(cipherdata[1], self.cipher.puk)
            Connection.send(cipherdata[0])
            Connection.send(tag)
            print(Magenta + self.yn + ' > ' + Reset + message)
            print()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.SendTxtMsg() : {e}' + Reset)
        finally:
            pass
            
    def RecvTxtMsg(self, Connection : socket) -> str:
        try:
            msgdata = Connection.recv(50000)
            ctag = Connection.recv(50000)
            tag = rsa.decrypt(ctag, self.cipher.pvk)
            return self.cipher.AESDecryptLayer(msgdata, tag).decode('utf-8')
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.RecvTxtMsg() : {e}' + Reset)
        finally:
            pass
        
    def SendFile(self, FilePath : str, Connection : socket):
        try:
            if filee == None:
                pass
            else:
                print(Cyan + 'Sending File...' + Reset)
                FileData : bytes = self.GetFileData(FilePath)
                CipherList : list = self.cipher.EncryptFile(FilePath, FileData)
                for cipher in CipherList:
                    Connection.send(cipher)
                print(Green + f'File {FilePath} Sent..' + Reset)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.SendFile() : {e}' + Reset)
        finally:
            pass 
            
    def RecvFile(self, Connection : socket):
        try:
            print(Cyan + 'Recieving File...' + Reset)
            fileciphername : bytes = Connection.recv(40000)
            cipherfile : bytes = Connection.recv(5000000)
            ctag : bytes = Connection.recv(50000)
            CipherList = [fileciphername, cipherfile, ctag]
            FileName, FileData = self.cipher.DecryptFile(CipherList)
            self.SaveFileData(FileName, FileData)
            print(Green + f'File {FileName} Recieved...' + Reset)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.RecvFile() : {e}' + Reset)
        finally:
            pass
    
    def InitConversationFile(self):
        try:
            oi : str = str(self.conn.OtherIP)
            os.chdir('Conversations')
            XmlData = BeautifulSoup('', 'lxml-xml')
            Root = XmlData.new_tag('Conversation', othername=self.on, ipa=oi)
            XmlData.append(Root)
            Data = XmlData.prettify()
            f = open(self.on, 'w')
            f.write(str(Data))
            f.close()
            os.chdir('..')
            print(Green + f'Conversation File {self.on} Initiated..' + Reset)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.InitConversationFile() : {e}' + Reset)
        finally:
            pass
        
    def SaveMessage(self, MessageOwner : str, Message : str):
        try:
            pass
        except Exception as e:
            print(Red + f'The Following Error Heppened in ChatPool.SaveMessage() : {e}' + Reset)
        finally:
            pass
        
class ServerChatPool(ChatPool):
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        super().__init__(connector, encryptor, YourName, OtherName)
        
    def Pool(self):
        try:
            t1 = Thread(target=self.Tunnel1, daemon=True)
            t2 = Thread(target=self.Tunnel2, daemon=True)
            t3 = Thread(target=self.Tunnel3, daemon=True)
            t4 = Thread(target=self.Tunnel4, daemon=True)
            t2.start()
            t1.start()
            t3.start()
            t4.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Pool() : {e}' + Reset)
        finally:
            pass
        
    def Tunnel1(self):
        print(Cyan + 'Starting Tunnel 1 ...' + Reset)
        try:
            print(Magenta + self.yn  + Reset, end='')
            Msg = str(input(' > '))
            while Msg not in ['bye', 'disc', 'exit']:
                print()
                self.SendTxtMsg(Msg, self.c[0])
                print(Magenta + self.yn  + Reset, end='')
                Msg = str(input(' > '))
            sys.exit(0)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Tunnel1() : {e}' + Reset)
        finally:
            pass
        
    def Tunnel2(self):
        print(Cyan + 'Starting Tunnel 2 ...' + Reset)
        try:
            Msg = self.RecvTxtMsg(self.c[1])
            while Msg not in ['bye', 'disc', 'exit']:
                print()
                print(Blue + self.on + ' > ' + Reset + Msg)
                Msg = self.RecvTxtMsg(self.c[1])
            sys.exit(0)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Tunnel2() : {e}' + Reset)
        finally:
            pass
        
    def Tunnel3(self):
        print(Cyan + 'Starting Tunnel 3 ...' + Reset)
        try:
            self.SendFile(filee, self.c[2])
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Tunnel3() : {e}' + Reset)
        finally:
            pass
            
    def Tunnel4(self):
        print(Cyan + 'Starting Tunnel 4 ...' + Reset)
        try:
            self.RecvFile(self.c[3])
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Tunnel4() : {e}' + Reset)
        finally:
            pass
        
class ClientChatPool(ChatPool):
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        super().__init__(connector, encryptor, YourName, OtherName)
    
    def Pool(self):
        try:
            t1 = Thread(target=self.Tunnel1, daemon=True)
            t2 = Thread(target=self.Tunnel2, daemon=True)
            t3 = Thread(target=self.Tunnel3, daemon=True)
            t4 = Thread(target=self.Tunnel4, daemon=True)
            t1.start()
            t2.start()
            t3.start()
            t4.start()
            t1.join()
            t2.join()
            t3.join()
            t4.join()
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientChatPool.Pool() : {e}' + Reset)
        finally:
            pass
    
    def Tunnel1(self):
        print(Cyan + 'Starting Tunnel 1 ...' + Reset)
        try:
            Msg = self.RecvTxtMsg(self.c[0])
            while Msg not in ['bye', 'disc', 'exit']:
                print()
                print(Blue + self.on + ' > ' + Reset + Msg)
                Msg = self.RecvTxtMsg(self.c[0])
            sys.exit(0)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientChatPool.Tunnel1() : {e}' + Reset)
        finally:
            pass
        
    def Tunnel2(self):
        print(Cyan + 'Starting Tunnel 2 ...' + Reset)
        try:
            print(Magenta + self.yn  + Reset, end='')
            Msg = str(input(' > '))
            while Msg not in ['bye', 'disc', 'exit']:
                print()
                self.SendTxtMsg(Msg, self.c[1])
                print(Magenta + self.yn  + Reset, end='')
                Msg = str(input(' > '))
            sys.exit(0)
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerChatPool.Tunnel2() : {e}' + Reset)
        finally:
            pass
    
    def Tunnel3(self):
        print(Cyan + 'Starting Tunnel 3 ...' + Reset)
        try:
            self.RecvFile(self.c[2])
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientChatPool.Tunnel3() : {e}' + Reset)
        finally:
            pass
        
    def Tunnel4(self):
        print(Cyan + 'Starting Tunnel 4 ...' + Reset)
        try:
            self.SendFile(filee, self.c[3])
        except Exception as e:
            print(Red + f'The Following Error Heppened in ClientChatPool.Tunnel4() : {e}' + Reset)
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
                print(Red + f'{role} is an Invalid Role !' + Reset)
        except Exception as e:
            print(Red + f'The Following Error Heppened in PlayGround.home() : {e}' + Reset)
        finally:
            pass
    
p = ArgumentParser()
p.add_argument('-r', type=str, metavar='role, ex: [1, server, Server, s], for client you can type : [2, client, Client, c]', required=True)
p.add_argument('-yn', type=str, metavar='YourName', required=True)
p.add_argument('-on', type=str, metavar='OtherName', required=True)
p.add_argument('-f', type=str, metavar='File to be sent', required=False)
p.add_argument('-mjk', type=str, metavar='Major Encryption Key', required=False)
p.add_argument('-mnk', type=str, metavar='Minor Encryption Key', required=False)
p.add_argument('-ports', type=str, metavar='4 Tunnels Ports ex:111,112,113,114', required=False)
p.add_argument('-ip', type=str, metavar='IP Address of the Server', required=False)
p.add_argument('-sc', type=str, metavar='Save Conversation', required=False)
a = p.parse_args()
role = str(a.r)
YourName = str(a.yn)
OtherName = str(a.on)
filee = str(a.f)
MajorKey = str(a.mjk).encode('utf-8')
MinorKey = str(a.mnk).encode('utf-8')
ports : list[str]= str(a.ports).split(',')
p1 = int(ports[0])
p2 = int(ports[1])
p3 = int(ports[2])
p4 = int(ports[3])
ip = str(a.ip)
SaveConv : bool = True if str(a.sc) in ['y', 'yes', 'Yes', 'True', 'true'] else False
Magenta = Fore.MAGENTA + Style.BRIGHT
Grey = Fore.LIGHTBLACK_EX + Style.BRIGHT
White = Fore.WHITE + Style.BRIGHT
Red = Fore.RED + Style.BRIGHT
Cyan = Fore.CYAN + Style.BRIGHT
Green = Fore.GREEN + Style.BRIGHT
Blue = Fore.BLUE + Style.BRIGHT
Reset = Fore.RESET + Style.RESET_ALL

if __name__ == '__main__':
    try:
        pg = PlayGround(YourName, OtherName)
        pg.home(role)
    except Exception as e:
        print(Red + f'The Following Error Heppened in main() : {e}' + Reset)