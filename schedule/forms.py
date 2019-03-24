#!/usr/bin/python
# encoding:utf8
from django import forms
from .models import Excel
from django.forms import ModelForm


class UploadFileForm(ModelForm):
    # flag = forms.BooleanField(required=True)
    # file = forms.FileField()

    class Meta:
        model = Excel
        fields = ['flag', 'file']


