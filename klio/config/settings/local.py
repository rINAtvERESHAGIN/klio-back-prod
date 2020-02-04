from configurations import values

from .base import Base


class Local(Base):

    SECRET_KEY = 'no_secret'

    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue(['localhost', '127.0.0.1', 'web'])

    INSTALLED_APPS = Base.INSTALLED_APPS + [
        # 'corsheaders',
        'debug_toolbar',
        'django_extensions',
    ]

    MIDDLEWARE = [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        # 'corsheaders.middleware.CorsMiddleware',
    ] + Base.MIDDLEWARE

    # DATABASES = values.DatabaseURLValue('mysql://db_user:userpass@db:3306/database')
    DATABASES = values.DatabaseURLValue('postgres://postgres@db/postgres')

    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda request: True if values.BooleanValue(Local.DEBUG) else False,
    }

    # CORS_ORIGIN_WHITELIST = [
    #     "http://localhost:8080",
    # ]

    # for logger in Base.LOGGING['loggers']:
    #     Base.LOGGING['loggers'][logger]['handlers'] += ['console']
