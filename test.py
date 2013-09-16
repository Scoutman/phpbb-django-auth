# -*- coding: UTF-8 -*-

import os
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = "phpbb_test.settings.local"
sys.path.append('/home/sascha/django-projects/phpbb_test/phpbb_test/')

from django.contrib.auth.models import User, Group
from phpbb.models import PhpbbUser, PhpbbGroup, GroupMapping, PhpbbUserGroup
import password as php_password

 
user_obj = set()
phpbb_group = PhpbbUserGroup.objects.filter(user = 2)

for pg in phpbb_group:
    print('Group: %s' % pg)

    django_group = GroupMapping.objects.filter(phpbb_group = pg)
    for dg in django_group:
        print('ID: %s' % dg.django_group_id)
    

        group = Group.objects.get(id = dg.django_group_id)
        perms = group.permissions.all()
        print(perms)

        user_obj.update([u"%s.%s" % (p.content_type.app_label, p.codename) for p in perms])
            
            
print('perms sum: %s' % user_obj)

