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

def is_Time_Calculation(seconds:int)->str:
    """
    コンテナの経過時間を文字列で返却
    args: seconds:現時刻との差分の秒数  
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

    return tmp




def is_CalculateContainerInfo(container,selectflag:int)->str:
    """
    コンテナの経過時間を文字列で返却
    args: seconds:現時刻との差分の秒数    viewflag: 0-CREATED  1-STATUS  2-FinishedAt
    return: 
    """
    days_tmp = []
    str_y = ' years'
    str_m = ' months'
    str_w = ' weeks'
    str_d = ' days'

    if selectflag == 0:
        is_select_info = container.attrs['Created']
    elif selectflag == 1:
        is_select_info = container.attrs['State']['StartedAt']
    elif selectflag == 2:
        is_select_info = container.attrs['State']['FinishedAt']


    if str(is_select_info) is None:
        str_tmp = 'None'
    else:
        # datetimeメソッドを用いて日時の差分を計算
        td1 = is_GetElapsedDays(int(is_select_info[:4]), int(is_select_info[5:7]), int(is_select_info[8:10]), int(is_select_info[11:13]), int(is_select_info[14:16]), int(is_select_info[17:19]))
        days_tmp = int(td1.days)
        if days_tmp > 730:
            #年表示
            tmp_years = int(days_tmp / 360)
            str_tmp = str(tmp_years) + str_y
        elif days_tmp > 30:
            #月表示
            tmp_moth = int(days_tmp / 30)
            str_tmp = str(tmp_moth) + str_m
        elif days_tmp > 13:
            tmp_weeks = int(days_tmp / 7)
            #週間表示
            if tmp_weeks == 1:
                str_tmp = str(tmp_weeks) + ' week'
            else:
                str_tmp = str(tmp_weeks) + str_w
        elif days_tmp > 1:
            #日にち表示
            str_tmp = str(days_tmp) + str_d
        else:
            # 2日以下なら hour, minutes, seconds,
            if days_tmp > 0:
                # 1日以上なら１日分の秒数を追加
                is_Elapsed_time = int(td1.seconds) + 86400*int(days_tmp)
                str_tmp = is_Time_Calculation(is_Elapsed_time)
            else:
                is_Elapsed_time = int(td1.seconds)
                str_tmp = is_Time_Calculation(is_Elapsed_time)

    if selectflag == 0:
        return str_tmp 
    elif selectflag == 1:
        return 'Up ' + str_tmp
    elif selectflag == 2:
        return str_tmp


def ps_image(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の IMAGEの値を返却する

    """

    if container.attrs['Config']['Image'][:6] == 'sha256':
        image_tmp = container.attrs['Config']['Image'][7:19]
    else:
        image_tmp = container.attrs['Config']['Image']

    return image_tmp


def ps_cmd(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の cmdの値を返却する

    """

    if container.attrs['Config']['Entrypoint'] is None:
        str_tmp = ' '.join(container.attrs['Config']['Cmd'])
    else:
        str_tmp = ' '.join(container.attrs['Config']['Entrypoint'])

    # 最大19文字表示のため19文字をスライス
    if len(str_tmp) > 19:
            tmp = str_tmp[0:18] + '…'
    else :
        tmp = str_tmp

    return str(tmp)
    

    
def ps_created(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の CREATEDの値を返却する
    return str_tmp + ' ago'

    """
    return is_CalculateContainerInfo(container,0)

def ps_finishAt(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の STATUS表示のExitedに必要な終了した日時の値を返却する
    return str_tmp + ' ago'

    """
    return is_CalculateContainerInfo(container,2)



def ps_status(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の STATUSの値を返却する
    Args : container

    """
    is_status = container.attrs['State']['Status']
    if is_status == 'running':
        is_str_tmp = is_CalculateContainerInfo(container,1)
    elif is_status == 'exited':
        is_str_tmp = 'Exited (0) ' + ps_finishAt(container) + ' ago'
    elif is_status == 'created':
        is_str_tmp = 'Created '
    elif is_status == 'restarting':
        is_str_tmp = 'Restarting'

    return is_str_tmp


def ps_port(container) -> str:
    """
    引数のコンテナ情報からdocker ps 出力時の PORTSの値を返却する

    """
    pk_tmp = []
    if len(container.attrs['NetworkSettings']['Ports']) < 1:
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
        起動済みの dockerコンテナID(10桁)リスト付きの文字列(23文字-内訳12-22-23)の取得
        <class 'list'>
        return [<Container: ed98a9a688>, <Container: 4f02ce3412>]
        """
        return self.client.containers.list()

    def is_get_name_from_id(self,id:str) -> str:
        """
        コンテナIDからコンテナ名を取得する
        """
        return self.client.containers.get(id).name

    def is_get_image_from_id(self,id:str) -> str:
        """
        コンテナIDからコンテナイメージ名を取得する
        """
        return ps_image(self.client.containers.get(id))
    def is_get_port_from_id(self,id:str) -> str:
        """
        コンテナIDからポート詳細を取得する
        """
        return ps_port(self.client.containers.get(id))


    
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
            tmp['IMAGE'] = ps_image(container)
            tmp['COMMAND'] = ps_cmd(container)
            tmp['CREATED'] = ps_created(container) + ' ago'
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
            tmp['IMAGE'] = ps_image(container)
            tmp['COMMAND'] = ps_cmd(container)
            tmp['CREATED'] = ps_created(container) + ' ago'
            tmp['STATUS'] = ps_status(container)
            tmp['PORT'] = ps_port(container)
            tmp['NAME'] = str(container.name)
            docker_ps.append(tmp)
            

        return docker_ps

