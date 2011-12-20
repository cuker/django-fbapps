#DO not import at test setup time
import base64
import hmac
import hashlib

try:
    import json
except ImportError:
    from django.utils import simplejson as json

from fbapps.views import FacebookTabView
#from fbapps.utils import parse_signed_request

class MockedFacebookTabView(FacebookTabView):
    object = None
    _facebook_data = None
    
    def get_object(self, **kwargs):
        return self.object

def create_signed_request(app_secret, data):
    data['algorithm'] = 'HMAC-SHA256'
    payload = json.dumps(data)
    encoded_payload = base64.urlsafe_b64encode(payload).replace('=','')
    sig = hmac.new(app_secret, msg=encoded_payload, digestmod=hashlib.sha256).digest()
    encoded_sig = base64.urlsafe_b64encode(sig).replace('=','')
    
    signed_request = '%s.%s' % (encoded_sig, encoded_payload)
    #parse_signed_request(signed_request, app_secret)
    return signed_request
