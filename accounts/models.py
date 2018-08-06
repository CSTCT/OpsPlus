#-*- coding: utf-8 -*-
'''
	Author: Geekwolf
	Blog: http://www.simlinux.com
'''
from django.db import models
from django.contrib.auth.models import Group,Permission,AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.core import validators
import uuid
from django.utils import timezone


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):

        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          last_login=now,
                          **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    
    uuid = models.UUIDField(primary_key=True, auto_created=True, default=uuid.uuid4)
    username = models.CharField(max_length=40, unique=True, verbose_name=u'用户名')
    email = models.EmailField(max_length=255, unique=True, verbose_name=u'邮箱')
    mobile = models.CharField((u'手机'), max_length=30, blank=False,
                              validators=[validators.RegexValidator(r'^[0-9+()-]+$',
                                                                    ('Enter a valid mobile number.'),
                                                                    'invalid')])
    fullname = models.CharField(max_length=64, null=True, verbose_name=u'中文姓名')
    is_active = models.BooleanField(default=False, verbose_name=u'状态')
    is_superuser = models.BooleanField(default=False, verbose_name=u'超级管理员')
    last_login = models.DateTimeField(default=timezone.now, verbose_name='最近登录时间')
    date_joined = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = u'用户'
        verbose_name_plural = verbose_name

    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self): 
        return self.fullname

    def __unicode__(self):
        
        if self.fullname:
            field = self.fullname
        else:
            field = self.username
            
        return field

    def get_short_name(self):
        "Returns the short name for the user."
        return self.username
