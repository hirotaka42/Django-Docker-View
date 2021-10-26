from .models import Docker
from django.shortcuts import render
import docker       # _stream_docker_logs関数で使用
from django.http import StreamingHttpResponse
import time
from datetime import datetime
from django.views.generic import TemplateView

# Create your views here.
def is_check_int(args):
    """
    文字列が整数かどうかの判定
    """
    try:
        int(args)
        return True
    except ValueError:
        return False

# make Class
class Index(TemplateView):

    #テンプレートファイル連携
    template_name = 'tail_docker_ps/logs_view.html'

    

    #変数を渡す
    def get_context_data(self,**kwargs):
         context = super().get_context_data(**kwargs)
         context["CONTAINER_ID"] = self.kwargs['container_id']
         dockerClass = Docker()
         context["IMAGE"] = dockerClass.is_get_image_from_id(self.kwargs['container_id'])
         context["NAME"] = dockerClass.is_get_name_from_id(self.kwargs['container_id'])
         context["PORT"] = dockerClass.is_get_port_from_id(self.kwargs['container_id'])
         context["tail"] = self.kwargs['tail']
         return context

    #get処理
    def get(self, request, *args, **kwargs):
        if 'tail' in request.GET:
            check_int = is_check_int(request.GET.get('tail'))
            # 文字列が数以外ならデフォルト値をセット
            if (check_int):
                tail = str(request.GET.get('tail'))
                self.kwargs['tail'] = int(tail.lower())
            else:
                # デフォルト値の設定
                self.kwargs['tail'] = 20
        else :
            # デフォルト値の設定
            self.kwargs['tail'] = 20

        return super().get(request, *args, **kwargs)

    #post処理
    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, context=self.kwargs)


# make ps_list View
def ps_list(request):
    dockerClass = Docker()

    if request.GET.get('a')=='1' or request.GET.get('a')=='１':
        docker_ps_list = dockerClass.ps_all_list()
    else:
        docker_ps_list = dockerClass.ps_list()

    return render(request, 'tail_docker_ps/ps_list.html', {'docker_ps_list':docker_ps_list})


def logs_detail(request,container_id):
    """
    JQueryのnew EventSourceでEventとして呼ばれる (../templates/tail_docker_ps/logs_view.html内に記述)
    引数 container_id を 用いてコンテナのログを取得し
    StreamingHttpResponse で 取得、整形したlog一行分ずつを返却する
    """
    # docker インスタンス(client2)の作成
    client2 = docker.from_env()
    container = client2.containers.get(container_id)
    if 'tail' in request.GET:
        return StreamingHttpResponse(
        _stream_docker_logs(container,is_get_tail=request.GET.get('tail')),
        content_type='text/event-stream')
    elif 'tail' not in request.GET:
        return StreamingHttpResponse(
        _stream_docker_logs(container,is_get_tail=5),
        content_type='text/event-stream')

    

def _stream_docker_logs(container, is_get_tail):
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
                stream=True, tail=int(is_get_tail), timestamps=True):

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
            

