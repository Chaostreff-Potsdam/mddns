"""
Django settings for mddns project.

Generated by 'django-admin startproject' using Django 2.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from .config_reader import config

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.get('general', 'SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.get_bool('general', 'DEBUG', default=False)

ALLOWED_HOSTS = []

# Determine MAIN_URL / FORCE_SCRIPT option
if config.has_option('server', 'HOST'):
	HOST = config.get('server', 'HOST')
	ALLOWED_HOSTS = [HOST]
else:
	HOST = ''
	ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
	'records.apps.RecordsConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mddns.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
				'records.context_processors.admin_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'mddns.wsgi.application'

# MDDNS pypodonasy backend

POWERDNS_URL = config.get('mddns', 'POWERDNS_URL')
POWERDNS_KEY = config.get('mddns', 'POWERDNS_KEY')

ADMIN_NAME = config.get('mddns', 'ADMIN_NAME')
ADMIN_MAIL = config.get('mddns', 'ADMIN_MAIL')

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.' + config.get('database', 'DATABASE_ENGINE'),
        'NAME': config.get('database', 'DATABASE_NAME', True),
        'USER': config.get('database', 'DATABASE_USER'),
        'PASSWORD': config.get('database', 'DATABASE_PASSWORD'),
        'HOST': config.get('database', 'DATABASE_HOST'),
        'PORT': config.get('database', 'DATABASE_PORT'),
    }
}

DEFAULT_AUTO_FIELD='django.db.models.AutoField'


# Logging

if config.has_option('logging', 'FILE'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse'
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue'
            },
        },
        'formatters': {
            'simple': {
                'format': '%(levelname)s %(message)s',
            },
            'verbose': {
                'format': "[%(asctime)s] %(levelname)s %(message)s"
            },
        },
        'handlers': {
            'console': {
                'level': 'DEBUG',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': config.get('logging', 'FILE'),
            }
        },
        'loggers': {
            'django': {
                'handlers': ['file'],
                'level': 'CRITICAL'
            },
            'pt2termin': {
                'handlers': ['file'],
                'level': 'DEBUG',
                'propagate': True,
                'formatter': 'verbose',
            },
        },
    }

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
] if not DEBUG else []


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
