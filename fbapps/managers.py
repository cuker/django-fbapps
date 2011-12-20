from django.db.models import Manager
from django.contrib.sites.models import Site

class FlatFacebookTabManager(Manager):
    def active(self):
        return self.filter(active=True, sites=Site.objects.get_current())
