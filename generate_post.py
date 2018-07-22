import markovify
import spacy
import random
import tumblr_client
import settings
import re
import nltk

class SpacyText(markovify.Text):
    def __init__(self, file):
        markovify.Text.__init__(self, file)
        print('loading spacy en nlp module...')
        self.__nlp = spacy.load('en')

    def word_split(self, sentence):
        return [ "::".join((word.orth_, word.pos_)) for word in self.__nlp(sentence) ]

    def word_join(self, words):
        return " ".join(word.split("::")[0] for word in words)

class NltkText(markovify.Text):
    def __init__(self, file):
        markovify.Text.__init__(self, file)

    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        if words[0] != "":
            words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        else:
            words = list("",)
        return words

    def word_join(self, words):
        return " ".join(word.split("::")[0] for word in words)


print('loading text...')
with open('text_source.txt', 'r', encoding='utf8') as f:
    #text_model = markovify.Text(f)
    #text_model = SpacyText(f)
    text_model = NltkText(f)

post = None
while post is None:
    post = text_model.make_sentence()

post = "AAAAAAAAAAAAAAHHH!!!\n\n" + post + "\n\nAAAAAAAAAAAAAAHHH!!!"
post = post.upper()

print(f"Generated post: {post}")

tumblr_client.create_post('screaming-bot', post, settings.tags_to_post)