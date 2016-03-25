from .base import *

# if you want to test with debug off
ALLOWED_HOSTS = [u'127.0.0.1', 'localhost']
STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'


DEBUG = True
SESSION_COOKIE_SECURE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{{ cookiecutter.repo_name }}',
        'USER': '{{ cookiecutter.repo_name }}',
        'PASSWORD': '{{ cookiecutter.repo_name }}',
        'HOST': 'localhost',
        'PORT': '',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

MEDIA_ROOT = str(PROJECT_ROOT)
MEDIA_URL = '/media/'

STATIC_ROOT = str(PROJECT_ROOT / 'static')


# TODO: Fix this when devserver is python3 compat
# INSTALLED_APPS = ('devserver',) + INSTALLED_APPS
INSTALLED_APPS += (
    'debug_toolbar',
    'template_debug',
)

MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}

INTERNAL_IPS = ('127.0.0.1',)

DEVSERVER_ARGS = ['--werkzeug']


EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


DEVSERVER_MODULES = (
    'devserver.modules.sql.SQLRealTimeModule',
    'devserver.modules.sql.SQLSummaryModule',
    'devserver.modules.profile.ProfileSummaryModule',

    # Modules not enabled by default
    'devserver.modules.ajax.AjaxDumpModule',
    'devserver.modules.profile.MemoryUseModule',
    'devserver.modules.cache.CacheSummaryModule',
    'devserver.modules.profile.LineProfilerModule',
)

TEMPLATES[0]['OPTIONS']['string_if_invalid'] = 'BAD TEMPLATE VARIABLE: %s'
SECRET_KEY = env('SECRET_KEY')

STRIPE_PUBLIC_KEY = env('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = env('STRIPE_SECRET_KEY')
