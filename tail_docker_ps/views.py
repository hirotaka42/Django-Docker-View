from .models import Docker
from django.shortcuts import render, get_object_or_404
from .models import Docker

# Create your views here.
# make ps_list View
def ps_list(request):
    dockerClass = Docker()
    docker_ps_list = dockerClass.ps_list()
    return render(request, 'tail_docker_ps/ps_list.html', {'docker_ps_list':docker_ps_list})

def logs_detail(request, pk):
    docker_id = get_object_or_404(Docker, container_id=container_id)
    return render(request, 'tail_docker_ps/logs_view.html', {'docker_id': docker_id})