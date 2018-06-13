from django.contrib import admin
from django.urls import include, path
import showTools
import manageTools


from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from multiprocessing import Process
import logging

from PyLightServer.tcpserver import ServerFactory
from PyLightSupport.Globals import *
import sys

urlpatterns = [
    path('', include('pwa.urls')),
    path('', include('showTools.urls')),
    path('showTools/', include('showTools.urls')),
    path('manageTools/', include('manageTools.urls')),
    path('hardwareRequest/', include('hardwareRequest.urls')),
    path('admin/', admin.site.urls),
    path(r'base_layout',showTools.views.base_layout,name='base_layout'),
    path(r'config_layout',manageTools.views.config_layout,name='config_layout'),
]

logger = logging.getLogger(__name__)

def startTCPServer():
    print("DEPP",file=sys.stderr)
    logger.debug(f"Starting TCP4 Server on {port}")
    endpoint = TCP4ServerEndpoint(reactor,port)
    factory = ServerFactory()
    endpoint.listen(factory)
    logger.debug(f"Running reactor")
    reactor.run()


#Running in top level urls --> only called once
p = Process(target=startTCPServer)
p.start()

