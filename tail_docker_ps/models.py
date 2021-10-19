from django.conf import settings
from django.db import models
#from django.utils import timezone
import docker
import datetime
from pytz import timezone

# Create your models here.

def is_GetElapsedDays(years, months, days, hours, minits, seconds):
    '''
    経過日時を現在日時と引数で計算し返却します

    一般的にdockerコンテナ内のタイムゾーンは'UTC'になっています。
    タイムゾーンがJSTに変更されているコンテナの場合
    時差を追うプログラムは組んでいないため表示がずれる可能性があります。
    https://note.nkmk.me/python-datetime-isoformat-fromisoformat/
    https://docs.python.org/ja/3/library/datetime.html
    '''
    #現在日時の取得 #docker コンテナのCreated値は'UTC'で定義されている
    dt_now = datetime.datetime.now(timezone('UTC'))
    #".isoformat()"メソッドを用いて日時フォーマットを文字列に変換
    is_dt_now = dt_now.isoformat()

    dt1 = datetime.datetime(years, months, days, hours, minits, seconds)
    dt2 = datetime.datetime(int(is_dt_now[:4]), int(is_dt_now[5:7]), int(is_dt_now[8:10]), int(is_dt_now[11:13]), int(is_dt_now[14:16]), int(is_dt_now[17:19]))
    td1 = dt2 - dt1

    #datetimeにより以下を取り出せ使用できる:
    #インスタンスの属性 (読み出しのみ):
    #td1.days 
    #td1.seconds
    #td1.microseconds 
    return td1

def is_Time_Calculation(seconds:int,viewflag:int)->str:
    """
    コンテナの経過時間を文字列で返却
    args: seconds:現時刻との差分の秒数    viewflag: 0-CREATED  1-STATUS
    return: 
    """
    is_Elapsed_time = seconds
    is_Elapsed_minits_time = int(is_Elapsed_time / 60)
    is_Elapsed_hours_time = int(is_Elapsed_minits_time / 60)
    
    
    if is_Elapsed_hours_time >= 1:
        # 一時間以上経過している場合
        if is_Elapsed_hours_time == 1:
            tmp = 'About an' +' hours'
        else:
            tmp = str(is_Elapsed_hours_time ) +' hours'
            
    else:
        # 一時間以内なら分数を返却
        if is_Elapsed_minits_time == 1:
            tmp = 'About a' + ' minutes'
        elif is_Elapsed_minits_time > 1:
            tmp = str(is_Elapsed_minits_time) +' minutes'
        else:
            tmp = str(is_Elapsed_time) +' seconds'

    if viewflag == 0:
        return tmp + ' ago'
    else :
        return tmp


def ps_created(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の CREATEDの値を返却する

    """
    days_tmp = []
    str_y = ' years ago'
    str_m = ' months ago'
    str_w = ' weeks ago'
    str_d = ' days ago'


    if str(container.attrs['Created']) is None:
        CREATED = 'None'
    else:
        is_created_dt = container.attrs['Created']
        # datetimeメソッドを用いて日時の差分を計算
        td1 = is_GetElapsedDays(int(is_created_dt[:4]), int(is_created_dt[5:7]), int(is_created_dt[8:10]), int(is_created_dt[11:13]), int(is_created_dt[14:16]), int(is_created_dt[17:19]))
        days_tmp = int(td1.days)
        if days_tmp > 365:
            #年表示
            tmp_years = int(days_tmp / 360)
            CREATED = str(tmp_years) + str_y
        elif days_tmp > 30:
            #月表示
            tmp_moth = int(days_tmp / 30)
            CREATED = str(tmp_moth) + str_m
        elif days_tmp > 10:
            tmp_weeks = int(days_tmp / 7)
            #週間表示
            if tmp_weeks == 1:
                CREATED = str(tmp_weeks) + ' week ago'
            else:
                CREATED = str(tmp_weeks) + str_w
        elif days_tmp > 2:
            #日にち表示
            CREATED = str(days_tmp) + str_d
        else:
            # 2日以下なら hour, minutes, seconds,
            if days_tmp > 0:
                # 1日以上なら１日分の秒数を追加
                is_Elapsed_time = int(td1.seconds) + 86400*int(days_tmp)
                CREATED = is_Time_Calculation(is_Elapsed_time,viewflag=0)
            else:
                is_Elapsed_time = int(td1.seconds)
                CREATED = is_Time_Calculation(is_Elapsed_time,viewflag=0)


    return CREATED


def ps_status(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の STATUSの値を返却する

    """
    days_tmp = []
    str_y = ' years'
    str_m = ' months'
    str_w = ' weeks'
    str_d = ' days'

    if str(container.attrs['State']['StartedAt']) is None:
        CREATED = 'None'
    else:
        is_State_StartedAt_dt = container.attrs['State']['StartedAt']
        # datetimeメソッドを用いて日時の差分を計算
        td1 = is_GetElapsedDays(int(is_State_StartedAt_dt[:4]), int(is_State_StartedAt_dt[5:7]), int(is_State_StartedAt_dt[8:10]), int(is_State_StartedAt_dt[11:13]), int(is_State_StartedAt_dt[14:16]), int(is_State_StartedAt_dt[17:19]))
        days_tmp = int(td1.days)
        if days_tmp > 365:
            #年表示
            tmp_years = int(days_tmp / 360)
            CREATED = str(tmp_years) + str_y
        elif days_tmp > 30:
            #月表示
            tmp_moth = int(days_tmp / 30)
            CREATED = str(days_tmp) + str_m
        elif days_tmp > 10:
            tmp_weeks = int(days_tmp / 7)
            #週間表示
            if tmp_weeks == 1:
                CREATED = str(tmp_weeks) + ' week'
            else:
                CREATED = str(tmp_weeks) + str_w
        elif days_tmp > 2:
            #日にち表示
            CREATED = str(days_tmp) + str_d
        else:
            # 2日以下なら hour, minutes, seconds,
            if days_tmp > 0:
                # 1日以上なら１日分の秒数を追加
                is_Elapsed_time = int(td1.seconds) + 86400*int(days_tmp)
                CREATED = is_Time_Calculation(is_Elapsed_time,viewflag=1)
            else:
                is_Elapsed_time = int(td1.seconds)
                CREATED = is_Time_Calculation(is_Elapsed_time,viewflag=1)


    return 'Up ' + CREATED


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
            tmp['STATUS'] = ps_status(container)
            tmp['PORT'] = ps_port(container)
            tmp['NAME'] = str(container.name)
            docker_ps.append(tmp)
            

        return docker_ps

    def ps_all_list(self) -> list:
        """
        起動済みの docker コンテナID と NAME の取得
        <class 'list'>
        return [{'CONTAINER_ID': 'ed98a9a688', 'NAME': 'docker-wp_wordpress_1'}, 
         {'CONTAINER_ID': '4f02ce3412', 'NAME': 'docker-wp_db_1'}]

        """
        docker_ps = []
        docker_containers = self.client.containers.list(all=True)
        for container in docker_containers:
            tmp = {}
            CONTAINER = str(container)
            tmp['CONTAINER_ID'] = CONTAINER[12:22]
            tmp['IMAGE'] = container.attrs['Config']['Image']
            tmp['COMMAND'] = 'COMMAND'
            tmp['CREATED'] = ps_created(container)
            tmp['STATUS'] = 'STATUS'
            tmp['PORT'] = 'PORT'
            tmp['NAME'] = str(container.name)
            docker_ps.append(tmp)
            

        return docker_ps

