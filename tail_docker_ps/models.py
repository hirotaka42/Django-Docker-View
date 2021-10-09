from django.conf import settings
from django.db import models
from django.utils import timezone
import docker

# Create your models here.

class Docker(models.Model):
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
        for docker_container_list in self.client.containers.list():
            tmp = {}
            CONTAINER = str(docker_container_list)
            CONTAINER_ID = CONTAINER[12:22]
            NAME = str(docker_container_list.name)
            tmp['CONTAINER_ID'] = CONTAINER_ID
            tmp['NAME'] = NAME
            docker_ps.append(tmp)

        return docker_ps

    


