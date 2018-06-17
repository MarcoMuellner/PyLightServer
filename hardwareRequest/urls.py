from django.urls import path

from hardwareRequest.views import HardwareRequest

urlpatterns = [
    path('', HardwareRequest.as_view(), name='postHardware'),
]