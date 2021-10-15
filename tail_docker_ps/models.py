from django.conf import settings
from django.db import models
from django.utils import timezone
import docker
import datetime

# Create your models here.
def getPastDay(y, m, d):
    return (datetime.date.today() - datetime.datetime(year=y,month=m,day=d).date()).days

def ps_created(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の CREATEDの値を返却する

    """
    time_tmp = []
    str_y = ' years ago'
    str_w = ' weeks ago'
    str_d = ' days ago'
    str_h = ' hours ago'
    str_min = ' minutes ago'
    str_sec = ' seconds ago'

    if str(container.attrs['Created']) is None:
        CREATED = 'None'
    else:
        created = container.attrs['Created']
        time_tmp = int(getPastDay(int(created[:4]), int(created[5:7]), int(created[8:10])))
        if time_tmp > 365:
            #年表示
            tmp_years = int(time_tmp / 360)
            CREATED = str(tmp_years) + str_y
        elif time_tmp > 30:
            #月表示
            tmp_moth = int(time_tmp / 30)
            CREATED = str(time_tmp)
        elif time_tmp > 7:
            tmp_weeks = int(time_tmp / 7)
            if tmp_weeks < 1:
                #週間表示
                CREATED = str(time_weeks) + str_w
        elif time_tmp > 1:
            #日にち表示
            CREATED = str(time_tmp) + str_d
        else:
            # 1日以下なら hour, minutes, seconds,
            CREATED = '1日以下なら hour, minutes, seconds,'


    return CREATED

def ps_port(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の PORTSの値を返却する

    """
    pk_tmp = []
    if str(container.attrs['NetworkSettings']['Ports']) is None:
        PORT = ''
    else:
        PORTS = container.attrs['NetworkSettings']['Ports']
        # dictに格納されている最初の値を取得
        PORT_Key1 = next(iter(PORTS.keys()))

        if PORTS[PORT_Key1] is None:
            # # ポートフォワーディング設定が無く、要素が１つの場合
            # 40772/tcp 
            PORT = PORT_Key1
        else:
            # ポートフォワーディング設定がある場合
            if len(PORTS.keys()) > 1:
                # 1つ以上要素がある場合
                # 9229/tcp, 0.0.0.0:40772->40772/tcp,
                for PK in PORTS.keys():
                    pk_tmp.append(PK)
                    
                #尚且つ,2つ要素がある場合
                if len(PORTS[PORT_Key1]) > 1:
                    str_port_first = pk_tmp[1] + ', ' + PORTS[PORT_Key1][0]['HostIp'] + ':' + PORTS[PORT_Key1][0]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    str_port_secnd = ', ' + PORTS[PORT_Key1][1]['HostIp'] + ':' + PORTS[PORT_Key1][1]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    PORT = str_port_first + str_port_secnd
                #1つ要素がある場合
                else:
                    str_port = pk_tmp[1] + ', ' + PORTS[PORT_Key1][0]['HostIp'] + ':' + PORTS[PORT_Key1][0]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    PORT = str_port
            else:
                # 0.0.0.0:40772->40772/tcp 
                #尚且つ,2つ要素がある場合
                if len(PORTS[PORT_Key1]) > 1:
                    str_port_first = PORTS[PORT_Key1][0]['HostIp'] + ':' + PORTS[PORT_Key1][0]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    str_port_secnd = ', ' + PORTS[PORT_Key1][1]['HostIp'] + ':' + PORTS[PORT_Key1][1]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    PORT = str_port_first + str_port_secnd
                #1つ要素がある場合
                else:
                    str_port = PORTS[PORT_Key1][0]['HostIp'] + ':' + PORTS[PORT_Key1][0]['HostPort'] + '->' + next(iter(PORTS.keys()))
                    PORT = str_port
                
            
    # PORT出力設定　ここまで
    return PORT


class Docker():
    # dockerインスタンス作成
    client = docker.from_env()

    def images(self) -> list:
        """
        dockerイメージリストの取得
        <class 'list'>
        return [<Image: 'ImageName'>, <Image: 'ImageName'>]
        """
        return self.client.images.list()

    def containers(self) -> list:
        """
        起動済みの dockerコンテナID(10桁)リストの取得
        <class 'list'>
        return [<Container: ed98a9a688>, <Container: 4f02ce3412>]
        """
        return self.client.containers.list()

    
    def ps_list(self) -> list:
        """
        起動済みの docker コンテナID と NAME の取得
        <class 'list'>
        return [{'CONTAINER_ID': 'ed98a9a688', 'NAME': 'docker-wp_wordpress_1'}, 
         {'CONTAINER_ID': '4f02ce3412', 'NAME': 'docker-wp_db_1'}]

        """
        docker_ps = []
        docker_containers = self.client.containers.list()
        for container in docker_containers:
            tmp = {}
            CONTAINER = str(container)
            tmp['CONTAINER_ID'] = CONTAINER[12:22]
            tmp['IMAGE'] = container.attrs['Config']['Image']
            tmp['COMMAND'] = container.attrs['Config']['Entrypoint'][0]
            tmp['CREATED'] = ps_created(container)
            tmp['STATUS'] = 'STATUS'
            tmp['PORT'] = ps_port(container)
            tmp['NAME'] = str(container.name)
            docker_ps.append(tmp)
            

        return docker_ps

    


