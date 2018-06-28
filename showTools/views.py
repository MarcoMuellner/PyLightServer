from django.shortcuts import render
from django.views import generic
from django.urls import reverse
from django.http import HttpResponseRedirect

import logging

from PyLightCommon.pylightcommon.models import ConnectedSystem,UsedIO
from PyLightCommon.cmdHandler.cmdHandler import sendCommand

logger = logging.getLogger(__name__)


class ConnectedSystemsView(generic.ListView):
    template_name = 'showTools/index.html'
    context_object_name = 'connectedSystem_list'

    def get_queryset(self):
        logger.debug(f"Requesting query set: {ConnectedSystem.objects.order_by('-name')}")
        return ConnectedSystem.objects.order_by('-name')


def base_layout(request):
    template = 'showTools/index.html'
    return render(request, template)


def saveState(request, usedio_id):
    logger.debug(f"Changing state of io {usedio_id}")
    usedIo = UsedIO.objects.get(pk=usedio_id)
    if 'io_switch' in request.POST:
        sendCommand(usedIo.connectedSystem.lastIP,
                    commando="changeOut",
                    usedIO_id=usedio_id,
                    active=True)
        logger.info(f"Setting {usedIo} to True")
    else:

        sendCommand(usedIo.connectedSystem.lastIP,
                    commando="changeOut",
                    usedIO_id=usedio_id,
                    active=False)
        logger.info(f"Setting {usedIo} to False")

    return HttpResponseRedirect(reverse('showTools:base_layout'))