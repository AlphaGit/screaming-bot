#  -*- coding: utf-8 -*-
# inspired in https://github.com/veggiedefender/miraculousladybot/blob/master/log.py
import requests
import re
import tumblr_client

from html2text import html2text
from datetime import datetime

from settings import blogs_to_search

def append_to_file(filename, contents):
    with open(filename, 'a', encoding='utf8') as file:
        file.write(contents)

def clean_up(text):
    text = text.replace('\n', ' ')
    text = re.sub(r'\!?\[.*\]\(.+\)', ' ', text)
    text = text.replace('*', '')
    text = text.replace('_', '')
    text = text.replace('~', '')
    text = text.replace('>', '')
    text = text.replace('#', '')
    return text

for blog in blogs_to_search:
    total = 0
    earliest = int(datetime.now().timestamp())
    iterations_without_posts = 0

    while total <= 100 and iterations_without_posts < 10:
        posts = tumblr_client.get_posts_from_blog(blog, earliest)

        if len(posts) > 0:
            earliest = min([ post["timestamp"] for post in posts ])
        else:
            break

        posts = [ post for post in posts if post["type"] == "text" ]
        if (len(posts) == 0):
            iterations_without_posts += 1

        for post in posts:
            body = html2text(post["body"])
            text = clean_up(body)
            print(text)
            print("********")
            append_to_file('text_source.txt', text)
            total += 1

    print(f'No more posts found from {blog}. Total found: {total}.')
