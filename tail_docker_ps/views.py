from django.shortcuts import render
from .models import Docker

# Create your views here.
# make ps_list View
def ps_list(request):
    dockerClass = Docker()
    docker_ps_list = dockerClass.ps_list()
    return render(request, 'tail_docker_ps/ps_list.html', {'docker_ps_list':docker_ps_list})