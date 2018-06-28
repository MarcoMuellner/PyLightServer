from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

import logging

from PyLightCommon.pylightcommon.models import ConnectedSystem,UsedIO,IO,IOType
from PyLightCommon.cmdHandler.cmdHandler import sendCommand

logger = logging.getLogger(__name__)

class ConnectedSystemsView(generic.ListView):
    template_name='manageTools/index.html'
    context_object_name = 'connectedSystem_list'

    def get_queryset(self):
        logger.debug(f"Requesting query set: {ConnectedSystem.objects.order_by('-name')}")
        return ConnectedSystem.objects.order_by('-name')

def saveSystem(request, connectedSystem_id):
    connectedSystem = get_object_or_404(ConnectedSystem,pk=connectedSystem_id)
    sendCommand(connectedSystem.lastIP,
                commando='nameChange',
                id=connectedSystem_id,
                name=request.POST['system_name'])


    logger.info(f"Setting system name with id {connectedSystem_id} from {connectedSystem.name} to"
                f"{request.POST['system_name']}")

    return HttpResponseRedirect(reverse('manageTools:index'))

def saveIO(request, usedio_id):
    logger.debug("Adding new io")
    io = get_object_or_404(IO,pk=request.POST['io_selection'])
    ioType = get_object_or_404(IOType,pk=request.POST['io_type_selection'])

    logger.debug(f"Future io: {io}, type: {ioType}")

    usedIo = get_object_or_404(UsedIO,pk=usedio_id)

    sendCommand(usedIo.connectedSystem.lastIP,
                commando="addOut",
                name=request.POST['io_name'],
                pin=io,
                type=ioType)
    return HttpResponseRedirect(reverse('manageTools:index'))

def config_layout(request):
    template = 'manageTools/index.html'
    return render(request,template)