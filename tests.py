#!/usr/bin/env python
"""
"""
import sys


def run_tests():
    import django
    from django.conf import global_settings
    from django.conf import settings

    if django.VERSION >= (1, 10):
        middleware_setting = 'MIDDLEWARE'
    else:
        middleware_setting = 'MIDDLEWARE_CLASSES'

    middleware = list(getattr(global_settings, middleware_setting) or [])
    middleware.append('corsheaders.middleware.CorsMiddleware')

    config = {
        'INSTALLED_APPS': [
            'corsheaders',
        ],
        'DATABASES': {
            'default': {
                'ENGINE': 'django.db.backends.sqlite3',
                'TEST_NAME': ':memory:',
            },
        },
        'ROOT_URLCONF': 'corsheaders.tests',
        middleware_setting: middleware,
    }
    settings.configure(**config)

    if hasattr(django, 'setup'):
        django.setup()

    try:
        from django.test.runner import DiscoverRunner as Runner
    except ImportError:
        from django.test.simple import DjangoTestSuiteRunner as Runner

    test_runner = Runner(verbosity=1)
    return test_runner.run_tests(['corsheaders'])


def main():
    failures = run_tests()
    sys.exit(failures)

if __name__ == '__main__':
    main()
