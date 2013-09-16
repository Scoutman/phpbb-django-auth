# -*- coding: UTF-8 -*-

import logging
from django.contrib.auth.models import User, Group
from models import PhpbbUser, PhpbbGroup
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
        """Authenticate user against phpBB3 database.

        Check if the user exists in Django users. If not, create it.
        Then authenticate."""
        logging.debug("PhpbbBackend::authenticate()")
        user = None
        try:
            phpbb_user = PhpbbUser.objects.get(username = username)
        except PhpbbUser.DoesNotExist:
            # The user does not exist in phpBB. Bailing out.
            logging.info("User '%s' doesn't exist." % username)
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
        #logging.debug("Returning user '%s'" % user)
        return user

    def get_user(self, user_id):
        user = User.objects.get(pk = user_id)
        #logging.debug("get_user(): Returning user '%s'" % user)
        return user

    def get_group_permissions(self, user_obj):
        print('get_group_permissions')
        # Perms for user scoutman : set([u'auth.add_user', u'auth.delete_user', u'auth.change_user'])
        # set([u'auth.add_user', u'auth.delete_user', u'auth.change_user'])
                
        #permset = set()
        #group = Group.objects.get(pk = 2)
        #perms = group.permissions.all()
        #print(perms)
        #permset.update([u"%s.%s" % (p.content_type.app_label, p.codename) for p in perms])
        """
        for p in perms:
            permset.update([u"%s.%s" % (p.content_type.app_label, p.codename)])
        
        print('TEST: %s' % permset)
        """
        
        phpbbuser = PhpbbUser.objects.filter(username= user_obj.username)[0]
        print(phpbbuser)
        ret = set()
        for phpbb_gid, django_gid in settings.PHPBB_GROUP_MAP:
            if phpbbuser in PhpbbGroup.objects.get(pk=phpbb_gid).members.all():
                django_group = Group.objects.get(pk=django_gid)
                perms = django_group.permissions.all()
                ret.update([u"%s.%s" % (p.content_type.app_label, p.codename) for p in perms])
            logging.debug("Perms for user %s : %s" % (user_obj, ret))
            print("Perms for user %s : %s" % (user_obj, ret))
            #print(ret)
        return ret
        
        """
        user = User.objects.get(username = user_obj.username)
        group = Group.objects.get(pk = 2)
        print group.permissions
        #group.permissions.add(permission)
        user.groups.add(group)
        return group.permissions
        """
        
    # Apparently django also want you to define all the functions below for things to works
    
    def get_all_permissions(self, user_obj):
        print('get_all_permissions')
        return self.get_group_permissions(user_obj)

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
    