from django.views.generic.base import View, TemplateResponseMixin
from django.views.generic.detail import SingleObjectMixin
from django.template import Template, RequestContext
from django.http import HttpResponseBadRequest

from utils import parse_signed_request
from models import FlatFacebookTab, GenericContentFacebookTab

import datetime

class FacebookViewMixin(object):
    def get_app_secret(self):
        raise NotImplementedError
    
    def get_facebook_data(self):
        """Return dictionary with signed request data."""
        if getattr(self, '_facebook_data', None) is None:
            app_secret = self.get_app_secret()
            signed_request = self.request.POST['signed_request']
            self._facebook_data = self._parse_signed_request(signed_request, app_secret)
        return self._facebook_data
    
    def _parse_signed_request(self, signed_request, app_secret):
        return parse_signed_request(signed_request, app_secret)
    
    def get_context_data(self, **kwargs):
        return {'facebook_data': self.get_facebook_data()}

class FacebookTabView(SingleObjectMixin, TemplateResponseMixin, FacebookViewMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return HttpResponseBadRequest('POSTs Only')
        self.object = self.get_object()
        self._facebook_data = self.get_passthrough_facebook_data()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        if not request.is_secure():
            return HttpResponseBadRequest('SSL Only')
        if not request.POST.get('signed_request', None):
            return HttpResponseBadRequest('Missing Signed Request')
        self.object = self.get_object()
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    
    def get_context_data(self, **kwargs):
        data = SingleObjectMixin.get_context_data(self, **kwargs)
        data.update(FacebookViewMixin.get_context_data(self, **kwargs))
        return data
    
    def get_template_names(self):
        templates = [self.template_name]
        if self.object.template_name:
            templates.insert(0, self.object.template_name)
        return templates
    
    def get_app_secret(self):
        return self.object.app_secret
    
    def get_passthrough_facebook_data(self):
        timestamp = datetime.datetime.now().isoformat()
        return {'algorithm':'passthrough',
                'issued_at':timestamp,
                'expires':timestamp,
                'app_data':'',
                'page': 
                    {'id':'',
                     'liked':False,
                     'admin':True, },
                'profile_id':0,
                }

class FlatFacebookTabView(FacebookTabView):
    queryset = FlatFacebookTab.objects.active()
    
    def get_context_data(self, **kwargs):
        data = FacebookTabView.get_context_data(self, **kwargs)
        request_context = RequestContext(self.request, data)
        data['content'] = Template(self.object.content).render(request_context)
        return data

flat_tab_view = FlatFacebookTabView.as_view()
generic_tab_view = FacebookTabView.as_view(model=GenericContentFacebookTab)

