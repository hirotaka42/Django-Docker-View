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

def ps_all_list(request):
    dockerClass = Docker()
    ps_all_list = dockerClass.ps_all_list()
    return render(request, 'tail_docker_ps/ps_all_list.html', {'ps_all_list':ps_all_list})


def logs_detail(request,container_id):
    """
    JQueryのnew EventSourceでEventとして呼ばれる (../templates/tail_docker_ps/logs_view.html内に記述)
    引数 container_id を 用いてコンテナのログを取得し
    StreamingHttpResponse で 取得、整形したlog一行分ずつを返却する
    """
    # docker インスタンス(client2)の作成
    client2 = docker.from_env()
    container = client2.containers.get(container_id)
    return StreamingHttpResponse(
        _stream_docker_logs(container),
        content_type='text/event-stream'
    )

def _stream_docker_logs(container):
    """
    log出力においてイテレータで文字列を返却してくれるが、１文字が返却される場合がある
    原因は不明だが要因として終端文字が'\r\n'や-json.logにおいて
    出力されたlogの内容によりエスケープが外れてしまうことが要因だと考えられる

    修正方法：
    文字はbytes型で来る。文字列ではなかった場合、これをスタックし終端文字列の'\n'をポイントとして
    スタックしたbeytesを文字コードUTF-8にデコード,str変換し文字列として返却
    """
    # since=datetime.utcfromtimestamp(time.time())
    # since オプションをつけてあげるとlogの出力期間を限定できる
    tmp = bytearray(b'')
    try:
        for line in container.logs(
                stream=True, tail=250, timestamps=True):

            if line != b'\n':
                #このブロックは正常な文字列と 単体文字列が混合している
                
                if len(line) > 10:
                    #正常な文字列の場合
                    yield 'data: {}\n\n'.format(line.decode("utf-8"))
                    time.sleep(0.001)
                else:
                    #異常文字列の場合 stack
                    tmp += bytes(line)
                
            elif line == b'\n':
                #完全な '\n'のみがヒットしたときの処理
                tmp += bytes(line)
                #stackしておいた文字列を返却
                yield 'data: {}\n\n'.format(str(tmp.decode("utf-8")))
                time.sleep(0.001)
                #返却後は初期化
                tmp = bytearray(b'')

    except docker.errors.APIError:
            yield 'data: このコンテナにはログがありません。\n\n'
            
