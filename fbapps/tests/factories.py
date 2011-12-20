from fbapps.models import FlatFacebookTab, GenericContentFacebookTab

from django.contrib.sites.models import Site

class FacebookTabFactory(object):
    def _create(self, model, kwargs, m2m_kwargs={}):
        instance = model(**kwargs)
        instance.save()
        for key, values in m2m_kwargs.iteritems():
            for value in values:
                getattr(instance, key).add(value)
        return instance
    
    def create_flat_tab(self, **kwargs):
        defaults = {'app_secret':'foobar',
                    'slug':'test',
                    'active':True,
                    'sites':[Site.objects.get_current()]}
        defaults.update(kwargs)
        m2m_kwargs = {'sites':defaults.pop('sites')}
        return self._create(FlatFacebookTab, defaults, m2m_kwargs)
    
    def create_generic_content_tab(self, **kwargs):
        defaults = {'app_secret':'foobar',
                    'content_object':Site.objects.get_current(),}
        defaults.update(kwargs)
        return self._create(GenericContentFacebookTab, defaults)

