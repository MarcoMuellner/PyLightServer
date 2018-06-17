from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.exceptions import ObjectDoesNotExist
from django.views import View

import sys
import logging

from PyLightCommon.pylightcommon.models import ConnectedSystem,UsedIO,IO,IOType
from PyLightCommon.Commandos import *

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class HardwareRequest(View):

    def get(self,request):
        logger.info(f"Incoming request from tcp server. POST Data: {request.GET}")
        cmd = request.GET["cmd"]
        if cmd[0] == cmd_alive[0]:
            return HttpResponse("OK",content_type="text/plain")


    def post(self,request):
        logger.info(f"Incoming request from tcp server. POST Data: {request.POST}")
        cmd = request.POST['cmd']
        logger.debug(f"Incoming command: {cmd}")
        data = cmd.split('||')

        cmdword = ""

        if data[0] == cmd_signup[0]:
            logger.info(f"Processing {cmd_signup[0]} with serial number {data[3]}")
            if len(ConnectedSystem.objects.filter(serialNumber=data[3])) == 0:
                logger.info(f"System with serial number {data[3]} not in database, adding new one")
                system = ConnectedSystem(name="Change me", lastIP=request.META["REMOTE_ADDR"], lastMacAddress=data[2]
                                         , serialNumber=data[3], connected=True, active=True)
                system.save()
                io = IO.objects.get(ioNr=0)
                ioType = IOType.objects.get(id=0)
                usedIO = UsedIO(name="", pin=io, type=ioType, connectedSystem=system)
                logger.info(f"Added system with {usedIO}")
                usedIO.save()
            else:
                logger.info(f"Changing system with serial number {data[3]} to IP {data[1]} and Mac {data[2]}")
                system = ConnectedSystem.objects.get(serialNumber=data[3])
                system.lastIP=request.META["REMOTE_ADDR"]
                system.lastMacAddress = data[2]
                system.connected = True
                system.save()

        else:
            logger.error(f"Command {data[0]} not known by server, returning")
            return HttpResponse()

        return HttpResponse()
