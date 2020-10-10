import os

from configurations import values

from .base import Base


class Local(Base):

    SECRET_KEY = 'no_secret'

    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1', 'web'])

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        'debug_toolbar',
        'django_extensions',
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ] + Base.MIDDLEWARE

    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')

    EMAIL_HOST = os.getenv('EMAIL_HOST')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    # DATABASES = values.DatabaseURLValue('mysql://db_user:userpass@db:3306/database')
    DATABASES = values.DatabaseURLValue('postgres://postgres@db/postgres')

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True if values.BooleanValue(Local.DEBUG) else False,
    }

    CORS_ORIGIN_ALLOW_ALL = False

    CORS_ORIGIN_WHITELIST = [
        "http://localhost:8080",
        "http://127.0.0.1:8080",
    ]

    # for logger in Base.LOGGING['loggers']:
    #     Base.LOGGING['loggers'][logger]['handlers'] += ['console']

    Base.REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'].append('rest_framework.renderers.BrowsableAPIRenderer')
