# Django-Docker-View

## Overview
Dockerコンテナ情報をWeb経由で確認することが出来ます。
localhostを超えて公開した場合、誰にでもログ情報が見えてしまうので注意してください。

***DEMO:***

iPhone(Safari) | Web(Chrome) | Web(Chrome)
:-------------------------:|:-------------------------:|:-------------------------:
![RPReplay_Final1638301361](https://user-images.githubusercontent.com/79750434/144117760-240c120b-093c-4b44-94a2-1c513ded6280.gif) | ![Docker-View](https://user-images.githubusercontent.com/79750434/140269687-8dde9527-72e3-4acc-aab4-6e3bcdee82b5.png) | ![Logs_View](https://user-images.githubusercontent.com/79750434/140269733-7ff1a824-eb55-4819-aa5e-e9cf8756727b.png)
## Prerequisite

- python >= 3.8
- Docker already running


## Installation

## linux (Ubuntuで確認済)
```
python -m venv venv
. ./venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver localhost:9999
```

## Mac
```
# git clone
git clone https://github.com/hirotaka42/Django-Docker-View.git
cd Django-Docker-View

# venv(仮想環境) を作成
python3 -m venv venv

# venv を有効化
. ./venv/bin/activate
# もしくわ
source ./venv/bin/activate

# venv内の pipをアップグレード
python3 -m pip install --upgrade pip
# モジュール の install 
pip install -r requirements.txt

# 初回起動時のみ マイグレーションが必要
python3 manage.py migrate
# 起動
python3 manage.py runserver localhost:9999

# 2回目以降 (venv有効化し、実行)
source ./venv/bin/activate
python3 manage.py runserver localhost:9999
```

## mac 一括実行(コピペ用)
```
# git clone
git clone https://github.com/hirotaka42/Django-Docker-View.git
cd Django-Docker-View

# venv(仮想環境) を作成
python3 -m venv venv && \
source ./venv/bin/activate && \
python3 -m pip install --upgrade pip && \
pip install -r requirements.txt && \
python3 manage.py migrate

# 実行
python3 manage.py runserver localhost:9999

# 終了したら仮想環境を終了
deactivate

# 2回目以降 (venv有効化し、実行)
source ./venv/bin/activate
python3 manage.py runserver localhost:9999
```

## How to use

- Access `/` to see its docker ps.    
[http://localhost:9999/](http://localhost:9999/)

- If you want to allow access from other PCs.

```
# Edit `Django-Docker-View/tail_docker/settings.py`
#`ALLOWED_HOSTS = ['My IP Address']`

# Run
python manage.py runserver [MyIP]:8000
```

Edit ./tail_docker/settings.py | Run
:-------------------------:|:-------------------------:
![vscode](https://user-images.githubusercontent.com/79750434/144116094-c0de7e4f-1fe9-4d38-a446-dbbc427c671d.png) | ![ターミナル](https://user-images.githubusercontent.com/79750434/144116521-960c2176-ace7-4233-96ee-c9643f4d2c11.png)
