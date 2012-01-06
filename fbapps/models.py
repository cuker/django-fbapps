from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.contrib.sites.models import Site

from urllib import urlencode

from managers import FlatFacebookTabManager

class AbstractFacebookTab(models.Model):
    app_id = models.CharField(max_length=255, blank=True) #CONSIDER, is this necessary?
    app_secret = models.CharField(max_length=255)
    template_name = models.CharField(max_length=255, blank=True, null=True, default='fbapps/base.html')
    
    def get_add_url(self, **kwargs):
        params = {'app_id':self.app_id,
                  'next':'http://%s/' % Site.objects.get_current().domain}
        params.update(kwargs)
        return u'https://www.facebook.com/dialog/pagetab?%s' % urlencode(params)
    
    class Meta:
        abstract = True

class FlatFacebookTab(AbstractFacebookTab):
    slug = models.SlugField()
    active = models.BooleanField(db_index=True, default=True)
    content = models.TextField(blank=True)
    
    sites = models.ManyToManyField(Site)
    
    objects = FlatFacebookTabManager()
    
    @models.permalink
    def get_absolute_url(self):
        return ('fbapps:flat-tab', [self.slug], {})

class GenericContentFacebookTab(AbstractFacebookTab):
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    @models.permalink
    def get_absolute_url(self):
        return ('fbapps:generic-tab', [self.pk], {})

