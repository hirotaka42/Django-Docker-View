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
    tmp = []
    for line in container.logs(
            stream=True, tail=5):
        #num = line
        #str_num = str(num)
        
        if line != b'\n':
            #ここには 正常な文字列と 単体文字列が混合している
            
            if len(line) > 10:
                #正常な文字列の場合
                yield 'data: {}\n\n'.format(line.decode("utf-8"))
                time.sleep(0.1)
            else:
                #異常文字列の場合 stack
                tmp.append(str(line.decode("utf-8")))
                #yield 'data: {}\n\n'.format(str_num.decode("utf-8"))
            
        elif line == b'\n':
            #ここは　完全な '\n'のみがヒットしたときの処理
            yield 'data: {}\n\n'.format(str(tmp))
            yield 'data: {}\n\n'.format("################################################")
            time.sleep(0.1)
            tmp = []

        else :
            pass
            time.sleep(1)
