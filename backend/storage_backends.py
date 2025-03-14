from abc import ABC

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage


class PublicMediaStorage(S3Boto3Storage, ABC):
    location = settings.PUBLIC_MEDIA_LOCATION
    file_overwrite = False
    default_acl = 'public-read'


class PrivateMediaStorage(S3Boto3Storage, ABC):
    location = settings.PRIVATE_MEDIA_LOCATION
    default_acl = 'private'
    file_overwrite = False
    custom_domain = False


class MediaStorage(S3Boto3Storage, ABC):
    location = 'media'
    file_overwrite = False
    default_acl = 'public-read'
