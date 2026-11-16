#!/usr/bin/env bash

sudo fuser -k 8090/tcp
lsof -i :8083 | awk '/[1-9]/ {print $2}' | xargs kill -9
rm /home/zaffarelli/Projects/github/dragonade/dragonade_media/pdf/results/stregoneria/*.svg
rm /home/zaffarelli/Projects/github/dragonade/dragonade_media/pdf/results/viaggiatore_spells/*.svg

#pip install --upgrade pip
#pip install -r requirements.txt
uv run ./manage.py makemigrations
uv run ./manage.py migrate
uv run ./manage.py collectstatic --no-input
uv run ./manage.py test && uv run ./manage.py runserver 0.0.0.0:8083
