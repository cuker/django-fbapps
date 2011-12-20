from django.contrib import admin
from django.contrib.contenttypes import generic
from models import FlatFacebookTab, GenericContentFacebookTab

class GenericContentFacebookTabAdmin(admin.ModelAdmin):
    list_display = ['slug', 'active']
    list_filter = ['active', 'sites']

admin.site.register(FlatFacebookTab, GenericContentFacebookTabAdmin)

class GenericContentFacebookTabInline(generic.GenericStackedInline):
    model = GenericContentFacebookTab
    max_num = 1
    extra = 1
