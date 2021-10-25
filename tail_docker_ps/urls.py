from django.urls import path
from . import views
from django.views.generic.base import TemplateView
from .views import logs_detail

"""
tail_docker_ps > views.py からViewを参照
"""

urlpatterns = [
    path('', views.ps_list, name='ps_list'),
    path('docker/logs/<str:container_id>/', views.logs_detail, name='logs_detail'),
]