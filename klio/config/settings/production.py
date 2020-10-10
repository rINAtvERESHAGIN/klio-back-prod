import os

from configurations import values

from .base import Base


class Production(Base):

    DEBUG = values.BooleanValue(False)

    SECRET_KEY = 'jch3we75+$xlesg8m_wd(2yuo&9dpr=zuw66xo1ga7jpkpey(2'

    ALLOWED_HOSTS = [
        '45.80.71.10',
        'kliogem.ru'
    ]

    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('POSTGRES_DB'),
            'USER': os.getenv('POSTGRES_USER'),
            'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
            'HOST': os.getenv('POSTGRES_HOST'),
            'PORT': int(os.getenv('POSTGRES_PORT'))
        }
    }

    CORS_ORIGIN_WHITELIST = [
        "http://45.80.71.10:8081",
        "http://kliogem.ru",
        "https://kliogem.ru",
    ]
