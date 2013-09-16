# -*- coding: utf-8 -*-

import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User, Group
from phpbb.utils import slugify
from datetime import datetime
from django.core import exceptions
from django.utils.encoding import force_unicode
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class PhpbbUser(models.Model):
    """Model for phpBB user."""
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    username_clean = models.CharField(max_length=255)
    user_password = models.CharField(max_length=32)
    user_posts = models.IntegerField()
    user_email = models.CharField(max_length=255)
    user_website = models.CharField(max_length=100)
    user_avatar_type = models.IntegerField()
    user_avatar = models.CharField(max_length=250)
    user_regdate_int = models.IntegerField(db_column="user_regdate")
    user_lastvisit_int = models.IntegerField(db_column="user_lastvisit")
    user_sig_bbcode_uid = models.CharField(max_length=8)
    user_sig_bbcode_bitfield = models.CharField(max_length=255)
    def __unicode__(self):
        return self.username
    def user_regdate(self):
        return datetime.fromtimestamp(self.user_regdate_int)
    def user_lastvisit(self):
        return datetime.fromtimestamp(self.user_lastvisit_int)
    class Meta:
        db_table = settings.PHPBB_TABLE_PREFIX + 'users'
        ordering = ['username']

class PhpbbGroup(models.Model):
    id = models.IntegerField(primary_key=True, db_column='group_id')
    group_type = models.IntegerField()
    group_founder_manage = models.IntegerField()
    group_name = models.CharField(max_length=255)
    group_desc = models.TextField()
    group_desc_bitfield = models.CharField(max_length=255)
    group_desc_options = models.IntegerField()
    members = models.ManyToManyField(PhpbbUser, through='PhpbbUserGroup')

    def __unicode__(self):
        #return u"PhpbbGroup(%s, %s)" % (self.id, self.group_name)
        return unicode(self.group_name)
    class Meta:
        db_table = settings.PHPBB_TABLE_PREFIX + 'groups'
        ordering = ['id']

class PhpbbUserGroup(models.Model):
    group = models.ForeignKey(PhpbbGroup, primary_key=True)
    user = models.ForeignKey(PhpbbUser, primary_key=True)
    group_leader = models.IntegerField()
    user_pending = models.IntegerField()
    #def __unicode__(self):
        #return u"PhpbbUserGroup(%s, %s)" % (self.group_id, self.user_id)
    def __unicode__(self):
        return unicode(self.group)
    class Meta:
        db_table = 'phpbb_user_group'

class PhpbbAclRole(models.Model):
    role_id = models.IntegerField(primary_key=True)
    role_name = models.CharField(max_length=255)
    role_description = models.TextField()
    role_type = models.CharField(max_length=10)
    role_order = models.IntegerField()
    def __unicode__(self):
        return force_unicode(self.role_name)
    class Meta:
        db_table = settings.PHPBB_TABLE_PREFIX + 'acl_roles'
        ordering = ['role_name']


class PhpbbAclOption(models.Model):
    auth_option_id = models.IntegerField(primary_key=True)
    auth_option = models.CharField(max_length=60)
    is_global = models.IntegerField()
    is_local = models.IntegerField()
    founder_only = models.IntegerField()
    def __unicode__(self):
        return self.auth_option
    class Meta:
        db_table = settings.PHPBB_TABLE_PREFIX + 'acl_options'
        ordering = ['auth_option_id']

class PhpbbConfig(models.Model):
    config_name = models.CharField(max_length=255, primary_key=True)
    config_value = models.CharField(max_length=255)
    is_dynamic = models.IntegerField()
    def __unicode__(self):
        return self.config_name
    class Meta:
        db_table = settings.PHPBB_TABLE_PREFIX + 'config'
        ordering = ['config_name']
        verbose_name = 'Phpbb config entry'
        verbose_name_plural = 'Phpbb config entries'

class GroupMapping(models.Model):
    django_group = models.ForeignKey(Group)
    phpbb_group = models.ForeignKey(PhpbbGroup)
    def __unicode__(self):
        return unicode(self.django_group)
        