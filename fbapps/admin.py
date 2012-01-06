from django.contrib import admin
from django.contrib.contenttypes import generic

from models import FlatFacebookTab, GenericContentFacebookTab
from forms import FlatFacebookTabForm

class FlatFacebookTabAdmin(admin.ModelAdmin):
    list_display = ['slug', 'active']
    list_filter = ['active', 'sites']
    form = FlatFacebookTabForm

admin.site.register(FlatFacebookTab, FlatFacebookTabAdmin)

class GenericContentFacebookTabInline(generic.GenericStackedInline):
    model = GenericContentFacebookTab
    max_num = 1
    extra = 1
