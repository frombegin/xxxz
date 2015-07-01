#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django.db import models
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

## -----------------------------------------------------------------------------
## 验证器

##class YourValidator(object):
##	message = _("输入内容的验证说明.")
##	code = 'invalid'
##
##	def __init__(self):
##		pass
##
##	def __call__(self, value):
##		try:
##			if not validate(value):
##				raise ValidationError(self.message, code=self.code)
##		except ValueError:
##			pass


## -----------------------------------------------------------------------------
## 模型字段

##your_validator = YourValidator()
##
##class YourField(models.CharField):
##	default_validators = [your_validator]
##
##	def validate(self, value, model_instance):
##
##		super(YourField, self).validate(value, model_instance)
##
##	def to_python(self, value):
##		value = super(YourField, self).to_python(value)
##		if value is None:
##			return value
##        ## 可以对数据进行处理
##		value = value.lower()
##		return value


## -----------------------------------------------------------------------------
## 表单字段

##class HiddenFormField(forms.IntegerField):
##
##	def __init__(self, *args, **kwargs):
##		kwargs['widget'] = forms.HiddenInput
##		super(HiddenFormField, self).__init__(*args, **kwargs)