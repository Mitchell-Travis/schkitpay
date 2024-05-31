"""
Django settings for schkitpay project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import os
from pathlib import Path
from django.core.wsgi import get_wsgi_application

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/js', 'serviceworker.js')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vio%o1wdilz*o^ds@=(q^#@qbae7j*nc_7)5hbw!#mum+#^=^a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '172.20.10.11', '127.0.0.1', '0.0.0.0']

# 'localhost', '172.20.10.11', '0.0.0.0', '127.0.0.1'

related_name='+'

AUTH_USER_MODEL = 'accounts.User'

# Backend for case insensitivity
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
    'accounts.backends.CaseInsensitiveModelBackend'
)



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pwa',


    # My apps
    'accounts',
    'core',
    'friends',
    'wellet',
]

PWA_APP_NAME = 'ChargeBoot'
PWA_APP_DESCRIPTION = "Charge your phone on-the-go!"
PWA_APP_THEME_COLOR = '#FFDE59'
PWA_APP_BACKGROUND_COLOR = '#FFDE59'
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'any'
PWA_APP_START_URL = ''
PWA_APP_STATUS_BAR_COLOR = 'default'
PWA_APP_ICONS = [
    {
        'src': 'static/svg/logos/chargebootlogo.png',  # Adjust the path accordingly
        'sizes': '192x192',  # Adjust the size as needed
    }
]

PWA_APP_ICONS_APPLE = [
    {
        'src': 'static/svg/logos/chargebootlogo.png',  # Adjust the path accordingly
        'sizes': '180x180',  # Adjust the size as needed
    }
]

PWA_APP_SPLASH_SCREEN = [
    {
        'src': 'static/svg/logos/chargebootlogo.png',  # Adjust the path accordingly
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)',
        'sizes': '750x1334',  # Adjust the size as needed
    }
]

PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'en-US'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'schkitpay.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'schkitpay.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Email Backends
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS= True
EMAIL_HOST= 'smtp.gmail.com'
EMAIL_HOST_USER= 'mitchellsherman01@gmail.com' 
EMAIL_HOST_PASSWORD= 'cbvdujfpfmornzog'

EMAIL_PORT=587
SERVER_EMAIL= EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = 'Schkit Pay no-reply@schkitpay.localhost'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'home' 
LOGIN_URL = 'sign-in'
