from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt

import sys
import logging

from manageTools.models import ConnectedSystem,UsedIO,IO,IOType
from PyLightSupport.Commandos import *
from PyLightServer.tcpserver import sendDataToTCPServer

logger = logging.getLogger(__name__)

@csrf_exempt
def handleRequests(request):
    logger.info(f"Incoming request from tcp server. POST Data: {request.POST}")
    cmd = request.POST['cmd']
    logger.debug(f"Incoming command: {cmd}")
    data = cmd.split('||')

    returnWord = ""

    if data[0] == cmd_signup[0]:
        logger.info(f"Processing {cmd_signup[0]} with serial number {data[3]}")
        if len(ConnectedSystem.objects.filter(serialNumber=data[3])) == 0:
            logger.info(f"System with serial number {data[3]} not in database, adding new one")
            system = ConnectedSystem(name="Change me",lastIP=data[1],lastMacAddress=data[2]
                                ,serialNumber=data[3],connected=True,active=True)
            system.save()
            io = IO.objects.get(ioNr=0)
            ioType = IOType.objects.get(id=0)
            usedIO = UsedIO(name="",pin=io,type=ioType,connectedSystem=system)
            logger.info(f"Added system with {usedIO}")
            usedIO.save()

        system = ConnectedSystem.objects.get(serialNumber=data[3])
        returnWord = cmd_welcome[0]+f"||{system.name}"

    logger.info(f"Sending returnWord {returnWord}")
    sendDataToTCPServer(returnWord)
    return HttpResponse()
