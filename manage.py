#!/usr/bin/env python
import os
import sys

from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from multiprocessing import Process

from PyLightServer.tcpserver import ServerFactory
from PyLightSupport.loghandler import setup_logging

setup_logging()

def startTCPServer():
    endpoint = TCP4ServerEndpoint(reactor,8500)
    factory = ServerFactory()
    endpoint.listen(factory)
    reactor.run()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyLightServer.settings")

p = Process(target=startTCPServer)
p.start()


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyLightServer.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
