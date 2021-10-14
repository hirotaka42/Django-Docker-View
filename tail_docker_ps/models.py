from django.conf import settings
from django.db import models
from django.utils import timezone
import docker

# Create your models here.

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
        #client = docker.from_env()
        #Client = self.client
        docker_containers = self.client.containers.list()
        for container in docker_containers:
            tmp = {}
            CONTAINER = str(container)
            tmp['CONTAINER_ID'] = CONTAINER[12:22]
            tmp['IMAGE'] = container.attrs['Config']['Image']
            tmp['COMMAND'] = container.attrs['Config']['Entrypoint'][0]
            tmp['CREATED'] = 'CREATED'
            tmp['STATUS'] = 'STATUS'
            PORTS = container.attrs['NetworkSettings']['Ports']
            for key in PORTS:
                PORT = key
            tmp['PORT'] = PORT
            tmp['NAME'] = str(container.name)
            docker_ps.append(tmp)
            

        return docker_ps

    


