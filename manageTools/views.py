from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db import IntegrityError
import requests

import logging

from PyLightCommon.pylightcommon.models import ConnectedSystem,UsedIO,IO,IOType
from PyLightCommon.Commandos import *

logger = logging.getLogger(__name__)

class ConnectedSystemsView(generic.ListView):
    template_name='manageTools/index.html'
    context_object_name = 'connectedSystem_list'

    def get_queryset(self):
        logger.debug(f"Requesting query set: {ConnectedSystem.objects.order_by('-name')}")
        return ConnectedSystem.objects.order_by('-name')

def saveSystem(request, connectedSystem_id):
    logger.debug(f"Setting new name for system with id {connectedSystem_id}")
    connectedSystem = get_object_or_404(ConnectedSystem,pk=connectedSystem_id)
    logger.info(f"Setting system name with id {connectedSystem_id} from {connectedSystem.name} to"
                f"{request.POST['system_name']}")
    connectedSystem.name = request.POST['system_name']
    connectedSystem.save()

    requests.post(f"http://{connectedSystem.lastIP}:8080/serverCommunication/",data={"cmd":f"{cmd_change_name[0]}"
                                                                                      f"||{connectedSystem.name}"})

    return HttpResponseRedirect(reverse('index'))

def saveIO(request, usedio_id):
    logger.debug("Adding new io")
    io = get_object_or_404(IO,pk=request.POST['io_selection'])
    ioType = get_object_or_404(IOType,pk=request.POST['io_type_selection'])

    logger.debug(f"Future io: {io}, type: {ioType}")

    usedIo = get_object_or_404(UsedIO,pk=usedio_id)

    if usedIo.id == min(UsedIO.objects.filter(connectedSystem=usedIo.connectedSystem).values_list('id',flat=True)):
        logger.info(f"Adding new io with name {request.POST['io_name']}, io {io}, type {ioType}")
        usedIo = UsedIO(name=request.POST['io_name'],pin=io,type=ioType,connectedSystem=usedIo.connectedSystem)
        oldPin = 0
    else:
        logger.info(f"Setting io with id {usedIo.id} from {usedIo.name} to {request.POST['io_name']} with io"
                    f"{io} and type {ioType}")
        usedIo.name = request.POST['io_name']
        oldPin = usedIo.pin
        usedIo.pin = io
        usedIo.type = ioType

    try:
        usedIo.save()
    except IntegrityError:
        usedIo.pin = oldPin
        usedIo.save()

    cmdword = f"{cmd_add_output[0]}||{usedIo.name}||{io.ioNr}"
    logger.debug(f"Sending data to TCPServer: {cmdword}")

    requests.post(f"http://{usedIo.connectedSystem.lastIP}:8080/serverCommunication/",data={"cmd":cmdword})
    return HttpResponseRedirect(reverse('index'))

def config_layout(request):
    template = 'manageTools/index.html'
    return render(request,template)