# django-view-results-of-Docker

## Prerequisite

python >= 3.8

## Installation

```
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver 192.168.0.13:9999
```

## How to use

Access `/` to see its docker ps.
