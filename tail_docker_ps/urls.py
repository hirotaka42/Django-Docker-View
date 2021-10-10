from django.urls import path
from . import views

"""
tail_docker_ps > views.py からViewを参照
"""

urlpatterns = [
    path('', views.ps_list, name='ps_list'),
]