import os
from hashlib import sha1 as sha_constructor
from os.path import join

from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    APPEND_SLASH = values.BooleanValue(False)

    SITE_ID = 1

    ADMINS = ('pythonchem1st@gmail.com',)

    # DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    #
    # EMAIL_HOST = os.getenv('EMAIL_HOST')
    # EMAIL_PORT = int(os.getenv('EMAIL_PORT'))
    # EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS')
    # EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
    # EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

    DEFAULT_FROM_EMAIL = 'pythonchem1st@gmail.com'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'pythonchem1st@gmail.com'
    EMAIL_HOST_PASSWORD = 'Fedo1702FG'

    INSTALLED_APPS = [
        'grappelli',  # should appear before 'django.contrib.admin'

        # System Packages
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',
        'django.contrib.postgres',

        # Third Party Packages
        'captcha',
        'cities_light',
        'corsheaders',
        'ckeditor',
        'ckeditor_uploader',
        'imagekit',
        'rest_framework',

        # Own Packages
        'basket',
        'contacts',
        'auth.apps.AuthConfig',
        'general',
        'products',
        'sale',
        'tags',
        'users',
    ]

    MIDDLEWARE = [
        'corsheaders.middleware.CorsMiddleware',
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ]

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                join(BASE_DIR, 'auth/templates'),
                join(BASE_DIR, 'general/templates'),
                join(BASE_DIR, 'products/templates')
            ],
            'APP_DIRS': values.BooleanValue(True),
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    ROOT_URLCONF = 'config.urls'

    WSGI_APPLICATION = 'config.wsgi.application'

    # Password validation
    # https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/2.2/topics/i18n/

    LANGUAGE_CODE = 'ru'

    LOCALE_PATHS = (join(BASE_DIR, 'locale'),)

    TIME_ZONE = 'Europe/Moscow'

    USE_I18N = values.BooleanValue(True)
    USE_L10N = values.BooleanValue(True)
    USE_TZ = values.BooleanValue(True)

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.2/howto/static-files/

    STATIC_URL = '/static/'

    # Static Files
    STATICFILES_DIRS = [
        join(BASE_DIR, 'static')
    ]

    STATIC_ROOT = join(os.path.dirname(BASE_DIR), 'static')

    STATICFILES_FINDERS = (
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

    # Media files
    MEDIA_URL = '/media/'

    MEDIA_ROOT = join(os.path.dirname(BASE_DIR), 'media')

    # Custom user app
    AUTH_USER_MODEL = 'users.User'

    REGISTRATION_SALT = sha_constructor(str(135793716).encode('utf-8')).hexdigest()[:5]

    ACCOUNT_ACTIVATION_DAYS = 7
    PASSWORD_RESET_DAYS = 3

    # REST FRAMEWORK
    REST_FRAMEWORK = {
        'DEFAULT_RENDERER_CLASSES': [
            'rest_framework.renderers.JSONRenderer',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        ],
        'PAGE_SIZE': 25
    }

    # SESSION_SAVE_EVERY_REQUEST = True

    CORS_ALLOW_CREDENTIALS = True

    DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

    # CITIES LIGHT SETTINGS
    CITIES_LIGHT_TRANSLATION_LANGUAGES = ['en', 'ru']
    CITIES_LIGHT_INCLUDE_COUNTRIES = ['RU']
    CITIES_LIGHT_INCLUDE_CITY_TYPES = ['PPL', 'PPLA', 'PPLA2', 'PPLA3', 'PPLA4', 'PPLC', 'PPLF', 'PPLG',
                                       'PPLL', 'PPLR', 'PPLS', 'STLMT', ]

    # CKEDITOR SETTINGS
    CKEDITOR_CONFIGS = {
        'default': {
            'toolbar': [
                ['Undo', 'Redo',
                 '-', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'
                                                               '-', 'Link', 'Unlink', 'Anchor', 'Format',
                 '-', 'Maximize',
                 '-', 'Table',
                 '-', 'Image',
                 '-', 'Source',
                 '-', 'NumberedList', 'BulletedList'
                 ],
                ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
                 'Font', 'FontSize', 'TextColor',
                 '-', 'Outdent', 'Indent',
                 '-', 'HorizontalRule',
                 '-', 'Blockquote'
                 ]
            ],
            'height': 200,
            'width': '100%',
            'toolbarCanCollapse': False,
            'forcePasteAsPlainText': True
        },
        'user_mode': {
            'toolbar': [
                ['Undo', 'Redo',
                 '-', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'
                                                               '-', 'Link', 'Unlink',
                 '-', 'Table',
                 '-', 'Image',
                 '-', 'NumberedList', 'BulletedList',
                 '-', 'HorizontalRule',
                 '-', 'Blockquote'
                 ]
            ],
            'height': 300,
            'width': '100%',
            'toolbarCanCollapse': False,
            'forcePasteAsPlainText': True
        }
    }

    CKEDITOR_UPLOAD_PATH = "ckeditor_uploads/"
    # Best 2 Pay Settings:
    B2P_SECTOR = os.getenv('B2P_SECTOR')
    B2P_SECRET = os.getenv('B2P_SECRET')
    B2P_BASE_URL = os.getenv('B2P_BASE_URL')
    B2P_FAIL_REDIRECT = os.getenv('B2P_FAIL_REDIRECT')
    B2P_SUCCESS_REDIRECT = os.getenv('B2P_SUCCESS_REDIRECT')
