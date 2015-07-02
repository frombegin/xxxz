#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.conf.urls import include, url
## from .views import ObjectListView

urlpatterns = [

    ## 标准格式：
    ## -------------------------------------------------
    ##  ^/object/$  # will list all objects
    ##  ^/object/(?<object_id>\d+)/$ # will give details for a specific object
    ##  ^/object/edit/(?<object_id>\d+)/$ # will edit an object
    ##  ^/object/delete/(?<object_id>\d+)/$ # will delete an object
    ##  ^/object/add/$ # will add an object
    ## --------------------------------------------------
    ## url(r'^admin/', include(admin.site.urls)),

    # url(r'^$', name='list')
]
