#-*- coding: utf-8 -*-
from django import forms
from saltapi.models import Salt
 
class SaltForm(forms.ModelForm):

    class Meta:
        model = Salt
        exclude = ('uuid','create_time','update_time','status')
        widgets = {
            'name' : forms.TextInput(attrs={'class':'form-control'}),
            'host' : forms.TextInput(attrs={'class':'form-control'}),
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.TextInput(attrs={'class':'form-control'}),
            'comment' : forms.TextInput(attrs={'class':'form-control','rows': '7'}),
       }
