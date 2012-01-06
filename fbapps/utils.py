import base64
import hmac
import hashlib

try:
    import json
except ImportError:
    from django.utils import simplejson as json

#TODO if facebook is in our python path, use it instead
def parse_signed_request(signed_request, app_secret):
    try:
        l = signed_request.split('.', 2)
        encoded_sig = str(l[0])
        payload = str(l[1])
    except IndexError:
        raise ValueError("Signed request malformed")
    
    sig = base64.urlsafe_b64decode(encoded_sig + "=" * ((4 - len(encoded_sig) % 4) % 4))
    data = base64.urlsafe_b64decode(payload + "=" * ((4 - len(payload) % 4) % 4))

    data = json.loads(data)

    if data.get('algorithm').upper() != 'HMAC-SHA256':
        raise ValueError("Signed request is using an unknown algorithm")
    else:
        expected_sig = hmac.new(str(app_secret), msg=payload, digestmod=hashlib.sha256).digest()

    if sig != expected_sig:
        raise ValueError("Signed request signature mismatch")
    else:
        return data
