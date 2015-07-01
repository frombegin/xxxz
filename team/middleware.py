#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.http import Http404

class YourMiddleware(object):

    def process_request(self, request):
        ## 如果需要认证，使用下述方法：
        ## ---------------------------------------
        ## if request.user.is_authenticated():
        ##      #TODO: after authenticated...
        ##
        ## 或者：
        ## request.your_object = 设置 app 相关对象
        pass