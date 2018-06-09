from django.urls import path

from . import views

urlpatterns = [
    path('', views.ConnectedSystemsView.as_view(), name='index'),
    path('system/<int:connectedSystem_id>/', views.saveSystem, name='saveSystem'),
    path('io/<int:usedio_id>/', views.saveIO, name='saveIO'),
]