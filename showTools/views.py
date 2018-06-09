from django.shortcuts import render
from manageTools.models import ConnectedSystem,UsedIO
from django.views import generic
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect

class ConnectedSystemsView(generic.ListView):
    template_name='showTools/index.html'
    context_object_name = 'connectedSystem_list'

    def get_queryset(self):
        return ConnectedSystem.objects.order_by('-name')

def saveState(request,usedio_id):
    usedIo = get_object_or_404(UsedIO,pk=usedio_id)
    if 'io_switch' in request.POST:
        if request.POST['io_switch'] == 'on':
            usedIo.active = True
    else:
        usedIo.active = False
    usedIo.save()
    return HttpResponseRedirect(reverse('index'))

