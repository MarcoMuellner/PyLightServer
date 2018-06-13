from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
import requests
import socket
import logging

from PyLightSupport.Globals import *

logger = logging.getLogger(__name__)

class Server(Protocol):
    def __init__(self,factory ,addr):
        self.factory = factory
        self.addr = addr

    def connectionMade(self):
        logger.info(f"Client connected with ip {self.addr}")
        self.factory.clients.append(self)

    def connectionLost(self,reason):
        logger.info(f"Connection lost due to {reason} with ip {self.addr}")

    def dataReceived(self,data:bytes):
        logger.info(f"Data received: {data} from ip {self.addr}")
        if self.addr.host == '127.0.0.1':
            logger.info("Data from localhost, sending data to client")
            cmds = str.split(data.decode(),"##")
            self.factory.sendData(cmds[1],cmds[0])
        else:
            logger.info(f"Data from client, sending to server with {data}")
            requests.post('http://127.0.0.1/hardwareRequest/',data={'cmd':data})

    def sendData(self,data):
        logger.debug(f"Sending data {data}")
        self.transport.write(data)


class ServerFactory(Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self,addr):
        logger.info(f"Building protocol with {addr} ")
        return Server(self,addr)

    def sendData(self,data,ip = ""):
        for i in self.clients:
            if i.addr.host != '127.0.0.1' and (ip != "" or i.addr.host == ip):
                logger.info(f"Sending data {data} to {i}")
                i.sendData(data)

def sendDataToTCPServer(data):
    logger.debug(f"Sending {data} to TCP server")
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    server_address = ('localhost',port)
    logger.debug(f"Server address is {server_address} --> connecting")
    sock.connect(server_address)
    logger.debug(f"Sending data")
    sock.sendall(str.encode(data))
    logger.debug(f"Closing socket")
    sock.close()