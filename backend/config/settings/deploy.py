from .base import *

SECRET_KEY = env('SECRET_KEY')

DEBUG = False

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default' : {
        'ENGINE' : 'django.db.backends.mysql',
        'NAME' : env('AWS_RDS_DB_NAME'),
        'USER' : 'root',
        'PASSWORD' : env('AWS_RDS_DB_PASSWORD'),
        'HOST' : env('AWS_RDS_DB_HOST'),
        'PORT' : env('AWS_RDS_DB_PORT'),
        
    }
}