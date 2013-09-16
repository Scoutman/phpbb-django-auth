# -*- coding: utf-8 -*-

from django.contrib import admin
from phpbb import models as pm

class PhpbbUserAdmin(admin.ModelAdmin):
    list_display = ('username',
                    'user_id',
                    'user_regdate',
                    'user_posts',
                    'user_email', )
admin.site.register(pm.PhpbbUser, PhpbbUserAdmin)

class PhpbbConfigAdmin(admin.ModelAdmin):
    list_display = ('config_name',
                    'config_value',
                    'is_dynamic')
admin.site.register(pm.PhpbbConfig, PhpbbConfigAdmin)

class PhpbbAclRoleAdmin(admin.ModelAdmin):
    pass
    # list_display = ('role_id',
    #                 'role_name',
    #                 'role_description',
    #                 'role_type',
    #                 'role_order')
admin.site.register(pm.PhpbbAclRole, PhpbbAclRoleAdmin)

class PhpbbAclRoleOptionAdmin(admin.ModelAdmin):
    pass
    # list_display = ('auth_option_id',
    #                 'auth_option',
    #                 'auth_global')
admin.site.register(pm.PhpbbAclOption, PhpbbAclRoleOptionAdmin)
# admin.site.register(pm.PhpbbAclRoleDatum)
# Composite keys support needed
# admin.site.register(pm.PhpbbAclGroup)
admin.site.register(pm.PhpbbGroup)



class GroupMappingAdmin(admin.ModelAdmin):
    list_display = ('django_group',
                    'phpbb_group', )
admin.site.register(pm.GroupMapping, GroupMappingAdmin)


class PhpbbUserGroupAdmin(admin.ModelAdmin):
    list_display = ('group',
                    'user', )
admin.site.register(pm.PhpbbUserGroup, PhpbbUserGroupAdmin)

