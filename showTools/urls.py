from django.urls import path

from . import views

urlpatterns = [
    path('', views.ConnectedSystemsView.as_view(), name='index'),
    path('state/<int:usedio_id>/', views.saveState, name='saveState'),
]