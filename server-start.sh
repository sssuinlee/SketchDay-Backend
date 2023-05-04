#!/bin/bash
HOME_LOCATION=/home/ubuntu/
REPOSITORY=/home/ubuntu/build/ 

cd $REPOSITORY
source server/bin/activate

export DJANGO_SETTINGS_MODULE=backend.config.settings.deploy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
