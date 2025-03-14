from .settings import *

DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
# Vite development server settings
VITE_DEV_SERVER = {
    'PROTOCOL': VITE_DEV_SERVER_PROTOCOL,
    'HOST': VITE_DEV_SERVER_HOST,
    'PORT': VITE_DEV_SERVER_PORT
}
VITE_DEV_MODE = config('VITE_DEV_MODE', default=True, cast=bool)

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CORS_ALLOW_CREDENTIALS = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), 'frontend', 'public', 'media')
VITE_APP_DIR = os.path.join(BASE_DIR, VITE_APP_ROOT_DIR, 'static')  # Your Vue app directory
FRONTEND_HOST = config('FRONTEND_HOST', default='localhost:3000')

if FRONTEND_HOST is not None:
    FRONTEND_SCHEME = config('FRONTEND_SCHEME', default='http')

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

PRIVATE_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
PUBLIC_MEDIA_LOCATION = os.path.join(MEDIA_ROOT, 'public')
PRIVATE_MEDIA_LOCATION = os.path.join(MEDIA_ROOT, 'private')
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'