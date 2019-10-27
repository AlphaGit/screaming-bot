#  -*- coding: utf-8 -*-
from functions import get_posts, tumblr_client

import os
import boto3

s3_bucket_name = os.environ['S3_BUCKET_NAME']
s3_file_path = os.environ['S3_TEXT_FILE_PATH']
blogs_to_search = os.environ['BLOGS_TO_SEARCH'].split(',')
posts_per_blog = int(os.environ['POSTS_PER_BLOG'])
tags_to_search = os.environ['TAGS_TO_SEARCH'].split(',')
posts_per_search = int(os.environ['POSTS_PER_SEARCH'])
line_limit_in_source = int(os.environ['LINE_LIMIT_SOURCE_FILE'])

downloaded_file = '/tmp/text_source.txt'
new_file = '/tmp/new_text_source.txt'

s3 = boto3.client('s3')
s3.download_file(s3_bucket_name, s3_file_path, downloaded_file)

with open(downloaded_file) as f:
    tumblr_posts = f.readlines()

search_function = tumblr_client.get_posts_from_blog
for blog in blogs_to_search:
    blog_posts = get_posts(search_function, blog, posts_per_blog)
    tumblr_posts.extend(blog_posts)

search_function = tumblr_client.get_posts_from_search
for tag in tags_to_search:
    tag_search_posts = get_posts(search_function, tag, posts_per_search)
    tumblr_posts.extend(tag_search_posts)

tumblr_posts = tumblr_posts[-line_limit_in_source:]

with open(new_file, 'w', encoding='utf8') as f:
    f.writelines(tumblr_posts)

s3.upload_file(new_file, s3_bucket_name, s3_file_path)