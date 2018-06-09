from .models import *
from django.views import generic
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db import IntegrityError



class ConnectedSystemsView(generic.ListView):
    template_name='manageTools/index.html'
    context_object_name = 'connectedSystem_list'

    def get_queryset(self):
        return ConnectedSystem.objects.order_by('-name')

def saveSystem(request, connectedSystem_id):
    connectedSystem = get_object_or_404(ConnectedSystem,pk=connectedSystem_id)
    connectedSystem.name = request.POST['system_name']
    connectedSystem.save()
    return HttpResponseRedirect(reverse('index'))

def saveIO(request, usedio_id):

    io = get_object_or_404(IO,pk=request.POST['io_selection'])
    ioType = get_object_or_404(IOType,pk=request.POST['io_type_selection'])

    usedIo = get_object_or_404(UsedIO,pk=usedio_id)

    if usedIo.id == min(UsedIO.objects.filter(connectedSystem=usedIo.connectedSystem).values_list('id',flat=True)):
        usedIo = UsedIO(name=request.POST['io_name'],pin=io,type=ioType,connectedSystem=usedIo.connectedSystem)
        oldPin = 0
    else:
        usedIo.name = request.POST['io_name']
        oldPin = usedIo.pin
        usedIo.pin = io
        usedIo.type = ioType

    try:
        usedIo.save()
    except IntegrityError:
        usedIo.pin = oldPin
        usedIo.save()
    return HttpResponseRedirect(reverse('index'))
