from django.contrib import admin
from django.urls import include, path
from showTools import views

urlpatterns = [
    path('', include('pwa.urls')),
    path('', include('showTools.urls')),
    path('showTools/', include('showTools.urls')),
    path('manageTools/', include('manageTools.urls')),
    path('hardwareRequest/', include('hardwareRequest.urls')),
    path('admin/', admin.site.urls),
    path(r'base_layout',views.base_layout,name='base_layout'),
]