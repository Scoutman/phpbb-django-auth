# -*- coding: UTF-8 -*-

import logging

from django.contrib.auth.models import User, Group
from . import middleware
from models import PhpbbUser, PhpbbGroup, GroupMapping, PhpbbUserGroup
import password as php_password

from django.conf import settings

logging.basicConfig(level=logging.DEBUG)
logging.debug(str(getattr(settings, 'DEBUG', True)))
if getattr(settings, 'DEBUG', True):
    logging_level = logging.DEBUG
else:
    logging_level = logging.FATAL
logging.basicConfig(level=logging_level)

class PhpbbBackend:
    supports_object_permissions = False
    supports_anonymous_user = False

    def authenticate(self, username=None, password=None):
        # Authenticate user against phpBB3 database.
        # Check if the user exists in Django users. If not, create it.
        # Then authenticate.
        
        logging.debug("PhpbbBackend::authenticate()")
        user = None
        try:
            phpbb_user = PhpbbUser.objects.get(username_clean = username.lower())
        except PhpbbUser.DoesNotExist:
            # The user does not exist in phpBB. Bailing out.
            logging.info("User '%s' doesn't exist." % username)
            print("User '%s' doesn't exist." % username)
            return None
        phpbb_checker = php_password.PhpbbPassword()
        if phpbb_checker.phpbb_check_hash(password, phpbb_user.user_password):
            logging.debug("User %s successfully authenticated "
                         "with phpBB database." % username)
        else:
            # Invalid password
            logging.info("Wrong password for user %s" % username)
            return None
        # At this point we have successfully checked phpBB user password.
        # Now we're getting and returning Django user. If necessary, we're
        # creating the user on the fly.
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            logging.info("Creating new Django user '%s'" % username)
            if username:
                user = User(username = username, password = "")
                user.is_staff = False
                user.is_superuser = False

                user.email = phpbb_user.user_email
                user.save()
            else:
                logging.warning("User name empty. Not creating.")
                return None
        # In case the phpBB password has changed, we're updating user's
        # Django password. Django password is necessary when user wants to log
        # in to the admin interface.
        user.set_password(password)
        logging.debug("Returning user '%s'" % user)
        return user

    def get_user(self, user_id):
        user = User.objects.get(pk = user_id)
        logging.debug("get_user(): Returning user '%s'" % user)
        return user

    def get_group_permissions(self, user_obj, request=None):
        print('1')
        request = middleware.get_current_request()
        
        if not 'perms_all' in request.session:
            request.session['perms_all'] = set()
            print('2')
            if not hasattr(user_obj, '_group_perm_cache'):
                
                phpbbuser = PhpbbUser.objects.filter(username_clean = user_obj.username.lower())
                if phpbbuser:
                    print('name check')
                else:
                    print('name not ckeck')
                    user_obj._group_perm_cache = set()
                    return user_obj._group_perm_cache
                print('username: %s' % phpbbuser)
                
                perms_all = None
                user_obj._group_perm_cache = set()
                phpbb_group = PhpbbUserGroup.objects.filter(user = user_obj.id)

                for pg in phpbb_group:

                    django_group = GroupMapping.objects.filter(phpbb_group = pg)
                    for dg in django_group:

                        group = Group.objects.get(id = dg.django_group_id)
                        perms = group.permissions.all()
                        if perms_all is None:
                            perms_all = perms
                        else:
                            perms_all | perms
                
                user_obj._group_perm_cache.update([u"%s.%s" % (p.content_type.app_label, p.codename) for p in perms_all])
                request.session['perms_all'] = user_obj._group_perm_cache
                
        return request.session['perms_all']
                
    def get_all_permissions(self, user_obj):
        #if not hasattr(user_obj, '_perm_cache'):
        #    user_obj._perm_cache = set("%s.%s" % (p.content_type.app_label, p.codename) for p in user_obj.user_permissions.select_related())
        #user_obj._perm_cache.update(self.get_group_permissions(user_obj))
        print('get_all_permissions')
        return self.get_group_permissions(user_obj)
        #return user_obj._perm_cache

    def has_perm(self, user_obj, perm):
        print('has_perm')
        return perm in self.get_all_permissions(user_obj)

    def has_module_perms(self, user_obj, app_label):
        print('has_module_perms')
        # Returns True if user_obj has any permissions in the given app_label.

        for perm in self.get_all_permissions(user_obj):
            if perm[:perm.index('.')] == app_label:
                return True
        return False
