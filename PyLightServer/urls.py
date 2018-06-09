from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('manageTools/', include('manageTools.urls')),
    path('showTools/', include('showTools.urls')),
    path('admin/', admin.site.urls),
]