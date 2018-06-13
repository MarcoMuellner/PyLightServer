"""
WSGI config for PyLightServer project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application


from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from multiprocessing import Process
import logging

from PyLightServer.tcpserver import ServerFactory
from PyLightSupport.Globals import *

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "PyLightServer.settings")

logger = logging.getLogger(__name__)

runServer = False



def startTCPServer():
    logger.debug(f"Starting TCP4 Server on {port}")
    endpoint = TCP4ServerEndpoint(reactor,port)
    factory = ServerFactory()
    endpoint.listen(factory)
    logger.debug(f"Running reactor")
    reactor.run()

if not runServer:
    p = Process(target=startTCPServer)
    p.start()
    runServer = True
else:
    logger.debug("Logger already running")




application = get_wsgi_application()
