from django.conf import settings
import hashlib
import base64

def get_sector():
    return settings.B2P_SECTOR


def get_secret():
    return settings.B2P_SECRET


def get_base_url():
    return settings.B2P_BASE_URL


def get_authorize_url():
    return f'{get_base_url()}/Authorize'

# Authorize
# Purchase

def get_register_url():
    return f'{get_base_url()}/Register'


def get_success_url(order_id):
    return str(settings.B2P_SUCCESS_REDIRECT).replace('{orderId}', str(order_id))


def get_fail_url(order_id):
    return str(settings.B2P_FAIL_REDIRECT).replace('{orderId}', str(order_id))


def generate_signature(data_to_signatur):
    combined = ''.join([get_sector(), *[str(el) for el in data_to_signatur], get_secret()])
    hash = hashlib.md5(combined.encode("utf-8")).hexdigest().encode('utf-8')
    hash64 = base64.b64encode(hash)
    return hash64