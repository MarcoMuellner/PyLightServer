from django.urls import path

from . import views

urlpatterns = [
    path('', views.handleRequests, name='postHardware'),
]