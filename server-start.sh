#!/bin/bash
HOME_LOCATION=/home/ubuntu/
REPOSITORY=/home/ubuntu/build/ 

cd $HOME_LOCATION
source server/bin/activate

cd $REPOSITORY

export DJANGO_SETTINGS_MODULE=backend.config.settings.deploy
python manage.py makemigrations
python manage.py migrate
screen -d -m python manage.py runserver
