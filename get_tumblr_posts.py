#  -*- coding: utf-8 -*-
from functions import get_posts, tumblr_client

from settings import blogs_to_search, posts_per_blog, tags_to_search, posts_per_search

for blog in blogs_to_search:
    get_posts(tumblr_client.get_posts_from_blog, blog, posts_per_blog)

for tag in tags_to_search:
    get_posts(tumblr_client.get_posts_from_search, tag, posts_per_search)