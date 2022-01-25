import os

from configurations import values

from .base import Base


class Local(Base):

    # SECRET_KEY = 'jch3we75+$xlesg8m_wd(2yuo&9dpr=zuw66xo1ga7jpkpey(2'
    SECRET_KEY = 'no_secret'
    # CSRF_COOKIE_SECURE = True
    # SESSION_COOKIE_SECURE = True
    # CSRF_COOKIE_SAMESITE = 'None'
    # SESSION_COOKIE_SAMESITE = 'None'

    DEBUG = values.BooleanValue(True)

    # ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1', 'web'])
    ALLOWED_HOSTS = ['127.0.0.1', 'klio.local.com']
    SESSION_COOKIE_DOMAIN = "klio.local.com"

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'debug_toolbar',
        'django_extensions',
    ]

    SESSION_COOKIE_HTTPONLY = False

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + Base.MIDDLEWARE

    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

    # EMAIL_HOST = os.getenv('EMAIL_HOST')
    # EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    # EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    # EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    # EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    EMAIL_HOST = 'klio.local.com'
    EMAIL_PORT = 2525
    # EMAIL_USE_TLS = "None"
    EMAIL_HOST_USER = ""
    EMAIL_HOST_PASSWORD = ""

    # DATABASES = values.DatabaseURLValue('postgres://postgres:postgres@localhost:5432/kliodamp')
    # DATABASES = values.DatabaseURLValue('postgres://postgres:postgres@localhost:5432/kliolocal')
    # DATABASES = values.DatabaseURLValue('postgres://postgres:postgres@localhost:5432/kliodbv2')
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'kliodamp',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': 'localhost',
            'PORT': '5432'
        }
    }

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True if values.BooleanValue(Local.DEBUG) else False,
    }

    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ORIGIN_WHITELIST = [
        "http://localhost:8080",
        "http://localhost:8081",
        "https://localhost:8080",
        "http://127.0.0.1:8080",
        "http://127.0.0.1:8000",
        "https://127.0.0.1:8080",
        "https://localhost:8080",
        "http://klio.local.com:8080",
    ]

    # for logger in Base.LOGGING['loggers']:
    #     Base.LOGGING['loggers'][logger]['handlers'] += ['console']

    Base.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
