from django.conf import settings
import phpbb.models

# TODO: get rid of hardcoded forum IDs
# They could be fixed by implementing permission tables
# from phpbb, but this runs into bug 373.
#
# http://code.djangoproject.com/ticket/373
#
# More information:
# http://code.djangoproject.com/wiki/MultipleColumnPrimaryKeys
forumqs = phpbb.models.PhpbbForum.objects
for excluded_forum_id in settings.PHPBB_BLOCKED_FORUMS:
  forumqs = forumqs.exclude(forum_id=excluded_forum_id)
