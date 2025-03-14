from .settings import *

DEBUG = env('DEBUG', default=False, cast=bool)
# Production-specific Vite settings
VITE_APP_DIR = os.path.join(BASE_DIR, VITE_APP_ROOT_DIR, 'dist')  # Your Vue app directory
VITE_MANIFEST_PATH = os.path.join(VITE_APP_ROOT_DIR, 'dist', '.vite', 'manifest.json')
VITE_DEV_MODE = False
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', default=['localhost', '127.0.0.1'])

# Production security settings
SECURE_SSL_REDIRECT = env.bool('SECURE_SSL_REDIRECT', default=True)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static and media files configuration
STATIC_HOST = env.url('CDN_STATIC_HOST', default='')
STATIC_URL = f'{STATIC_HOST}/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Nuxt production settings
NUXT_DIST = os.path.join(BASE_DIR, "dashboard/dist")

# CORS settings
CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS', default=['http://localhost:3000'])

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST_USER = "apikey"
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', default="EMAIL_HOST_PASSWORD")

# Optional AWS S3 configuration
if env.bool('USE_S3', default=False):
    AWS_ACCESS_KEY_ID = env.str('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = env.str('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = env.str('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # Media files
    DEFAULT_FILE_STORAGE = 'storage_backends.PublicMediaStorage'
    MEDIA_ROOT = 'media'
    MEDIA_URL = f"https://{AWS_S3_CUSTOM_DOMAIN}/{MEDIA_ROOT}/"
    PRIVATE_MEDIA_LOCATION = 'media/private'
    PRIVATE_FILE_STORAGE = 'storage_backends.PrivateMediaStorage'
    PUBLIC_MEDIA_LOCATION = 'media/public'
else:
    # Local storage configuration
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
    PRIVATE_MEDIA_LOCATION = os.path.join(MEDIA_ROOT, 'private')
    PRIVATE_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    # Make sure the directories exist
    os.makedirs(MEDIA_ROOT, exist_ok=True)
    os.makedirs(PRIVATE_MEDIA_LOCATION, exist_ok=True)

FRONTEND_HOST = env.str('FRONTEND_HOST', default=None)
FRONTEND_SCHEME = env.str('FRONTEND_SCHEME', default='https')

STATICFILES_DIRS += [
    os.path.join(VITE_APP_ROOT_DIR, 'dist'),  # Vite's production build output
]