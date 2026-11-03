def ServerConnect(self) -> list[socket]:
        try:
            s1 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
            myip = str(net_if_addrs()['wlp2s0'][0].address)
            print(Blue + 'Your Ip Address is : ' + myip + Reset)
            s1.bind((myip, p1))
            s1.listen(120)
            print(Magenta + 'Server Is Listening For Connections...' + Reset)
            c1, a1 = s1.accept()
            if True:
                print(Green + f'Tunnel LayLine 1 Connection Established With {str(a1)}' + Reset)
                s2 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
                s2.bind((myip, p2))
                s2.listen(120)
                c2, a2 = s2.accept()
                print(Green + f'Tunnel LayLine 2 Connection Established With {str(a2)}' + Reset)
                s3 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
                s3.bind((myip, p3))
                s3.listen(120)
                c3, a3 = s3.accept()
                print(Green + f'Tunnel LayLine 3 Connection Established With {str(a3)}' + Reset)
                s4 = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
                s4.bind((myip, p4))
                s4.listen(120)
                c4, a4 = s4.accept()
                print(Green + f'Tunnel LayLine 4 Connection Established With {str(a4)}' + Reset)
                self.OtherIP = a1[0]
                return [c1, c2, c3, c4]
        except Exception as e:
            print(Red + f'The Following Error Heppened in ServerConnctor.ServerConnect() : {e}' + Reset)
        finally:
            self.Handshake()
            
            
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
            

