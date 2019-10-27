import requests
import re
import tumblr_client
import html

from datetime import datetime

# inline tags keep text together visually (<b>S</b>ame)
# non-inline tags keep text separate (<p>Sentence1</p><p>Sentence2</p>)
html_tags_inline = {
    'a': True,
    'b': True,
    'blockquote': False,
    'br': False,
    'div': False,
    'em': True,
    'figure': False,
    'g': True,
    'h1': False,
    'h2': False,
    'h3': False,
    'h4': False,
    'h5': False,
    'h6': False,
    'hr': False,
    'i': True,
    'iframe': False,
    'img': False,
    'li': False,
    'ol': False,
    'p': False,
    'small': True,
    'source': False,
    'span': True,
    'sub': False,
    'sup': False,
    'strike': True,
    'strong': True,
    'ul': False,
    'video': True
}

def clean_up(text):
    # remove usernames
    text = re.sub(r'<a.*class="tumblr_blog".*>.*</a>:', '', text)
    text = re.sub(r'<a.*class="tumblelog".*>.*</a>', '', text)

    # remove html tags
    for html_tag, is_inline in html_tags_inline.items():
        regex = r'\</?' + html_tag + r'(\s+[^\>]*)?/?\>'
        replacement = '' if is_inline else '\n'
        text = re.sub(regex, replacement, text)

    # all vertical spaces to a single line feed
    text = re.sub(r'[\n\r\f]+', '\n', text)
    # all horizontal spaces to a single space
    text = re.sub(r'[\t\v ]+', ' ', text)
    # all combinations of vertical and horizontal spaces to a single line feed
    text = re.sub(r'\ ?\n\ ?', '\n', text)

    # decode html entities
    text = html.unescape(text)

    # remove start/end spaces
    text = text.strip()

    return text

def get_posts(search_function, search_parameter, post_search_limit):
    total = 0
    earliest = int(datetime.now().timestamp())
    iterations_without_text_posts = 0

    posts_results = []

    while total <= post_search_limit and iterations_without_text_posts < 5:
        posts = search_function(search_parameter, earliest)

        if len(posts) == 0:
            break

        earliest = min([ post["timestamp"] for post in posts ])
        posts = [ post for post in posts if post["type"] == "text" ]

        if len(posts) == 0:
            iterations_without_text_posts += 1
            continue

        for post in posts:
            body = post["body"]
            text = clean_up(body)
            if len(text) == 0:
                continue

            print(body + "\n\n")
            print(text)
            print("****************************************")
            posts_results.append(text + "\n")
            total += 1

    print(f'No more posts found for {search_parameter}. Total found: {total}.')

    return posts_results
