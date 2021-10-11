from .models import Docker
from django.shortcuts import render
import docker
from django.http import StreamingHttpResponse
import time
from datetime import datetime

# Create your views here.
# make ps_list View
def ps_list(request):
    dockerClass = Docker()
    docker_ps_list = dockerClass.ps_list()
    return render(request, 'tail_docker_ps/ps_list.html', {'docker_ps_list':docker_ps_list})

def logs_detail(request,container_id):
    """
    引数 container_id を tail_docker_ps/logs_view.html へ渡し、
    logs_detail ページを render する 
    """
    # docker インスタンス(client2)の作成
    client2 = docker.from_env()
    container = client2.containers.get(container_id)
    return StreamingHttpResponse(
        _stream_docker_logs(container),
        content_type='text/event-stream'
    )
    # return render(request, 'tail_docker_ps/logs_view.html', {'container_id': container_id})

def _stream_docker_logs(container):
    # , since=datetime.utcfromtimestamp(time.time())
    # stream=True 後にsince オプションをつけてあげると出力を限定できる
    for line in container.logs(
            stream=True):
        yield 'data: {}\n\n'.format(line.decode('utf-8'))
        time.sleep(0.1)