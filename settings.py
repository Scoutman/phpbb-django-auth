from django.conf import settings

# These defaults can be overriden in project's settings.py

PHPBB_TABLE_PREFIX = getattr(settings, 'PHPBB_TABLE_PREFIX', 'phpbb_')
PHPBB_BLOCKED_FORUMS = getattr(settings, 'PHPBB_BLOCKED_FORUMS', [])
PHPBB_SMILIES_URL = getattr(settings, 'PHPBB_SMILIES_URL', '') 
PHPBB_URL =  getattr(settings, 'PHPBB_URL', '')
PHPBB_FORUM_DETAIL_TMPL = getattr(settings,
                                  'PHPBB_FORUM_DETAIL_TMPL',
                                  'phpbb/forum_detail.html')
PHPBB_TOPIC_DETAIL_TMPL = getattr(settings,
                                  'PHPBB_TOPIC_DETAIL_TMPL',
                                  'phpbb/topic_detail.html')
PHPBB_TOPIC_ARCHIVE_DETAIL_TMPL = getattr(settings,
                                          'PHPBB_TOPIC_ARCHIVE_DETAIL_TMPL',
                                          'phpbb/topic_archive_detail.html')
