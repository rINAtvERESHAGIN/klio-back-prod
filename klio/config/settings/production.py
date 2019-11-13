import os

from configurations import values

from .base import Base


class Production(Base):

    DEBUG = values.BooleanValue(False)

    SECRET_KEY = 'jch3we75+$xlesg8m_wd(2yuo&9dpr=zuw66xo1ga7jpkpey(2'

    ALLOWED_HOSTS = [
        '',
    ]

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
