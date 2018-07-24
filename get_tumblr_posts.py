#  -*- coding: utf-8 -*-
# inspired in https://github.com/veggiedefender/miraculousladybot/blob/master/log.py
import requests
import re
import tumblr_client

from html2text import html2text
from datetime import datetime

from settings import blogs_to_search, posts_per_blog, tags_to_search, posts_per_search

def append_to_file(filename, contents):
    with open(filename, 'a', encoding='utf8') as file:
        file.write(contents)

def clean_up(text):
    text = text.replace('\n', '')
    text = re.sub(r'\!?\[.*\]\(.+\):?', '', text)
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('~', '')
    text = text.replace('>', '')
    text = text.replace('#', '')
    text = text.strip()
    return text

def get_posts(search_function, search_parameter, post_search_limit):
    total = 0
    earliest = int(datetime.now().timestamp())
    iterations_without_posts = 0

    while total <= post_search_limit and iterations_without_posts < 5:
        posts = search_function(search_parameter, earliest)

        if len(posts) > 0:
            earliest = min([ post["timestamp"] for post in posts ])
        else:
            break

        posts = [ post for post in posts if post["type"] == "text" ]
        if len(posts) == 0:
            iterations_without_posts += 1

        for post in posts:
            body = html2text(post["body"])

            text = clean_up(body)
            if len(text) == 0:
                continue

            print(text)
            print("********")
            append_to_file('text_source.txt', text)
            total += 1

    print(f'No more posts found for {search_parameter}. Total found: {total}.')

for blog in blogs_to_search:
    get_posts(tumblr_client.get_posts_from_blog, blog, posts_per_blog)

for tag in tags_to_search:
    get_posts(tumblr_client.get_posts_from_search, tag, posts_per_search)