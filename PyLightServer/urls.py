from django.contrib import admin
from django.urls import include, path
import showTools
import manageTools

urlpatterns = [
    path('', include('pwa.urls')),
    path('', include('showTools.urls')),
    path('showTools/', include('showTools.urls')),
    path('manageTools/', include('manageTools.urls')),
    path('hardwareRequest/', include('hardwareRequest.urls')),
    path('admin/', admin.site.urls),
    path(r'base_layout',showTools.views.base_layout,name='base_layout'),
    path(r'config_layout',manageTools.views.config_layout,name='config_layout'),
]