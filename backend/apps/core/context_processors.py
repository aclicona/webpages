def vite_hmr(request):
    """
    Add Vite HMR settings to the template context in development
    """
    from django.conf import settings
    if settings.VITE_DEV_MODE:
        vite_url = f"{settings.VITE_DEV_SERVER_PROTOCOL}://{settings.VITE_DEV_SERVER_HOST}:{settings.VITE_DEV_SERVER_PORT}"
        return {
            'vite_dev_mode': True,
            'vite_server_url': vite_url,
        }
    return {
        'vite_dev_mode': False,
        'vite_server_url': '',
    }
