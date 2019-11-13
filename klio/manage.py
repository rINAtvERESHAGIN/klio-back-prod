#!/usr/bin/env python
import os
import sys


if __name__ == "__main__":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

    try:
        from configurations.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing.
        try:
            import django  # noqa
        except ImportError as exc:
            raise ImportError(
                """Couldn't import Django. Are you sure it's installed and
                available on your PYTHONPATH environment variable? Did you
                forget to activate a virtual environment?"""
            ) from exc
        raise
    execute_from_command_line(sys.argv)
