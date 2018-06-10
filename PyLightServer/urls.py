from django.contrib import admin
from django.urls import include, path
from showTools import views

urlpatterns = [
    path('', views.ConnectedSystemsView.as_view(), name='home'),
    path('manageTools/', include('manageTools.urls')),
    path('showTools/', include('showTools.urls')),
    path('hardwareRequest/', include('hardwareRequest.urls')),
    path('admin/', admin.site.urls),
]