#!/usr/bin/env bash
pip install --upgrade pip
pip install -r requirements.txt
python ./manage.py makemigrations
python ./manage.py migrate
python ./manage.py collectstatic --no-input
python ./manage.py runserver 0.0.0.0:8083
