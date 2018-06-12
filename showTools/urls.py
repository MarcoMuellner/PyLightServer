from django.urls import path

from . import views

urlpatterns = [
    path('', views.ConnectedSystemsView.as_view(), name='home'),
    path(r'base_layout',views.base_layout,name='base_layout'),
    path('state/<int:usedio_id>/', views.saveState, name='saveState'),
]