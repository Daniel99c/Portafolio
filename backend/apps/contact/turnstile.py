import json
import logging
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from django.conf import settings

logger = logging.getLogger(__name__)

VERIFY_URL = 'https://challenges.cloudflare.com/turnstile/v0/siteverify'


def verify(token, ip=None):
    """Confirma con Cloudflare que el captcha lo resolvió una persona."""
    if not settings.TURNSTILE_SECRET_KEY or not token:
        return False
    data = {'secret': settings.TURNSTILE_SECRET_KEY, 'response': token}
    if ip:
        data['remoteip'] = ip
    try:
        with urlopen(Request(VERIFY_URL, data=urlencode(data).encode()), timeout=8) as response:
            return bool(json.load(response).get('success'))
    except (URLError, TimeoutError, ValueError):
        logger.exception('No se pudo verificar Turnstile')
        return False
