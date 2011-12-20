from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser

from factories import FacebookTabFactory

FACTORY = FacebookTabFactory()

class GenericTabModelTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_geneirc_tab_absolute_url(self):
        tab = FACTORY.create_generic_content_tab()
        tab.get_absolute_url()
    
    def test_generic_tab_view(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_generic_content_tab()
        view = MockedFacebookTabView.as_view(object=tab, _facebook_data={})
        request = self.factory.post('/fbapps/generic-tab/1/', {'signed_request':'ABC'}, **{'wsgi.url_scheme':'https'})
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 200)

