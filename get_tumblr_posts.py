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

local_file_path = '/tmp/text_source.txt'

s3 = boto3.client('s3')
s3.download_file(s3_bucket_name, s3_file_path, local_file_path)

search_function = tumblr_client.get_posts_from_blog
for blog in blogs_to_search:
    get_posts(search_function, blog, posts_per_blog, file_name=local_file_path)

search_function = tumblr_client.get_posts_from_search
for tag in tags_to_search:
    get_posts(search_function, tag, posts_per_search, file_name=local_file_path)

s3.upload_file(local_file_path, s3_bucket_name, s3_file_path)