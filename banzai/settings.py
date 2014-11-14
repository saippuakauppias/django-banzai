from django.conf import settings


BANZAI_API_DOMAIN = getattr(settings, 'BANZAI_API_DOMAIN', 'api.get-n-post.ru')
BANZAI_API_VERSION = getattr(settings, 'BANZAI_API_VERSION', 'v1')
BANZAI_API_KEY = getattr(settings, 'BANZAI_API_KEY', '')
