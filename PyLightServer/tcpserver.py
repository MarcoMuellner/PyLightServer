from twisted.internet.protocol import Protocol
from twisted.internet.protocol import Factory
import requests
import socket
import logging
from requests.exceptions import ConnectionError

from PyLightSupport.Globals import *
from PyLightSupport.Commandos import *

logger = logging.getLogger(__name__)

class Server(Protocol):
    def __init__(self,factory ,addr):
        self.factory = factory
        self.addr = addr

    def connectionMade(self):
        logger.info(f"Client connected with ip {self.addr}")
        self.factory.clients.append(self)

    def connectionLost(self,reason):
        if self.addr != '127.0.0.1':
            logger.info(f"Connection lost due to {reason} with ip {self.addr}")
            data = f"{cmd_client_disconnected[0]}||{self.addr.host}"
            sendPostData(data)


    def dataReceived(self,data:bytes):
        logger.info(f"Data received: {data} from ip {self.addr}")
        if self.addr.host == '127.0.0.1':
            logger.info("Data from localhost, sending data to client")
            cmds = str.split(data.decode(),"##")
            self.factory.sendData(cmds[1],cmds[0])
        else:
            logger.info(f"Data from client, sending to server with {data}")
            sendPostData(data)


    def sendData(self,data:str):
        logger.debug(f"Sending data {data}")
        self.transport.write(str.encode(data))


class ServerFactory(Factory):
    def __init__(self):
        self.clients = []

    def buildProtocol(self,addr):
        logger.info(f"Building protocol with {addr} ")
        return Server(self,addr)

    def sendData(self,data:str,ip = ""):
        for i in self.clients:
            if i.addr.host != '127.0.0.1' and (ip != "" or i.addr.host == ip):
                logger.info(f"Sending data {data} to {i}")
                i.sendData(data)

def sendPostData(data):
    logger.debug(f"Sending request to django with {data}")
    try:
        #Verify=False is necesary because we have a self signed certificate
        requests.post('https://127.0.0.1/hardwareRequest/',data={'cmd':data},verify=False)
    except ConnectionError:
        logger.info("Running on testserver --> using port 8000")
        requests.post('http://127.0.0.1:8000/hardwareRequest/', data={'cmd': data})

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