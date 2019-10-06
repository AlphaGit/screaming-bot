# import spacy
import markovify
import random
import tumblr_client
import re
import nltk
import os
import boto3

tags_to_post = os.environ['TAGS_TO_POST'].split(',')

s3_bucket_name = os.environ['S3_BUCKET_NAME']
s3_file_path = os.environ['S3_TEXT_FILE_PATH']

local_file_path = '/tmp/text_source.txt'

s3 = boto3.client('s3')
s3.download_file(s3_bucket_name, s3_file_path, local_file_path)

# class SpacyText(markovify.Text):
#     def __init__(self, file):
#         markovify.Text.__init__(self, file)
#         print('loading spacy en nlp module...')
#         self.__nlp = spacy.load('en')

#     def word_split(self, sentence):
#         return [ "::".join((word.orth_, word.pos_)) for word in self.__nlp(sentence) ]

#     def word_join(self, words):
#         return " ".join(word.split("::")[0] for word in words)

class NltkText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        if words[0] != "":
            words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        else:
            words = list("",)
        return words

    def word_join(self, words):
        return " ".join(word.split("::")[0] for word in words)

def get_scream():
    scream_length = random.randint(7, 20)
    exclamation_length = random.randint(3, 10)

    return ('A' * scream_length) + 'HHHHHH' + ('!' * exclamation_length)

print('loading gutenberg corpora...')
gutenberg_texts = " ".join([ " ".join(nltk.corpus.gutenberg.words(f)) for f in nltk.corpus.gutenberg.fileids() ])
gutenberg_model = NltkText(gutenberg_texts)

with open(local_file_path, 'r', encoding='utf8') as f:
    #text_model = markovify.Text(f)
    #text_model = SpacyText(f)
    print('loading tumblr corpora...')
    tumblr_text_model = NltkText(f)
    text_model = markovify.combine([tumblr_text_model, gutenberg_model ], [ 2, 1 ])

post = None
while post is None:
    post = text_model.make_sentence()

post = re.sub(r'([\.\?\!\)\(])(\w)', r'\1 \2', post)

print(f"Generated post: {post}")

html_post = f"<p>{get_scream()}</p><p>{post.upper()}</p><p>{get_scream()}</p>"
tumblr_client.create_post('screaming-bot', html_post, tags_to_post)