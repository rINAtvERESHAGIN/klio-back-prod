import os


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

from configurations.wsgi import get_wsgi_application  # noqa

application = get_wsgi_application()
