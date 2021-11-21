# Django-View-Results-of-Docker
![Docker-View](https://user-images.githubusercontent.com/79750434/140269687-8dde9527-72e3-4acc-aab4-6e3bcdee82b5.png)
![Logs_View](https://user-images.githubusercontent.com/79750434/140269733-7ff1a824-eb55-4819-aa5e-e9cf8756727b.png)
## Prerequisite

python >= 3.8

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
# venv を有効化
python -m venv venv
. ./venv/bin/activate
```

```
# venv内の pipをアップグレード
python3 -m pip install --upgrade pip
# モジュール の install 
pip install -r requirements.txt

python3 manage.py migrate
python3 manage.py runserver localhost:9999
```

## How to use

Access `/` to see its docker ps.

