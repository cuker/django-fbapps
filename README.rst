========================================
django-fbapps - Facebook Tabs for Django
========================================

:version: alpha

Introduction
============

This package enables users to create facebook tabs from their Django site.


To use you first have to add ``fbapps`` to ``INSTALLED_APPS``, and then
execute ``syncdb`` to create the tables.

Additionally add the following to your root urlpatterns::
    
    url(r'^fbapps/', include('fbapps.urls', namespace='fbapps')),


FlatFacebookTab
===============

``FlatFacebookTab`` allows a staff user to create a static facebook tab much like one would create a flat page.


GenericContentFacebookTab
=========================

``GenericContentFacebookTab`` is a facebook tab associated to a generic content object. When used with ``GenericContentFacebookTabInline`` staff users are able to associate a facebook tab with an object in the admin.

Example adding ``GenericContentFacebookTabInline`` to the MyModel admin below::

    from django.contrib import admin
    from fbapps.admin import GenericContentFacebookTabInline
    
    from myapp.models import MyModel
    
    class MyModelAdmin(admin.ModelAdmin):
        inlines = [GenericContentFacebookTabInline]
    
    admin.site.register(MyModel, MyModelAdmin)


FacebookTabView
===============

TODO


License
=======

This software is licensed under the ``New BSD License``. See the ``LICENSE``
file in the top distribution directory for the full license text.

.. # vim: syntax=rst expandtab tabstop=4 shiftwidth=4 shiftround

