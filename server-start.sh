#!/bin/bash
HOME_LOCATION=/home/ubuntu/
ENV_LOCATION=/home/ubuntu/env/
REPOSITORY=/home/ubuntu/build/ 

cd $ENV_LOCATION
cp .env ../build/

cd $REPOSITORY
source server/bin/activate

export DJANGO_SETTINGS_MODULE=backend.config.settings.deploy
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
