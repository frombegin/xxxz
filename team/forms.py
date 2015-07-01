#!/usr/bin/env python
# -*- coding: UTF-8 -*-

from django import forms
from django.utils.translation import ugettext_lazy as _

## from .models import YourModel

class YourModelForm(forms.ModelForm):
    pass

##    def clean_yourfield(self):
##        return self.cleaned_data["yourfield"]

##    class Meta:
##        model = YourModel
##        fields = [ 'your', 'field', 'here', 'ordered', ]


class YourNormalForm(forms.Form):
    pass

##    field1 = forms.CharField(label="label text")
##    field2 = forms.ChoiceField(choices=YourModel.ROLE_CHOICES, widget=forms.RadioSelect)
