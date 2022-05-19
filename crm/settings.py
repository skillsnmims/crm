import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '&15vc2(lq0=8!uke#otuwdkb&5)q1_j&3gw9$si59%8@lr4-h_'

DEBUG = False
ENVIRONMENT = "PROD"

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'crispy_forms',

    'portal',
    'accounts',
    'agents',
    'branches',
    'calls',
    'campaigns',
    'prospects',
    'teams',
    'activities',
    'crm_timezones',

    'channels',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'portal.middleware.CheckUserType',

]

ROOT_URLCONF = 'crm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
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

WSGI_APPLICATION = 'crm.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = False


ASGI_APPLICATION = "crm.routing.application"
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('10.182.27.67', 6379)],
            # "hosts": [('127.0.0.1', 6379)],
        },
    },
}

AUTH_USER_MODEL = 'accounts.User'

CRISPY_TEMPLATE_PACK = "bootstrap4"
LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"

DEFAULT_CALLBACK_GAP = 24   # In Hours

STATIC_URL = "/static/"
MEDIA_URL = "/media/"

if ENVIRONMENT == "LOCAL":
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, "static"),
    ]
    # STATIC_ROOT = os.path.join(BASE_DIR, "static")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "static/")
    MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


STANDARD_DATE_FORMAT = "%d/%m/%y"
STANDARD_TIME_FORMAT = "%H:%M"
STANDARD_DATETIME_FORMAT = "%d/%m/%y - %H:%M"

DATE_FORMAT = [
    STANDARD_DATE_FORMAT,
]
DATE_INPUT_FORMATS = [
    STANDARD_DATE_FORMAT,
]


# sudo docker run -p 6379:6379 -d redis:5
