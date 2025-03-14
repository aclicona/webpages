from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
import json
import os

register = template.Library()


def load_vite_manifest():
    if not hasattr(load_vite_manifest, 'manifest'):
        manifest_path = getattr(settings, 'VITE_MANIFEST_PATH', None)
        if manifest_path and os.path.exists(manifest_path):
            with open(manifest_path) as f:
                load_vite_manifest.manifest = json.load(f)
        else:
            load_vite_manifest.manifest = {}
    return load_vite_manifest.manifest


@register.simple_tag
def vite_asset(path):
    """
    Template tag to load Vite assets with HMR support in development
    and proper static files in production.

    Usage: {% vite_asset 'src/main.js' %}
    """
    if settings.VITE_DEV_MODE:
        server_url = f"{settings.VITE_DEV_SERVER_PROTOCOL}://{settings.VITE_DEV_SERVER_HOST}:{settings.VITE_DEV_SERVER_PORT}"
        return mark_safe(f'<script type="module" src="{server_url}/{path}"></script>')

    manifest = load_vite_manifest()
    if path in manifest:
        file_path = manifest[path]['file']
        return mark_safe(f'<script type="module" src="{settings.STATIC_URL}{file_path}"></script>')

    raise ValueError(f'Vite manifest does not contain path: {path}')