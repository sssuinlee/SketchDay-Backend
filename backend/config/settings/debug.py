from .base import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : 'sketch_day',
        'USER' : 'root',
        'PASSWORD' : env('PASSWORD'),
        'HOST' : '127.0.0.1',
        'PORT' : '3306'
        
    }
}