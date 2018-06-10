from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.csrf import csrf_exempt
from manageTools.models import ConnectedSystem,UsedIO,IO,IOType
from PyLightSupport.Commandos import *
from PyLightServer.tcpserver import sendDataToTCPServer
import sys

@csrf_exempt
def handleRequests(request):
    cmd = request.POST['cmd']
    data = cmd.split('||')
    if data[0] == cmd_signup[0]:
        if len(ConnectedSystem.objects.filter(serialNumber=data[3])) == 0:
            system = ConnectedSystem(name="Change me",lastIP=data[1],lastMacAddress=data[2]
                                ,serialNumber=data[3],connected=True,active=True)
            system.save()
            io = IO.objects.get(ioNr=0)
            ioType = IOType.objects.get(id=0)
            usedIO = UsedIO(name="",pin=io,type=ioType,connectedSystem=system)
            usedIO.save()


        sendDataToTCPServer(cmd_welcome[0]+f"||{ConnectedSystem.objects.get(serialNumber=data[3]).name}")

    return HttpResponse()
