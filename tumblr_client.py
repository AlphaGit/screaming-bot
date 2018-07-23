import requests
import oauth2
import urllib

from settings import auth

def get(url):
    request = requests.get(url)
    json = request.json()
    response = json['response']
    return response

def get_posts_from_blog(blog, before):
    consumer_key = auth['consumer_key']
    response = get(f'https://api.tumblr.com/v2/blog/{blog}.tumblr.com/posts/text?api_key={consumer_key}&before={before}')
    return response['posts']

def create_post(blog, post_content, post_tags=[]):
    client = oauth2.Client(
        oauth2.Consumer(key=auth['consumer_key'], secret=auth['consumer_secret']),
        oauth2.Token(key=auth['oauth_token'], secret=auth['oauth_token_secret'])
    )

    client.request(
        f'https://api.tumblr.com/v2/blog/{blog}/post',
        method='POST',
        body=urllib.parse.urlencode({
            'type': 'text',
            'state': 'queue',
            'body': post_content,
            'tags': ','.join(post_tags),
            'format': 'markdown'
        })
    )