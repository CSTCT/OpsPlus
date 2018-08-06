#-*- coding: utf-8 -*-
from accounts.models import User
from django.contrib.auth.models import Group
from django import forms
from django.contrib import auth

class LoginForm(forms.Form):
    username = forms.CharField(required=True,label=u"用户名",error_messages={'required': u'请输入用户名'},widget=forms.TextInput(attrs={'placeholder':u"用户名"}))
    password = forms.CharField(required=True,label=u"密码",error_messages={'required': u'请输入密码'},widget=forms.PasswordInput(attrs={'placeholder':u"密码"}))

    def __init__(self, request=None, *args, **kwargs):
        self.request = request
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)


    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = auth.authenticate(username=username, password=password)
            if self.user_cache is None:         
               raise forms.ValidationError(u'账号密码不匹配')
        return self.cleaned_data
        
    def get_user(self):
        return self.user_cache


class UserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        #设置Form显示默认值
        #默认值
        # self.initial['is_active'] = 'True'
        self.fields['password'].required = False

    class Meta:
        model = User
        fields = ('username', 'password', 'fullname','email', 'mobile', 'groups', 'is_superuser', "is_active", )
        widgets = {
            'username' : forms.TextInput(attrs={'class':'form-control'}),
            'groups' : forms.Select(attrs={'class':'form-control'}),
            'email' : forms.TextInput(attrs={'class':'form-control'}),
            'fullname' : forms.TextInput(attrs={'class':'form-control'}),
            'password' : forms.TextInput(attrs={'class':'form-control'}),
            'mobile' : forms.TextInput(attrs={'class':'form-control'}),
            'is_active' : forms.Select(choices=((True, u'正常'),(False, u'禁用')),attrs={'class':'form-control'}),
            'is_superuser' : forms.CheckboxInput(attrs={'class':'i-checks'})
       }
