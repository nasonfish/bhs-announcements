#!/usr/bin/python2.7

# A fully fledged cron system doesn't exactly fit our one task, so we can just
# throw our task in here.

# 0 0 * * * python2.7 $blah.py

from announcements.models import Post
from time import time as now

posts = Post.query.filter_by(archived=False, deleted=False).all()

for i in posts:
    if now() > i.expire:
        i.archive()

print("Expired old announcements")