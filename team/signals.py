#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.dispatch import Signal


member_added = Signal(providing_args=["membership"])
