from django.shortcuts import render
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

import logging
import requests

from PyLightCommon.pylightcommon.models import ConnectedSystem,UsedIO
from PyLightCommon.Commandos import *

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
    usedIo = get_object_or_404(UsedIO, pk=usedio_id)
    if 'io_switch' in request.POST:
        logger.info(f"Setting {usedIo} to True")
        usedIo.active = True
        cmd =cmd_set_output[0]
    else:
        logger.info(f"Setting {usedIo} to False")
        usedIo.active = False
        cmd = cmd_reset_outptut[0]

    richCmd = f"{cmd}||{usedIo.name}"
    usedIo.save()
    logger.debug(f"Sending data to TCPServer: {richCmd}")
    requests.post(f"http://{usedIo.connectedSystem.lastIP}:8080/serverCommunication/", data={"cmd": richCmd})
    return HttpResponseRedirect(reverse('home'))
