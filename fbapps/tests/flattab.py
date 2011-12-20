from django.test import TestCase
from django.test.client import RequestFactory
from django.contrib.auth.models import AnonymousUser, User

from factories import FacebookTabFactory, FlatFacebookTab

FACTORY = FacebookTabFactory()

class FlatTabModelTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
    
    def test_flat_tab_absolute_url(self):
        tab = FACTORY.create_flat_tab()
        tab.get_absolute_url()
    
    def test_flat_tab_view(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_flat_tab()
        view = MockedFacebookTabView.as_view(object=tab, _facebook_data={})
        request = self.factory.post('/fbapps/flat-tab/someslug/', {'signed_request':'ABC'}, **{'wsgi.url_scheme':'https'})
        request.user = AnonymousUser()
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    #CONSIDER move the following tests to their own testcase, tests the view's handling of errors
    
    def test_flat_tab_view_requires_ssl(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_flat_tab()
        view = MockedFacebookTabView.as_view(object=tab)
        request = self.factory.post('/fbapps/flat-tab/someslug/')
        response = view(request)
        self.assertContains(response, 'SSL Only', status_code=400)
    
    def test_flat_tab_view_requires_post(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_flat_tab()
        view = MockedFacebookTabView.as_view(object=tab)
        request = self.factory.get('/fbapps/flat-tab/someslug/')
        request.user = AnonymousUser()
        response = view(request)
        self.assertContains(response, 'POSTs Only', status_code=400)
    
    def test_flat_tab_view_by_staff_user(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_flat_tab()
        user = User.objects.create_user('username', 'email@email.com', 'password')
        user.is_staff = True
        view = MockedFacebookTabView.as_view(object=tab)
        request = self.factory.get('/fbapps/flat-tab/someslug/', **{'wsgi.url_scheme':'https'})
        request.user = user
        response = view(request)
        self.assertEqual(response.status_code, 200)
    
    def test_flat_tab_view_requires_signed_request(self):
        from mocks import MockedFacebookTabView
        tab = FACTORY.create_flat_tab()
        view = MockedFacebookTabView.as_view(object=tab, _facebook_data={})
        request = self.factory.post('/fbapps/flat-tab/someslug/', **{'wsgi.url_scheme':'https'})
        request.user = AnonymousUser()
        response = view(request)
        self.assertContains(response, 'Missing Signed Request', status_code=400)
    
    def test_flat_tab_view_parses_signed_request(self):
        from mocks import MockedFacebookTabView, create_signed_request
        tab = FACTORY.create_flat_tab()
        payload = MockedFacebookTabView().get_passthrough_facebook_data()
        
        data = {'signed_request':create_signed_request(tab.app_secret, payload)}
        request = self.factory.post('/fbapps/flat-tab/someslug/', data, **{'wsgi.url_scheme':'https'})
        request.user = AnonymousUser()
        
        view = MockedFacebookTabView(object=tab, request=request)
        fb_data = view.get_facebook_data()
        self.assertEqual(fb_data, payload)

class FlatTabManagerTest(TestCase):
    def test_flat_tab_active(self):
        active_tab = FACTORY.create_flat_tab()
        FACTORY.create_flat_tab(active=False)
        FACTORY.create_flat_tab(sites=[])
        
        self.assertEqual(FlatFacebookTab.objects.all().count(), 3)
        
        active_qs = FlatFacebookTab.objects.active()
        self.assertEqual(active_qs.count(), 1)
        self.assertTrue(active_qs.filter(pk=active_tab.pk).exists())

