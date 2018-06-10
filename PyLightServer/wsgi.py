"""
WSGI config for PyLightServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from multiprocessing import Process

from PyLightServer.tcpserver import ServerFactory

from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

def startTCPServer():
    endpoint = TCP4ServerEndpoint(reactor,8500)
    factory = ServerFactory()
    endpoint.listen(factory)
    reactor.run()

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyLightServer.settings")

p = Process(target=startTCPServer)
p.start()

application = get_wsgi_application()
