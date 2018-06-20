from django.contrib import admin
from django.urls import include, path
import showTools
import manageTools

from PyLightCommon.Globals import *
from PyLightCommon.loghandler import setup_logging
import PyLightCommon.cmdHandler


urlpatterns = [
    path('', include('pwa.urls')),
    path('', include('showTools.urls')),
    path('showTools/', include(('showTools.urls','showTools'),namespace='showTools')),
    path('manageTools/', include(('manageTools.urls','manageTools'),namespace='manageTools')),
    path('cmdHandler/', include(('PyLightCommon.cmdHandler.urls','PyLightCommon.cmdHandler'),namespace='cmdHandler')),
    path('admin/', admin.site.urls),
    path(r'base_layout',showTools.views.base_layout),
    path(r'config_layout',manageTools.views.config_layout),
]

setup_logging()



