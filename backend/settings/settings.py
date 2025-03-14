import logging.handlers
import os
from datetime import timedelta

from decouple import config
from dj_database_url import parse as db_url
from gqlauth.settings_type import GqlAuthSettings, email_field, first_name_field

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT_URLCONF = 'urls'
WSGI_APPLICATION = 'wsgi.application'

# Vite's configuration for the Vue frontend
VITE_DEV_SERVER_HOST = config('VITE_DEV_SERVER_HOST', default='localhost')
VITE_DEV_SERVER_PORT = config('VITE_DEV_SERVER_PORT', default=5173, cast=int)
VITE_DEV_SERVER_PROTOCOL = config('VITE_DEV_SERVER_PROTOCOL', default='http')

# Security settings with better defaults
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ADMINS = [
    ('Admin Name', config('ADMIN_EMAIL', default='admin@example.com'))
]

# Application definition with organized grouping
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'django.contrib.sites',
    'django.contrib.humanize',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'whitenoise.runserver_nostatic',
    'strawberry_django',
    'gqlauth',
    'versatileimagefield',
    'django_filters',
    'django_cleanup.apps.CleanupConfig',
    'tinymce',
    'setty'
]

LOCAL_APPS = [
    'apps.core',
    'apps.account',
    # 'apps.document',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Enhanced middleware configuration
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'apps.core.middleware.JWTMiddleware',
    'gqlauth.core.middlewares.django_jwt_middleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'compression_middleware.middleware.CompressionMiddleware',

]
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]
VITE_APP_ROOT_DIR = 'dashboard'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            VITE_APP_ROOT_DIR,
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'apps.core.context_processors.vite_hmr',
            ],
            'libraries': {
                'vite': 'apps.core.templatetags.vite',  # Custom template tags for Vite
                'my_tags': 'apps.core.templatetags.template_tags',
            },
        },
    },
]

# Enhanced database configuration
DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='postgres://localhost/dbname',
        cast=db_url
    )
}

# Improved authentication settings
AUTH_USER_MODEL = "account.User"
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

GQL_AUTH = GqlAuthSettings(
    LOGIN_REQUIRE_CAPTCHA=False,
    REGISTER_REQUIRE_CAPTCHA=False,
    REGISTER_MUTATION_FIELDS={email_field, first_name_field},
    JWT_PAYLOAD_PK=email_field,
    LOGIN_FIELDS={email_field},
    ALLOW_LOGIN_NOT_VERIFIED=config('ALLOW_LOGIN_NOT_VERIFIED', default=True),
    SEND_ACTIVATION_EMAIL=config('SEND_ACTIVATION_EMAIL', default=True),
    PASSWORD_RESET_PATH_ON_EMAIL=config('PASSWORD_RESET_PATH_ON_EMAIL', default="account/password-reset"),
    ACTIVATION_PATH_ON_EMAIL=config('ACTIVATION_PATH_ON_EMAIL', default="account/activate"),
    EMAIL_TEMPLATE_PASSWORD_RESET="mails/account_password_reset_email.html",
    EMAIL_TEMPLATE_ACTIVATION="mails/account_activation_email.html",
    EMAIL_TEMPLATE_ACTIVATION_RESEND="mails/account_activation_email.html",
    EMAIL_SUBJECT_ACTIVATION="mails/account_activation_subject.txt",
    EMAIL_SUBJECT_ACTIVATION_RESEND="mails/account_activation_subject.txt",
    EMAIL_SUBJECT_PASSWORD_RESET="mails/account_password_reset_subject.txt",
    JWT_REFRESH_EXPIRATION_DELTA=timedelta(days=5)
)
# Internationalization
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Base settings for static/media files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'user_image': [
        ('avatar', 'crop__50x50'),
        ('medium', 'crop__300x300')
    ]
}

VERSATILEIMAGEFIELD_SETTINGS = {
    # Images should be pre-generated on Production environment
    "create_images_on_demand": config('CREATE_IMAGES_ON_DEMAND', default=DEBUG)
}

# Modern security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Logging options

LOG_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

# Common formatter settings
CONSOLE_FORMAT = '%(levelname)s %(asctime)s %(name)s:%(lineno)d %(message)s'
FILE_FORMAT = '%(levelname)s %(asctime)s %(name)s:%(lineno)d [%(process)d:%(thread)d] %(message)s'

# Define the base logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': FILE_FORMAT,
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
        'console': {
            'format': CONSOLE_FORMAT,
            'datefmt': '%H:%M:%S',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console',
            'filters': ['require_debug_true'],
        },
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'error.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'critical_file': {
            'level': 'CRITICAL',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'critical.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        'security_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'security.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10MB
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
    'loggers': {
        # Root logger
        '': {
            'handlers': ['console', 'error_file', 'critical_file'],
            'level': 'INFO',
        },
        # Django's internal logger
        'django': {
            'handlers': ['console', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
        # Django template logger
        'django.template': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Django request logger
        'django.request': {
            'handlers': ['mail_admins', 'error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Django security logger
        'django.security': {
            'handlers': ['security_file', 'mail_admins'],
            'level': 'INFO',
            'propagate': False,
        },
        # Database logger
        'django.db.backends': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },
        # Your application logger
        'myapp': {
            'handlers': ['console', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Production-specific settings
if not DEBUG:
    LOGGING['handlers']['error_file']['backupCount'] = 30  # Keep more backups in production
    LOGGING['handlers']['critical_file']['backupCount'] = 30


# Custom exception handler for uncaught exceptions
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Call the default handler for keyboard interrupts
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return

    # Log the exception
    logger = logging.getLogger('root')
    logger.critical(
        'Uncaught exception:',
        exc_info=(exc_type, exc_value, exc_traceback)
    )


# Set the custom exception handler
import sys

sys.excepthook = handle_exception
BACKEND_HOST = config('BACKEND_HOST', default="www.backend-host.com")
SITE_NAME = config('SITE_NAME', default='SITE_NAME')
SITE_ID = 1
SITES = [{'pk': SITE_ID, "domain": BACKEND_HOST, "name": SITE_NAME}]

SETTY_BACKEND = 'CacheBackend'
SETTY_CACHE_TTL = 60  # 60 seconds
