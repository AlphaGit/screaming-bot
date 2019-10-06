import requests
import oauth2
import urllib
import os

tumblr_consumer_key = os.environ['TUMBLR_CONSUMER_KEY']
tumblr_consumer_secret = os.environ['TUMBLR_CONSUMER_SECRET']
tumblr_oauth_token = os.environ['TUMBLR_OAUTH_TOKEN']
tumblr_oauth_secret = os.environ['TUMBLR_OAUTH_SECRET']

def get(url):
    request = requests.get(url)
    json = request.json()
    response = json['response']
    return response

def get_posts_from_blog(blog, before):
    response = get(f'https://api.tumblr.com/v2/blog/{blog}.tumblr.com/posts/text?api_key={tumblr_consumer_key}&before={before}')
    return response['posts']

def get_posts_from_search(search, before):
    response = get(f'https://api.tumblr.com/v2/tagged?api_key={tumblr_consumer_key}&tag={search}&before={before}')
    return response

def create_post(blog, post_content, post_tags=[]):
    client = oauth2.Client(
        oauth2.Consumer(key=tumblr_consumer_key, secret=tumblr_consumer_secret),
        oauth2.Token(key=tumblr_oauth_token, secret=tumblr_oauth_secret)
    )

    response, _ = client.request(
        f'https://api.tumblr.com/v2/blog/{blog}/post',
        method='POST',
        body=urllib.parse.urlencode({
            'type': 'text',
            'state': 'queue',
            'body': post_content,
            'tags': ','.join(post_tags),
            'format': 'html'
        })
    )

    print(f"Response: {response['status']}")