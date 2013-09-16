# -*- coding: UTF-8 -*-
# This file is part of django-phpbb, integration between Django and phpBB
# Copyright (C) 2007-2008  Maciej Bliziński
# 
# django-phpbb is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# django-phpbb is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with django-phpbb; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor,
# Boston, MA  02110-1301  USA

import re

from django.template.defaultfilters import stringfilter
from django import template
from django.conf import settings

# Requires http://code.google.com/p/postmarkup
from postmarkup import render_bbcode

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
@stringfilter
def bbcode(s):
    return mark_safe(render_bbcode(s))

@register.filter
def withlink(obj):
    return "<a href=\"%s\" rel=\"nofollow\">%s</a>" % (obj.get_absolute_url(), str(obj))
