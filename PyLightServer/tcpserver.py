from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
import requests
import sys
import socket



class Server(Protocol):
    def __init__(self,factory ,addr):
        self.factory = factory
        self.addr = addr

    def connectionMade(self):
        print(f"Client connected with ip {self.addr}")
        self.factory.clients.append(self)

    def connectionLost(self,reason):
        print(f"Connection lost due to {reason} with ip {self.addr}")

    def dataReceived(self,data):
        print(f"Data received: {data} from ip {self.addr}")
        if self.addr.host == '127.0.0.1':
            self.factory.sendData(data)
        else:
            pass
            #requests.post('http://127.0.0.1/hardwareRequest/',data={'cmd':data})

    def sendData(self,data):
        self.transport.write(data)


class ServerFactory(Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self,addr):
        print("Building protocol ...")
        return Server(self,addr)

    def sendData(self,data):
        for i in self.clients:
            if i.addr.host != '127.0.0.1':
                i.sendData(data)

def sendDataToTCPServer(data):
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = ('localhost',8500)
    sock.connect(server_address)
    sock.sendall(str.encode(data))
    sock.close()