from django.contrib import admin
from django.urls import include, path
import showTools
import manageTools


from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from multiprocessing import Process
import logging
import sys
import os
from django.core.exceptions import ObjectDoesNotExist

from PyLightServer.tcpserver import ServerFactory
from PyLightCommon.Globals import *
from PyLightCommon.loghandler import setup_logging
from PyLightCommon.updater import updater,RunnerType
from PyLightCommon.pylightcommon.models import ClientSettings

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

setup_logging()

logger = logging.getLogger(__name__)

def startTCPServer():
    logger.debug(f"Starting TCP4 Server on {port}")
    endpoint = TCP4ServerEndpoint(reactor,port)
    factory = ServerFactory()
    endpoint.listen(factory)
    logger.debug(f"Running reactor")
    reactor.run()


try:
    os.environ['MIGRATIIONS_APPLY']
    migrationsApply = True
except KeyError:
    migrationsApply=False

if not migrationsApply:
    #Running in top level urls --> only called onc
    p = Process(target=startTCPServer)
    p.start()
    print(f"{os.path.dirname(__file__)}/version")
    with open(f"{os.path.dirname(__file__)}/version",'r') as f:
        version = f.read()

try:
    os.environ['DEV_ENVIRONMENT']
    devEnv = True
except KeyError:
    devEnv=False

if not devEnv:
    try:
        settings = ClientSettings.objects.get(pk=1)
        settings.version = version
    except ObjectDoesNotExist:
        settings = ClientSettings(serverAddress="127.0.0.1",name="server",version=version)
    settings.save()

    p = Process(target=updater,args=(RunnerType.Server,version,))
    p.start()


