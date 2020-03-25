import os
from os.path import join

from configurations import Configuration, values


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    APPEND_SLASH = values.BooleanValue(False)

    INSTALLED_APPS = [
        # System Packages
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Third Party Packages
        'captcha',
        'cities_light',
        'corsheaders',
        'ckeditor',
        'rest_framework',

        # Own Packages
        'basket',
        'contacts',
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
            'DIRS': [],
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

    # CITIES LIGHT SETTINGS
    CITIES_LIGHT_TRANSLATION_LANGUAGES = ['ru']
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
