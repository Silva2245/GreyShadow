import os
import sys
from socket import *
import asyncio
from rsa import *
from Crypto.Cipher import AES
from base64 import *
from hashlib import *
from colorama import *
from psutil import *

class Encryptor:
    def __init__(self):
        print(Fore.CYAN + Style.DIM + 'Enter The Major Key ' + Style.RESET_ALL + Fore.RESET, end='')
        self.MajorKey = str(input(' > ')).encode('ascii')
        print(Fore.CYAN + Style.DIM + 'Enter The Minor Key ' + Style.RESET_ALL + Fore.RESET, end='')
        self.MinorKey = str(input(' > ')).encode('ascii')
        vmj = self.ValidateMajorKey(self.MajorKey)
        vmn = self.ValidateMinorKey(self.MinorKey)
        if vmj == True and vmn == True:
            print(Fore.GREEN + Style.BRIGHT + 'The Keys Are Valid' + Style.RESET_ALL + Fore.RESET)
        else:
            print(Fore.RED + Style.NORMAL + 'The Keys Are Invalid' + Style.RESET_ALL + Fore.RESET)
            sys.exit(0)
        self.AesCipher = AES.new(key=self.MajorKey, mode=AES.MODE_GCM, nonce=self.MinorKey)
        self.tag = None
        self.puk = PublicKey(20754990986263218681313840090981290486714834267245681731195215816802357219626058398490791366068911882409135325757716558308615024165560966052611378737252772755663037140455683784897845902687614154299629313494854989590268941820431542114959088690677128445710946879567098761596214930651479971682613505656523942928901777231244166823624028995773296834261448033860929834967547354832873431699331189537355987181022186301608929171107858095016348434577688270993979425788410298020088148909102936265719278592827947533236430600229887080691490319726684622337355671332439376261101240418615790000472143770783381840941489556192498532153, 
                             65537)
        self.pvk = PrivateKey(20754990986263218681313840090981290486714834267245681731195215816802357219626058398490791366068911882409135325757716558308615024165560966052611378737252772755663037140455683784897845902687614154299629313494854989590268941820431542114959088690677128445710946879567098761596214930651479971682613505656523942928901777231244166823624028995773296834261448033860929834967547354832873431699331189537355987181022186301608929171107858095016348434577688270993979425788410298020088148909102936265719278592827947533236430600229887080691490319726684622337355671332439376261101240418615790000472143770783381840941489556192498532153, 
                              65537, 
                              14676420148563351135208009083973113585086677212062905358328576019623596451304307862142892477191992055884257112800248080652091888015999997707801228692502025540010866078705734983955946605249738357762908300277584643523228612398862611291843524225888431932489775412969437995462920007494721093848408606281680239419094723974661893513121141708829766708186639516222689807880497527047267787872376762328069859930485846929174009122188389253758496313017968822798958913291911372175875080133365762271739621739676741938992848806471540229386800402774655590535154311772086671050317580544381439795546855474226464317118014380692135367933, 3111642810301690359814516477140709663540966247404370897926705194646838837520342908630255790651213518543108880856164878859665622921688635892309711774883589366785585313282935082970946741949199584943183771238300690280817469589648883625841547379833655339538116491287904375268116248894870132103929862786409041817042474298565496533171, 
                              6670107159327490950805805040938160145688220880631817648856598713757832642440309185523198879571338670704595944456444398894207065909182450267182424444736185580071713686590467738236143061166305830325791762872926927817852387419818341289800836934333526185587999491713532740146057778235929439843)

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
    
    def RSAEncryptLayer(self, txt : str):
        try:
            if self.ValidateTxtLength(txt) == True:
                pt = txt.encode('ascii')
                return encrypt(self.puk, pt)
            else:
                print(Fore.RED + Style.NORMAL + 'The Text Length is Invalid, It Must Be No More Than 256 Characters' + Style.RESET_ALL + Fore.RESET)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.RSAEncryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
            
    def RSADecryptLayer(self, txt : bytes):
        try:
            ct = decrypt(self.pvk, txt)
            return ct.decode('ascii')
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.RSADecryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def AESEncryptLayer(self, data : bytes):
        cd = None
        try:
            cd, self.tag = self.AesCipher.encrypt_and_digest(data)
            return cd
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESEncryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
            
    def AESDecryptLayer(self, data : bytes):
        try:
            return self.AesCipher.decrypt_and_verify(data, self.tag)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.AESDecryptLayer() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def ValidateTxtLength(self, message: str):
        try:
            if len(message) <= 256:
                return True
            else:
                return False
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.ValidateTxtLength() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def EncryptText(self, message : str):
        try:
            layer1 = self.RSAEncryptLayer(message)
            return self.AESEncryptLayer(layer1)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.EncryptText() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def DecryptText(self, message : bytes):
        try:
            layer1 = self.AESDecryptLayer(message)
            return self.RSADecryptLayer(layer1)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened In Encryptor.DecryptText() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def EncryptFile(self, filepath : str):
        try:
            f = open(filepath, 'rb')
            data = f.read()
            f.close()
            cd = self.AESEncryptLayer(data)
            return cd
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.EncryptFile() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    def DecryptFile(self, filedata : bytes, filename : str):
        try:
            pd = self.AESDecryptLayer(filedata)
            filepath = 'files/' + filename
            f = open(filepath, 'wb')
            f.write(pd)
            f.close()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in Encryptor.DecryptFile() : {e}' + Style.RESET_ALL + Fore.RESET)

class Connector:
    def __init__(self):
        self.r = None
        self.ip = None
        self.p = None
        print('1. Server')
        print('2. Client')
        print(Fore.CYAN + Style.DIM + 'What Is Your Role (Server/Client) :' + Fore.RESET + Style.RESET_ALL, end='')
        self.r = str(input(' > '))
        print('r : ' + self.r)
        self.ConnectionOpen = False
        #self.AllPorts = [x for x in range(1, 65536)]
        #self.AllAddresses = self.GenerateAddress()
        self.c = None
        if self.r == '1':
            self.c = self.ServerConnect()
            #task1 = asyncio.create_task(self.SendTxtMsg())
        elif self.r == '2':
            print(Fore.CYAN + Style.DIM + 'Enter The IP Address Of The Other ' + Style.RESET_ALL + Fore.RESET, end='')
            self.ip = str(input(' > '))
            print(Fore.CYAN + Style.DIM + 'Enter The Port Number ' + Style.RESET_ALL + Fore.RESET, end='')
            self.p = int(input(' > '))
            self.c = self.ClientConnect()
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
            myip = str(net_if_addrs()['WiFi'][1].address)
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

class ChatPool:
    def __init__(self, connector : Connector, encryptor : Encryptor, YourName : str, OtherName : str):
        self.c  = connector.c
        self.cipher = encryptor
        self.yn = YourName
        self.on = OtherName
    def HandShake(self):
        try:
            print()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL + Fore.RESET)
            
    async def Pool(self):
        try:
            print(Fore.MAGENTA + Style.NORMAL + self.yn  + Style.RESET_ALL + Fore.RESET, end='')
            Msg = str(input(' > '))
            while Msg != 'exit' or Msg != 'disc' or Msg != 'bye':
                await asyncio.gather(self.SendTxtMsg(Msg), self.RecvTxtMsg())
                print(Fore.MAGENTA + Style.NORMAL + self.yn + Style.RESET_ALL + Fore.RESET)
                Msg = str(input(' > '))
            print(Fore.BLUE + Style.DIM + 'Disconnecting...' + Style.RESET_ALL + Fore.RESET)
            self.c.close()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.Pool() : {e}' + Style.RESET_ALL + Fore.RESET)
    
    async def SendTxtMsg(self, message : str):
        try:
            cipherdata = self.cipher.EncryptText(message)
            await asyncio.to_thread(self.c.send, cipherdata)
            print(Fore.MAGENTA + Style.NORMAL + self.yn + ' > ' + Style.RESET_ALL + Fore.RESET + message)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
                
    async def RecvTxtMsg(self):
        try:
            msgdata = await asyncio.to_thread(self.c.recv, 2000000000)
            res = self.cipher.DecryptText(msgdata)
            print(Fore.YELLOW + Style.DIM + self.on + ' > ' + Style.RESET_ALL + Fore.RESET + res)
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.RecvTxtMsg() : {e}' + Style.RESET_ALL + Fore.RESET)
                
    async def SendFile(self, filepath : str):
        try:
            print()
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened in ChatPool.SendFile() : {e}' + Style.RESET_ALL + Fore.RESET)
                
    async def RecvFile(self):
        res = (None, None)
        try:
            print()
            return res
        except Exception as e:
            print(Fore.RED + Style.NORMAL + f'The Following Error Heppened ChatPool.RecvFile() : {e}' + Style.RESET_ALL + Fore.RESET)
            
            

class PlayGround:
    def __init__(self):
        self.n = None
        
    def home(self):
        print(Fore.WHITE + Style.DIM + '*** Welcome to GreyShadow ***' + Style.RESET_ALL)
        print(Fore.MAGENTA + Style.NORMAL + 'Enter Your Name : ' + Style.RESET_ALL + Fore.RESET, end='')
        YourName = str(input(' > '))
        print(Fore.YELLOW + Style.DIM + 'Enter Other Person Name : ' + Style.RESET_ALL + Fore.RESET, end='')
        OtherName = str(input(' > '))
        e = Encryptor()
        c = Connector()
        if c.ConnectionOpen == True:
            cp = ChatPool(c, e, YourName, OtherName)
            asyncio.run(cp.Pool())
            sys.exit(0)
if __name__ == '__main__':
    try:
        pg = PlayGround()
        pg.home()
    except Exception as e:
        print(Fore.RED +Style.NORMAL + f'The Following Error Heppened : {e}' + Style.RESET_ALL + Fore.RESET)