from __future__ import division
import json
from string import punctuation

tweets = open("o2.txt").read()
tweets_list = tweets.split('\n')

pos_sent = open("positive.txt").read()
positive_words=pos_sent.split('\n')
positive_counts=[]

neg_sent = open('negative.txt').read()
negative_words=neg_sent.split('\n')
negative_counts=[]

def analysis(tag, tweet):
    out = {}
    out['tag'] = tag
    res = 0
    neg = {}
    pos = {}
    positive_counter = 0
    negative_counter = 0

    t = tweet.lower()
    for p in list(punctuation):
        t = t.replace(p, '')

    words = t.split(' ')
    wc = len(words)
    for word in words:
        if word != '':
            if word in positive_words:
                if word in pos:
                    pos[word] = pos[word] + 1
                else:
                    pos[word] = 1
                positive_counter = positive_counter + 1
            elif word in negative_words:
                if word in neg:
                    neg[word] = neg[word] + 1
                else:
                    neg[word] = 1
                negative_counter = negative_counter + 1
    res = (positive_counter) - (negative_counter)
    print res, positive_counter, negative_counter
    out['results'] = res
    out['positive_words'] = pos
    out['negative_words'] = neg
    out['word_count'] = wc
    out['rating'] = round((res/wc)*100, 2)
    return out

o = []
for tweet in tweets_list:
    o.append(analysis('obama', tweet))

with open('test.json', 'w') as f:
    f.write(json.dumps(o))
