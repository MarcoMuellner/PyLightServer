from django.urls import path

from . import views

urlpatterns = [
    path('state/<int:usedio_id>/', views.saveState, name='saveState'),
]