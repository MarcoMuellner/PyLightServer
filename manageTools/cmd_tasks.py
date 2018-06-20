from django.core.exceptions import ObjectDoesNotExist

from PyLightCommon.cmdHandler.cmdHandler import cmd
from PyLightCommon.pylightcommon.models import UsedIO,IO,IOType,ConnectedSystem

@cmd
def addUsedIO(serialNumber):
    try:
        usedIO = UsedIO.objects.get(connectedSystem__serialNumber=serialNumber)
    except ObjectDoesNotExist:
        system = ConnectedSystem.objects.get(serialNumber=serialNumber)
        io = IO.objects.get(ioNr=0)
        ioType = IOType.objects.get(id=0)
        usedIO = UsedIO(name="",pin=io,type=ioType,connectedSystem=system)
        usedIO.save()
