# django-view-results-of-Docker

## Prerequisite

python >= 3.8

## Installation

## linux
```
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver localhost:9999
```

## Mac
```
$ python -m venv venv
$ . ./venv/bin/activate
$ python -m pip install --upgrade pip --user
$ pip install -r requirements.txt
$ python manage.py migrate
$ python manage.py runserver localhost:9999
```

## How to use

Access `/` to see its docker ps.
